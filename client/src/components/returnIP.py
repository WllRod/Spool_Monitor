import subprocess
import sys
import os
from .Error import ErrorLog
import getpass

def return_ip(printer):
    try:
        array = []
        data = {
            
        }
        cabec = []
        item = []
        proc_start_service  = subprocess.Popen("wmic printer list full", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, shell=True)
        for lines in proc_start_service.stdout.readlines():
            lines = lines.decode('windows-1252')
            lines = ''.join(lines).replace('\n', '').replace('\r', '')
            try:
                
                (key, value) = lines.split("=")
                
                if key not in data.keys():
                    data[key] = []
                
            
                data[key].append(value)
                
            except Exception:
                pass

        cont = 0
        for x in data['DeviceID']:
            if(x == printer):
                break
            cont = cont + 1

        ip = ""
        if(data['PortName'][cont].find("192.168.0") > -1):
            ip = data['PortName'][cont]
            if(ip.find("_") > -1):
                ip = ip.split("_")
                ip = ip[0]

        elif(data['Location'][cont].find("192.168.0") > -1):
            ip = data['Location'][cont]
            ip = ip.split("/")
            ip = ip[2].split(":")
            ip = ip[0]
        return ip
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ErrorLog(
            Error=str(e),
            Script=os.path.basename(os.path.dirname(__file__))+"\\"+os.path.basename(__file__),
            Line=exc_tb.tb_lineno,
            User=str(getpass.getuser())
        )

# cont = 0
# for x in cabec:
#     if(x == "PortName" or x == "Location"):
#         if(item[cont].find("192.168.0.") > -1):
#             ip = item[cont]
#            if(ip.find("_") > -1):
#                 ip = ip.split("_")
#                 ip = ip[0]
               
#             elif(ip.find("/") > -1):
#                 ip = ip.split("/")
#                 ip = ip[2].split(":")
#                 ip = ip[0]
            
#             if(ip not in array):
#                 array.append(ip)
#     cont = cont + 1

# for x in array:
#     print(x)
