
import sys, os, site

# Required for pythonservice.exe to find venv packages
# Will also load pywin32.pth, so the win32* packages will work as normal
script_dir = "C:\\Users\\TI2\\Desktop\\Controle de impressão"
site_packages = os.path.join(script_dir, 'Lib\\site-packages')
try:
    if site_packages not in sys.path:
        site.addsitedir(site_packages)
except Exception:
    pass

from components import Execute
#
import winreg
import os
from os.path import expanduser
import servicemanager
import socket
import sys
import win32event
import win32service
import win32serviceutil
from components.userLogged import return_loggedUser
from components import Execute
import subprocess
# from components import Error

def func():
    text = "LOCAL_PATH={}\nCURRENT_USER={}".format(
        os.getenv("CURRENT_PATH"),
        os.getenv("CURRENT_USER")
    )
    arq = open('C:\\Users\\TI2\\Desktop\\sub_resp.txt', 'w')
    arq.write(text)
    arq.close()

class SpoolMonitorClient(win32serviceutil.ServiceFramework):
    _svc_name_ = "SpoolMonitorClient"
    _svc_display_name_ = "SpoolMonitor"
    _svc_description_ = ""
    
    
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
            os.environ["CURRENT_PATH"] = os.path.dirname(sys.argv[0])
            os.environ['CURRENT_USER'] = return_loggedUser()
            Execute()
            rc = win32event.WaitForSingleObject(self.hWaitStop, 1000)
            if(rc == win32event.WAIT_OBJECT_0):
                break
            else:
                continue
        
if __name__ == '__main__':
    if len(sys.argv) == 1:
        
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(SpoolMonitorClient)
        servicemanager.StartServiceCtrlDispatcher()
    else:
       
        win32serviceutil.HandleCommandLine(SpoolMonitorClient)
