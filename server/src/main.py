import os
from os.path import expanduser
import winreg
from datetime import datetime
import socket
import sys
import win32event
import win32service
import win32serviceutil
from collections import namedtuple
from shutil import copy
import time
import servicemanager
import logging.handlers
import subprocess
import shutil
from API import app
import requests

class SpoolAPI(win32serviceutil.ServiceFramework):
    _svc_name_ = "API-Monitorador_De_Spool"
    _svc_display_name_ = "API-Monitorador De Spool"
    _svc_description_ = "API-Monitorador De Spool"

    def __init__(self, args):
        
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        
        
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        
        win32event.SetEvent(self.hWaitStop)
        requests.get('http://localhost:5000/quit')
        #os.system("TASKKILL /F /IM {}".format(self_name))

    def SvcDoRun(self):
        rc = None
        
           
        app.run(host='0.0.0.0', debug=True)
        


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(SpoolAPI)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(SpoolAPI)

# from API import app


# app.run(host='0.0.0.0', debug=True)