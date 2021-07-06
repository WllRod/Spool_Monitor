from Models.SQL_Server import SQL_Server

class PageUser():
    def __init__(self):
        self.db = SQL_Server()

    def set_user_data(self, **kwargs):
        min = 1
        max = len(kwargs)
        
        text = ""
        for keys, values in kwargs.items():
            if(min < max):
                text += "'"+str(values)+"',"
            else:
                text += "'"+str(values)+"'"
            min = min + 1
        query = f'INSERT INTO PAGES_PER_USER SELECT {text}'
        self.db.set_data(query)