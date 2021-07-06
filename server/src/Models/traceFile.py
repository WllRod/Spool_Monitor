from Models.SQL_Server import SQL_Server

def returnTraceFile(user):
    sql = SQL_Server()

    query = f"""
    SELECT 
        TraceFile AS "Tracer"
    FROM
        USERS
    WHERE
        UserDesc='{user}'
    """

    response = sql.get_data(query)
    if(response[0].Tracer == 1):
        return True
    else:
        return False