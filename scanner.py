import os
import arpreq
from prettytable import PrettyTable
import requests

def getvendor(mac):
   rval = requests.get("https://api.macvendors.com/"+mac)
   if rval.status_code != 200:
      return "Not found"
   else:
      return rval.text

if os.geteuid() !=  0:
    print("Please run as root")
    exit(1)

sysip = os.popen("hostname -I | awk '{print $1}'").read().strip()
sysip = sysip.split(".")
mynet = sysip[0]+"."+sysip[1]+"."+sysip[2]+"."
t = PrettyTable(['id','IP Address', 'MAC Address','Device Vendor'])
item_no = 0

print("-------------------------")
print("Python Wifi Scanner")
print("-------------------------")

timeout = input("Please enter the ping timeout [default:1.5]") or "1.5"
print("Scanning Network... (this will take a while)")
for i in range(1,255):
  cmd = "ping "+mynet+str(i)+" -c 1 -W "+timeout+"> /dev/null"
  rcode = os.system(cmd)
  if rcode == 0:
    item_no = item_no + 1
    ip = mynet+str(i)
    mac = arpreq.arpreq(mynet+str(i))
    if mac == None:
       mac = "Not found"
       vendor = "Not found"
    else:
       vendor = getvendor(mac)
    t.add_row([item_no,ip,mac,vendor])
  if i%10 == 0:
    print("Scanned IPs do far: "+str(i))
print("Network scan is completed.")
print("Devices found:")  
print(t)
print("Total number of devices:"+str(item_no))