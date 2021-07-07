import pyodbc
from .config import return_config

class SQL_Server:
    def __init__(self):
        config = return_config()
        print(config)
        self.cnxn = pyodbc.connect(
            'Driver={SQL Server};'
            'Server=%s;'
            'Database=%s;'
            'UID=%s;'
            'PWD=%s;' % (
                config['Server'], 
                config['Database'], 
                config['DBUser'], 
                config['DBPassword']
            )
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