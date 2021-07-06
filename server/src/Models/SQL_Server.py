import pyodbc

class SQL_Server:
    def __init__(self):
        self.cnxn = pyodbc.connect(
            'Driver={SQL Server};'
            'Server=192.168.0.101;'
            'Database=CDA;'
            'UID=sa;'
            'PWD=$2@cda101;'
        )
        self.cursor = self.cnxn.cursor()
    
    def set_data(self, query):
        self.cursor.execute(query)
        while self.cursor.nextset():
            pass
        self.cnxn.commit()
    
    def get_data(self, query):
        self.cursor.execute(query)
        q = self.cursor.fetchall()
        return q