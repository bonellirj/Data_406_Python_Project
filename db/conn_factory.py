import pyodbc


def getConnection():

    SERVER = 'database-sait.czcg0caimnqq.us-east-2.rds.amazonaws.com'
    USER = 'admin'
    PASSWORD = '___Abc999*'
    DATABASE = 'data-406-capstone'  

    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USER};PWD={PASSWORD}'

    conn = pyodbc.connect(connection_string)

    return conn
        