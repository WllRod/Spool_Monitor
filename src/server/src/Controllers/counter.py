"""
DESCRIÇÃO: NESTE FONTE SERÃO RETIRADAS AS CONTAGENS DAS IMPRESSORAS
____________________________________________________________________

AUTOR: WILLIAM RODRIGUES
____________________________________________________________________

DATA: 08/07/2021

"""

import subprocess
import time
import os, sys
from Error import ErrorLog
from Models import return_oid

def generate_error(error):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    filename = os.path.basename(os.path.dirname(__file__))+"\\"+os.path.basename(__file__)
    
    ErrorLog(
        Error=error,
        Script=filename,
        Line=exc_tb.tb_lineno
    )

def verifyPrinterData(ip, key):
    """
    Função responsável por executar o comando de leitura das impressoras via Terminal.
    Params: IP -> IP da Impressora
            OID -> Identificador de Objeto
    """
    OIDFiles    = return_oid()
    oid         = OIDFiles[ip][key]     
    startCommand= f"SnmpGet.exe -r:{ip} -t:10 -o:{oid}" #Programa que fazem as leituras
    execute = subprocess.Popen(
        startCommand, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT, 
        stdin=subprocess.DEVNULL
    )

    return return_value(execute.stdout.readlines())

def return_value(lines):

    """
    Função resposável por formatar o resultado das leituras da impressoras.
    Param:  lines -> retorno da função verifyPrinterData
    """
    try:
        values = 0
        for lines in lines:
            lines = lines.decode('utf-8')
            if(lines.startswith('Value')):
                (key, value) = lines.split("=")
                values = int(value)
                break
        
        return values
    except Exception as e:
        generate_error(e)

class PrinterCounter():
    def __init__(self, IP):
        self.IP = IP
        self.totalCounter = 0
        self.printCounter = 0
        self.copyCounter = 0
        self.scannerCounter = 0
        self.otherCounter = 0
    
    def getCounterPrint(self):
        """
        Extrai a leitura total das impressões
        """
        try:
            self.printCounter = verifyPrinterData(self.IP, "Print")
            return self.printCounter
        except Exception as e:
            generate_error(e)
    
    def getCounterCopy(self):
        """
        Extrai a leitura total das cópias
        """
        try:
            self.copyCounter = verifyPrinterData(self.IP, "Copy")
            return self.copyCounter
        except Exception as e:
            generate_error(e)

    def getCounterOther(self):
        """
        Extrai a leitura total de outros tipos de usagem da impressora
        """
        try:
            self.otherCounter = verifyPrinterData(self.IP, "Others")
            return self.otherCounter
        except Exception as e:
            generate_error(e)

    def getCounterScanner(self):
        """
        Extrai a leitura total de documentos escaneados
        """
        try:
            self.scannerCounter = verifyPrinterData(self.IP, "Scanner")
            return self.scannerCounter
        except Exception as e:
            generate_error(e)

    def getCounter(self):
        """
        Extrai a leitura total de nums de impressões + num de cópias + num de outros
        """
        try:
            self.totalCounter = verifyPrinterData(self.IP, "Total")
            return self.totalCounter
        except Exception as e:
            generate_error(e)