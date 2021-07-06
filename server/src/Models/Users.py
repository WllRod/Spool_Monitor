from Models.SQL_Server import SQL_Server

class InsertUser():
    def __init__(self):
        self.db = SQL_Server()
        self.user = ""
    def insert_user(self, user):
        self.user = user
        
        query = f"""
        BEGIN
            IF NOT EXISTS (SELECT * FROM USERS 
                    WHERE UserDesc = '{user}'
                )
            BEGIN
                INSERT INTO Users SELECT '{user}', 0
            END
        END
        """
        
        self.db.set_data(query)
        return self.get_user_id()

    def get_user_id(self):
        query = f"""
        SELECT UserID AS "ID" FROM USERS WHERE UserDesc='{self.user}'
        """

        return self.db.get_data(query)