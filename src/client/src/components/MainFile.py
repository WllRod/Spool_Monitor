#!/usr/bin/python
# -*- coding: latin-1 -*-

from posixpath import expanduser
import subprocess
import os
from datetime import datetime
import sys
from os.path import expanduser, join
import requests
import time
import re
from components.returnIP import return_ip
#from returnIP import return_ip
from components.Error import  ErrorLog
from components.Config import returnConfig
from dotenv import load_dotenv
import getpass

def proc_file(**kwargs):
    
    for path in kwargs['array']:
        if not (path.startswith("::")):
            for root, dirs, file in os.walk(path):
                for filenames in file:
                    if re.sub(u'[^a-zA-Z0-9: ]', '', filenames) == kwargs['filename']:
                        return os.path.join(root, filenames)

    return False


def getSSID():
    
    ssid = ""
    ssid = subprocess.Popen(
        "wmic useraccount where name='{}' get sid /FORMAT:CSV".format(os.getenv("CURRENT_USER")), 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT, 
        stdin=subprocess.DEVNULL, 
        shell=True
    )
    for x in ssid.stdout.readlines():
        x = x.decode('windows-1252')
        x = x.replace('\n', '').replace('\r', '')
        if(x.startswith('Node') or x == '\n'):
            pass
        elif(x.find(',') > -1):
            (key, value) = x.split(',')
            ssid = value
            break
    
    return ssid

def block_stop(ssid):
    
    verify = subprocess.Popen(
        "sc sdshow SpoolMonitorClient", 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT, 
        stdin=subprocess.DEVNULL, 
        shell=True
    )
    response = verify.stdout.read().decode('windows-1252')

    if response.find(ssid) <= -1:
        command = f'sc sdset SpoolMonitorClient D:(A;;CCLCSWRPWPDTLOCRRC;;;SY)(D;;RPWP;;;{ssid})(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;BA)(A;;CCLCSWRPLOCRRC;;;IU)(A;;CCLCSWRPLOCRRC;;;SU)(A;;CR;;;AU)(A;;LCRP;;;NS)(A;;LCRP;;;LS)(A;;LCRP;;;AC)S:(AU;FA;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;WD)'
        subprocess.Popen(
            command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            stdin=subprocess.DEVNULL, 
            shell=True
        )

def Execute():
    #load_dotenv(os.path.dirname(sys.argv[0])+"\\.env")
    
    try:
        server = returnConfig()['SERVER']
        ssid = getSSID()
        #block_stop(ssid)
        #subprocess.Popen("sc sdset TESTE4 D:(A;;CCLCSWRPWPDTLOCRRC;;;SY)(D;;RPWP;;;BA)(A;;CCLCSWLOCRRC;;;IU)(A;;CCLCSWLOCRRC;;;SU)S:(AU;FA;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;WD)", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, shell=True)
        
        user = expanduser("~")
        conding = sys.stdout.encoding
        path = os.path.dirname(sys.argv[0])
        cabecalho = ""
        item = ""
        proc_start_service  = subprocess.Popen("wmic printjob get /format:csv", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, shell=True)
        
        for x in proc_start_service.stdout.readlines():
            x = x.decode("windows-1252")
            x = ''.join(x).replace("\n", "").replace("\r", "")
            
            if(x.startswith("Node")):
                cabecalho = x.split(",")
            else:
                item = x.split(",")

        if item == ['']:
            pass
        else:
            
            date = datetime.now()
            data = {
                "User": os.getenv("CURRENT_USER"),
                "Printer": item[8],
                "FileName": re.sub(u'[^a-zA-Z0-9: ]', '', item[7]),
                "originalFilename": item[7],
                "FilePath": "NULL",
                "Pages": int(item[31]),
                "DATE": date.strftime("%Y%m%d %H:%M"),
                "IP": return_ip(item[1])
            }
            
            traceFile = requests.get(f"{server}/verifyTracerFile?USER={data['User']}").json()
            
            path_array = []
            get_file = subprocess.Popen("cd {} && powershell ./OF.ps1".format(os.getenv("CURRENT_PATH")), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, shell=True)
            for x in get_file.stdout.readlines():
                x = x.decode('latin-1').encode('utf-8').decode('latin-1')
                x = x.replace('\r', '').replace('\n', '')
                print(x)
                path_array.append(x)

            
            if(traceFile == False):
                pass
            else:
                if(path_array == []):
                    path_array.append(user+"\\Desktop")
                    procFile = proc_file(
                        array=path_array,
                        filename=data["FileName"]
                    )
                else:
                    procFile = proc_file(
                        array=path_array,
                        filename=data["FileName"]
                    )

                    if not procFile:
                        procFile = proc_file(
                            array=[user+"\\Desktop"],
                            filename=data["FileName"]
                        )
                if( not procFile):
                    pass
                else:
                    fileName = "{}_{}_{}".format(
                        item[16],
                        date.strftime("%Y%m%d_%H%M%S"),
                        os.path.basename(procFile)
                    )
                    files = {
                        'upload_file': open(procFile, 'rb'), 
                        'Name': fileName
                    }
                    requests.post(f'{server}/uploadedFile', files=files)

            rc = True
            while rc:
                verify_service  = subprocess.Popen("wmic printjob get /format:csv", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, shell=True)
                if(verify_service.stdout.read().decode('latin-1').find('Printed') > -1):
                    rc = False
            
            subprocess.Popen("wmic printjob where jobid={} delete".format(item[12]), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, shell=True)
            time.sleep(8)
            
            requests.post(f'{server}/setData', json=data)
            print(data)
            
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        ErrorLog(
            Error=str(e),
            Script=os.path.basename(os.path.dirname(__file__))+"\\"+os.path.basename(__file__),
            Line=exc_tb.tb_lineno,
            User=str(os.getenv("CURRENT_USER"))
        )
