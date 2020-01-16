import os
import arpreq
from prettytable import PrettyTable

if os.geteuid() !=  0:
    print("Please run as root")
    exit(1)

sysip = os.popen("hostname -I | awk '{print $1}'").read().strip()
sysip = sysip.split(".")
myip = sysip[0]+"."+sysip[1]+"."+sysip[2]+"."
t = PrettyTable(['id','IP Address', 'MAC Address'])
item_no = 0

print("-------------------------")
print("Python Wifi Scanner")
print("-------------------------")

timeout = input("Please enter the ping timeout [default:1.5]") or "1.5"
print("Scanning Network... (this will take a while)")
for i in range(1,255):
  cmd = "ping "+myip+str(i)+" -c 1 -W "+timeout+"> /dev/null"
  rcode = os.system(cmd)
  if rcode == 0:
    item_no = item_no + 1
    ip = "192.168.1."+str(i)
    mac = arpreq.arpreq("192.168.1."+str(i))
    if mac == None:
       mac = "Not found"
    t.add_row([item_no,ip,mac])
print(t)
print("Total number of devices:"+str(item_no))