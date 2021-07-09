"""
DESCRIÇÃO:  FONTE RESPONSÁVEL POR ATUALIZAR OS CONTADORES DAS IMPRESSORAS E 
            DADOS DA IMPRESSÃO POR USUARIO
_____________________________________________________________________________
AUTOR: WILLIAM RODRIGUES
_____________________________________________________________________________
DATA: 08/07/2021

"""






from Models import PrinterDataSQL
from .counter import PrinterCounter
from Models import PageUser
import os, sys
from Error import ErrorLog

def generate_error(error):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    filename = os.path.basename(os.path.dirname(__file__))+"\\"+os.path.basename(__file__)
    
    ErrorLog(
        Error=error,
        Script=filename,
        Line=exc_tb.tb_lineno
    )

class PrinterData():
    def __init__(self, user, upload_folder):
        self.upload_folder = upload_folder
        self.data = PrinterDataSQL()
        self.page = PageUser()
        
        self.user = user
        

    def get_db_data(self, printer, data):
        """
        Irá armazenar as contagens e os dados da impressora no banco de dados
        Params: printer -> Nome padrão do driver da impressora
                data -> json com os dados enviados pelo client.
        """
        try:
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
                filePath = self.upload_folder+"\\"+data['originalFilename']
            
            if(int(self.printCounter) != int(db_data[0].PRINT)):
                """Irá atualizar os dados da impressão por usuario"""

                self.page.set_user_data(
                    UserID=self.user,
                    PrinterID=db_data[0].ID,
                    PagesPrinted=int(self.printCounter) - int(db_data[0].PRINT),
                    Filename=data['originalFilename'],
                    Path=filePath,
                    Time=data['DATE']
                )
                
            self.update_printers(db_data)
        except Exception as e:
            generate_error(e)

    def update_printers(self, db):
        """
        Irá atualizar os dados gerais da Impressora no banco de dados!
        params: db -> dados da impressora obtidos do banco de dados
        """

        try:
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
        except Exception as e:
            generate_error(e)
        
    