#!/usr/bin/python
# -*- coding: latin-1 -*-

from posixpath import expanduser
import subprocess
import os
from datetime import datetime
import sys
from os.path import expanduser, join
import shutil
import requests
import time
import re
from returnIP import return_ip
import json

def proc_file(**kwargs):
    
    for path in kwargs['array']:
        if(path.startswith("::")):
            pass
        else:
            for root, dirs, file in os.walk(path):
                for filenames in file:
                    print(filenames)
                    if re.sub(u'[^a-zA-Z0-9: ]', '', filenames) == kwargs['filename']:
                        pathFolder = os.path.join(root, filenames)
                        
                        return pathFolder

    return False



def Execute():
    try:
        arq = open("PrinterLog.txt", "a")
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
            (h, any) = item[30].split(".")
            date = datetime.strptime(h, "%Y%m%d%H%M%S")

            data = {
                "User": item[16],
                "Printer": item[8],
                "FileName": re.sub(u'[^a-zA-Z0-9: ]', '', item[7]),
                "originalFilename": item[7],
                "FilePath": "NULL",
                "Pages": int(item[31]),
                "DATE": date.strftime("%d-%m-%Y %H:%M:%S"),
                "IP": return_ip(item[1])
            }
            traceFile = requests.get(f"http://192.168.0.180:5000/verifyTracerFile?USER={data['User']}").json()
            
            path_array = []
            get_file = subprocess.Popen("cd {} && powershell ./teste.ps1".format(os.path.dirname(sys.argv[0])), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, shell=True)
            for x in get_file.stdout.readlines():
                x = x.decode('latin-1').encode('utf-8').decode('latin-1')
                x = x.replace('\r', '').replace('\n', '')
                
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
                    print(proc_file)
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
                    requests.post('http://192.168.0.180:5000/uploadedFile', files=files)

            rc = True
            while rc:
                verify_service  = subprocess.Popen("wmic printjob get /format:csv", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, shell=True)
                if(verify_service.stdout.read().decode('latin-1').find('Printed') > -1):
                    rc = False
            
            subprocess.Popen("wmic printjob where jobid={} delete".format(item[12]), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, shell=True)
            time.sleep(8)
            print(data)
            requests.post('http://192.168.0.180:5000/setData', json=data)
            
    except Exception as e:
        arq.write(str(e))
        arq.write("\n")
    

Execute()