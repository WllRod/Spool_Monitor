import json
import subprocess
#from Error import ErrorLog
import sys, os, getpass


def returnConfig():
        user = os.getenv('CURRENT_USER')
        temp = "C:\\Windows\\Temp"
        t = subprocess.Popen(
            "net use \\\\192.168.0.102\\SpoolMonitorClient /User:Protheus Totvs@cda && copy \\\\192.168.0.102\\SpoolMonitorClient\\config.json {}".format(temp), 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            stdin=subprocess.DEVNULL, 
            shell=True
        )
        print(t.stdout.read())
        with open(temp+"\\config.json", "r") as f:
            jsonData = json.load(f)
        f.close()
        print(jsonData)
        return jsonData
    
    