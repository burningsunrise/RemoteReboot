#!/usr/bin/python3
import paramiko
import configparser
import MySQLdb
from multiprocessing.dummy import Pool as ThreadPool 
import time

def reboot(ip_address, cmd):
    with paramiko.SSHClient() as ssh_client:
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh_client.connect(ip_address, username='username', password='password', timeout=10, allow_agent=False)
            ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(cmd, get_pty=True)
            ssh_stdin.write('password' + '\n')
            ssh_stdin.flush()
            timeout = 10
            endtime = time.time() + timeout
            while not ssh_stdout.channel.eof_received:
                time.sleep(1)
                if time.time() > endtime:
                    ssh_stdout.channel.close()
                    break
            output = ssh_stdout.read()
            d_output = output.decode(encoding='UTF-8') 
            print(f"{d_output}")
            if ssh_stderr.read().decode('UTF-8') == None or ssh_stderr.read().decode('UTF-8') == '':
                pass
            else:
                print(ssh_stderr.read())
            print(f"Rebooted => {ip_address}")
            return "Successfully updated!"
        except Exception as e:
            print(f"Conn error {ip_address} {e}")


def connect_db():
    config = configparser.ConfigParser()
    config.read('../lib/db_conf.ini')
    db = MySQLdb.connect(host=config['db_conf']['host'], user=config['db_conf']['user'], passwd=config['db_conf']['pass'], db=config['db_conf']['db'], ssl={'ca':config['db_conf']['ca'], 'key':config['db_conf']['key'], 'cert':config['db_conf']['cert']})
    db.autocommit(True)
    return db


def main(table):
    db = connect_db()
    with db.cursor() as c:
        c.execute(f"SELECT theMachinesIp, somethingElse FROM {table} WHERE condition LIKE %s", ("%condition%",))
        db_list = list(c.fetchall())
    db.close()

    ip = [x[0] for x in db_list]
    cmd = ["sudo -S reboot"] * len(ip)
    pool = ThreadPool(8)
    results = pool.starmap(reboot, zip(ip, cmd))
    pool.close()
    pool.join()


if __name__ == "__main__":
    print(main("table"))
