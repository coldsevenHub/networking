from netmiko import ConnectHandler
from datetime import datetime
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
 
with open("devices2_file") as devices_file:
    devices = devices_file.readlines()

for line in devices:
    line = line.strip("\n")
    ipaddr = line.split(",")[0]
    username = line.split(",")[1]
    password = line.split(",")[2]
    enable_password = line.split(",")[3]


    vendor = line.split(",")[4]

    if vendor.lower() == "cisco":
        device_type = "cisco_ios"
        backup_command = "show running-config"

    elif vendor.lower() == "juniper":
        device_type = "juniper"
        backup_command = "show configuration | display set"

    print str(datetime.now()) + " Connecting to device {}" .format(ipaddr)


    try:
        net_connect = ConnectHandler(device_type=device_type,
                                     ip=ipaddr,
                                     username=username,
                                     password=password,
                                     secret=enable_password)

        net_connect.enable()

    except (AuthenticationException):
        print ("Authentication failure: " + ipaddr)
        continue    
    except (NetMikoTimeoutException):
        print("Timeout to device " + ipaddr)
        continue    

    running_config = net_connect.send_command(backup_command)

    print str(datetime.now()) + " Saving config from device {}" .format(ipaddr)

    f = open( "dev_" + ipaddr + "_.cfg", "w")
    f.write(running_config)
    f.close()
    print "=============================================="
