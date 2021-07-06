import subprocess
import time

def verifyPrinterData(ip, oid):
    startCommand = f"SnmpGet.exe -r:{ip} -t:10 -o:{oid}"
    execute = subprocess.Popen(
        startCommand, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT, 
        stdin=subprocess.DEVNULL
    )

    value = return_value(execute.stdout.readlines())
    return value

def return_value(lines):
    values = 0
    for lines in lines:
        lines = lines.decode('utf-8')
        if(lines.startswith('Value')):
            (key, value) = lines.split("=")
            values = int(value)
            break
    return values

class PrinterCounter():
    def __init__(self, IP):
        self.IP = IP
        self.totalCounter = 0
        self.printCounter = 0
        self.copyCounter = 0
        self.scannerCounter = 0
        self.otherCounter = 0
    
    def getCounterPrint(self):
        self.printCounter = verifyPrinterData(self.IP, "1.3.6.1.4.1.2435.2.3.9.4.2.1.5.5.52.21.1.3.1")
        return self.printCounter
    
    def getCounterCopy(self):
        self.copyCounter = verifyPrinterData(self.IP, "1.3.6.1.4.1.2435.2.3.9.4.2.1.5.5.52.21.1.3.2")
        return self.copyCounter

    def getCounterOther(self):
        self.otherCounter = verifyPrinterData(self.IP, "1.3.6.1.4.1.2435.2.3.9.4.2.1.5.5.52.21.1.3.4")
        return self.otherCounter

    def getCounterScanner(self):
        self.scannerCounter = verifyPrinterData(self.IP, "1.3.6.1.4.1.2435.2.3.9.4.2.1.5.5.54.2.2.1.3.4")
        return self.scannerCounter

    def getCounter(self):
        self.totalCounter = verifyPrinterData(self.IP, "1.3.6.1.2.1.43.10.2.1.4.1.1")
        return self.totalCounter