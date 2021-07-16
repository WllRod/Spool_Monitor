from Models.SQL_Server import SQL_Server
from Controllers import PrinterCounter
from Error import ErrorLog
import sys, os

def generate_error(error):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    filename = os.path.basename(os.path.dirname(__file__))+"\\"+os.path.basename(__file__)
    
    ErrorLog(
        Error=error,
        Script=filename,
        Line=exc_tb.tb_lineno
    )

class InsertPrinter():
    def __init__(self):
        try:
            self.db = SQL_Server()
            
            self.printer = ""
            self.ip = ""
        except Exception as e:
            generate_error(str(e))
    
    def insert_printer(self, ip, desc):
        
        try:
            self.ip = ip
            self.printer = desc
            self.printerCounter = PrinterCounter(self.ip)
            self.printCounter = self.printerCounter.getCounterPrint()
            self.copyCounter = self.printerCounter.getCounterCopy()
            self.scannderCounter = self.printerCounter.getCounterScanner()
            self.othersCounter = self.printerCounter.getCounterOther()
            self.totalCounter = self.printerCounter.getCounter()

            if(self.printCounter is None):
                self.printCounter = 0
            elif(self.copyCounter is None):
                self.copyCounter = 0
            elif(self.scannderCounter is None):
                self.scannderCounter = 0
            elif(self.othersCounter is None):
                self.othersCounter = 0
            elif(self.totalCounter is None):
                self.totalCounter = 0

            query = f"""
            BEGIN
                IF NOT EXISTS (SELECT * FROM Printers 
                        WHERE PrinterIP = '{self.ip}'
                    )
                BEGIN
                    INSERT INTO Printers(PrinterDesc, PrinterIP, TotalPrint, TotalCopy, TotalScanner, TotalOthers, Total)
                    VALUES('{self.printer}', '{self.ip}', {self.printCounter}, {0}, {0}, {0}, {0})
                END
            END
            """

            self.db.set_data(query)
        except Exception as e:
            generate_error(str(query))
