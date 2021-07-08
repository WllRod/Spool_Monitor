import getpass
import os
from os.path import expanduser
import winreg
from datetime import datetime
import ctypes


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
from components import Execute
from GUI import start_gui

class TestService(win32serviceutil.ServiceFramework):
    _svc_name_ = "SpoolMonitorClient"
    _svc_display_name_ = "Spool Monitor"
    _svc_description_ = "TESTE4"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):

        #teste = start_gui()
        #print(teste)
        #ctypes.windll.user32.MessageBoxA(0, "Your text?", "Your title", 0x10)
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
        #print('TESTE')
        #start_gui()
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(TestService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        arq = open('C:\\Windows\\User.txt', 'w')
        arq.write(str(getpass.getuser()))
        arq.close()
        win32serviceutil.HandleCommandLine(TestService)