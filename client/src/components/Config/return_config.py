import json
import subprocess
#from Error import ErrorLog
import sys, os, getpass


def returnConfig():
    
        subprocess.Popen(
            r"net use \\192.168.0.102\SpoolMonitorClient /User:Protheus Totvs@cda && copy \\192.168.0.102\SpoolMonitorClient\config.json C:\Windows", 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            stdin=subprocess.DEVNULL, 
            shell=True
        )
        with open("C:\\Windows\\config.json", "r") as f:
            jsonData = json.load(f)
        f.close()
        print(jsonData)
        return jsonData
    
    