from sqlalchemy import create_engine

def getConnection():

    server = 'database-sait.czcg0caimnqq.us-east-2.rds.amazonaws.com'
    user = 'admin'
    password = '___Abc999*'
    database = 'data-406-capstone' 
    driver = 'ODBC Driver 17 for SQL Server'

    connection_string = f'mssql+pyodbc://{user}:{password}@{server}/{database}?driver={driver}'

    print(" ")
    print("[Connection String]", connection_string)
    print(" ")

    engine = create_engine(connection_string)

    print(" ")
    print("[Engine_Factory: Server Connection established]")
    print(" ")

    return engine