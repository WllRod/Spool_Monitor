import os
from os.path import expanduser
import winreg
from datetime import datetime
import ctypes

path    = r'SOFTWARE\Puxada_XML'

if(os.path.exists(path)):
    pass
else:
    winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, path)
    registry_key    = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_WRITE)
    winreg.SetValueEx(registry_key, "XML's", 0, winreg.REG_SZ, os.environ.get('LOCAL_PATH'))
    winreg.CloseKey(registry_key)
import servicemanager
import socket
import sys
import win32event
import win32service
import win32serviceutil
import pyodbc
import json
from collections import namedtuple
from shutil import copy
import winshell
import time
import schedule
import logging.handlers
import subprocess
import shutil
from components import Execute

class TestService(win32serviceutil.ServiceFramework):
    _svc_name_ = "TESTE"
    _svc_display_name_ = "TESTE"
    _svc_description_ = "TESTE"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):

        
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        
        win32event.SetEvent(self.hWaitStop)
        #os.system("TASKKILL /F /IM {}".format(self_name))

    def SvcDoRun(self):
        rc = None
        while True:
            #main()
            #print('TESTE')
            Execute()
            rc = win32event.WaitForSingleObject(self.hWaitStop, 1000)
            if(rc == win32event.WAIT_OBJECT_0):
                break
            else:
                continue


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(TestService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(TestService)