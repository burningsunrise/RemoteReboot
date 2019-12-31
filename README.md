# SSH Reboot for Multiple Machines

Automatci SSH Reboot for multiple machines using a database of IP's as a list to reboot the rigs. Also uses threading to do more than one at a time denoted by the
threadpool argument.

## Basic usage

Requirements
```
paramiko
configparser
MySQLdb
```
- [x] Edit the script add userNames and passwords where necessary (in the paramiko arguments and where paramiko writes) and change MySql calls to your own.
- [x] Run!
