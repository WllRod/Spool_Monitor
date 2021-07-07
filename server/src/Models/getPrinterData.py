from Models.SQL_Server import SQL_Server

class PrinterDataSQL():
    def __init__(self):
        self.db = SQL_Server()
    
    def get_counter(self, printer, ip):
        query = f"""
        SELECT
            P.PrinterID AS "ID",
            P.PrinterDesc AS "DESC",
            P.PrinterIP AS "IP",
            P.TotalPrint AS "PRINT",
            P.TotalCopy AS "COPY",
            P.TotalScanner AS "SCANNER",
            P.TotalOthers AS "OTHERS",
            P.Total AS "TOTAL",
            P.PrinterSectionID AS "SECTION"
        FROM PRINTERS P
        
        WHERE P.PrinterDesc='{printer}' AND P.PrinterIP='{ip}'

        """
        print(query)
        return self.db.get_data(query)

    def updateCounter(self, **kwargs):
        query = f"""
        UPDATE 
            Printers 
        SET 
            TotalPrint={kwargs['TotalPrint']},
            TotalCopy={kwargs['TotalCopy']},
            TotalScanner={kwargs['TotalScanner']},
            TotalOthers={kwargs['TotalOthers']},
            Total={kwargs['Total']}
        WHERE 
            PrinterID='{kwargs['ID']}'
        """
        self.db.set_data(query)