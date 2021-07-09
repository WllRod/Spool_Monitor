import getpass
import os
from os.path import expanduser
import servicemanager
import socket
import sys
import win32event
import win32service
import win32serviceutil
from components import Execute
from components import Error

class SpoolMonitorClient(win32serviceutil.ServiceFramework):
    _svc_name_ = "SpoolMonitorClient"
    _svc_display_name_ = "Spool Monitor"
    _svc_description_ = ""

    def __init__(self, args):
        try:
            win32serviceutil.ServiceFramework.__init__(self, args)
            self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
            socket.setdefaulttimeout(60)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            Error.ErrorLog(
                Error=str(e),
                Script=os.path.basename(os.path.dirname(__file__))+"\\"+os.path.basename(__file__),
                Line=exc_tb.tb_lineno,
                User=str(getpass.getuser())
            )

    def SvcStop(self):

        try:
            self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
            
            win32event.SetEvent(self.hWaitStop)
            #os.system("TASKKILL /F /IM {}".format(self_name))
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            Error.ErrorLog(
                Error=str(e),
                Script=os.path.basename(os.path.dirname(__file__))+"\\"+os.path.basename(__file__),
                Line=exc_tb.tb_lineno,
                User=str(getpass.getuser())
        )

    def SvcDoRun(self):
        try:
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
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            Error.ErrorLog(
                Error=str(e),
                Script=os.path.basename(os.path.dirname(__file__))+"\\"+os.path.basename(__file__),
                Line=exc_tb.tb_lineno,
                User=str(getpass.getuser())
            )


if __name__ == '__main__':
    if len(sys.argv) == 1:
        
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(SpoolMonitorClient)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        try:
            arq = open('C:\\Windows\\User.txt', 'w')
            arq.write(str(getpass.getuser()))
            arq.close()
            win32serviceutil.HandleCommandLine(SpoolMonitorClient)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            Error.ErrorLog(
                Error=str(e),
                Script=os.path.basename(os.path.dirname(__file__))+"\\"+os.path.basename(__file__),
                Line=exc_tb.tb_lineno,
                User=str(getpass.getuser())
            )