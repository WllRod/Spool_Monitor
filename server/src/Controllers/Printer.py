from Models import PrinterDataSQL
from .counter import PrinterCounter
from Models import PageUser
from API import app

class PrinterData():
    def __init__(self, user):
        self.data = PrinterDataSQL()
        self.page = PageUser()
        
        self.user = user
        

    def get_db_data(self, printer, data):
        
        db_data = self.data.get_counter(printer, data['IP'])
        self.counter = PrinterCounter(data['IP'])
        self.printCounter = self.counter.getCounterPrint()
        self.copyCounter = self.counter.getCounterCopy()
        self.scannerCount = self.counter.getCounterScanner()
        self.othersCount = self.counter.getCounterOther()
        self.total = self.counter.getCounter()

        filePath = data['FilePath']
        if( not filePath ):
            filePath = "NULL"
        else:
            filePath = app.config['UPLOAD_FOLDER']+"\\"+data['originalFilename']
        if(int(self.printCounter) != int(db_data[0].PRINT)):
            self.page.set_user_data(
                UserID=self.user,
                PrinterID=db_data[0].ID,
                PagesPrinted=int(self.printCounter) - int(db_data[0].PRINT),
                Filename=data['originalFilename'],
                Path=filePath,
                Time=data['DATE']
            )
            
        self.update_printers(db_data)

    def update_printers(self, db):
        db_data = db
        if(int(self.printCounter) == int(db_data[0].PRINT)) and (
            int(self.copyCounter) == int(db_data[0].COPY)
        ) and (
            int(self.scannerCount) == int(db_data[0].SCANNER)
        ) and (
            int(self.othersCount) == int(db_data[0].OTHERS)
        ) and (
            int(self.total) == int(db_data[0].TOTAL)
        ):
            pass
        
            
        else:
            self.data.updateCounter(
                TotalPrint=int(self.printCounter),
                TotalCopy=int(self.copyCounter),
                TotalScanner=int(self.scannerCount),
                TotalOthers=int(self.othersCount),
                Total=int(self.total),
                ID=db_data[0].ID
            )
        
        # for x in db_data:
        #     self.counter = PrinterCounter(data['IP'])
        #     self.newCounter = int(self.counter.getCounter())
        #     self.oldcounter = int(x.COUNTER)
            
        #     self.data.updateCounter(x.ID, self.newCounter)
        
        #     break