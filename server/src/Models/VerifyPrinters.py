from Models.SQL_Server import SQL_Server
from Controllers import PrinterCounter

class InsertPrinter():
    def __init__(self):
        self.db = SQL_Server()
        
        self.printer = ""
        self.ip = ""
    
    def insert_printer(self, ip, desc):
        
        self.ip = ip
        self.printer = desc
        self.printerCounter = PrinterCounter(self.ip)
        self.printCounter = self.printerCounter.getCounterPrint()
        self.copyCounter = self.printerCounter.getCounterCopy()
        self.scannderCounter = self.printerCounter.getCounterScanner()
        self.othersCounter = self.printerCounter.getCounterOther()
        self.totalCounter = self.printerCounter.getCounter()

        query = f"""
        BEGIN
            IF NOT EXISTS (SELECT * FROM Printers 
                    WHERE PrinterIP = '{self.ip}'
                )
            BEGIN
                INSERT INTO Printers(PrinterDesc, PrinterIP, TotalPrint, TotalCopy, TotalScanner, TotalOthers, Total)
                VALUES('{self.printer}', '{self.ip}', {self.printCounter}, {self.copyCounter}, {self.scannderCounter}, {self.othersCounter}, {self.totalCounter})
            END
        END
        """

        self.db.set_data(query)
