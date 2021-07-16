"""
DESCRIÇÃO: FONTE PRINCIPAL
________________________________________________________________
MODO DE USO:    1) - EXECUÇÃO NORMAL
                2) - INSTALAÇÃO COMO SERVIÇO
________________________________________________________________
EXEMPLO DE INSTALAÇÃO COMO SERVIÇO: 

    SpoolMonitorAPI.exe install && SpoolMonitorAPI.exe start
    DIGITE SpoolMonitorAPI.exe /? PARA MAIS EXEMPLOS
________________________________________________________________
AUTOR: WILLIAM RODRIGUES
________________________________________________________________
DATA: 08/07/2021
"""

import os, sys
import socket
import sys
import win32event
import win32service
import win32serviceutil
from collections import namedtuple
from shutil import copy
import servicemanager
import logging
import logging.handlers
import requests
from waitress import serve
class SpoolAPI(win32serviceutil.ServiceFramework):
    _svc_name_ = "SpoolMonitorAPI"
    _svc_display_name_ = "Spool Monitor API"
    _svc_description_ = ""

    def __init__(self, args):
        
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        """
        Função para parar o serviço quando necessário
        """
        
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        
        win32event.SetEvent(self.hWaitStop)
        requests.get('http://localhost:5000/quit') #requisição para parar a execução da API
        #os.system("TASKKILL /F /IM {}".format(self_name))

    def SvcDoRun(self):
        """
        Função para iniciar o serviço e executar a função da API
        """
        rc = None
        
        os.environ['LOCAL_PATH'] = os.path.dirname(sys.argv[0])
        

        from API import app
        serve(app, host='0.0.0.0', port=5000) #API ficará escutando em modo global
        


if __name__ == '__main__':
    if len(sys.argv) == 1:
        """Execução normal"""
        #app.run(host='0.0.0.0', debug=True)
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(SpoolAPI)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        """Como serviço"""

        win32serviceutil.HandleCommandLine(SpoolAPI)

# from API import app

# app.run(host='0.0.0.0', debug=True)
