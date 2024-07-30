import pyodbc
from database_operations import DataOperations as DataOperations

class DatabaseConnection:
    
    def __init__(self):
        
        SERVER = 'database-sait.czcg0caimnqq.us-east-2.rds.amazonaws.com'
        USER = 'admin'
        PASSWORD = '___Abc999*'
        DATABASE = 'data-406-capstone'  

        connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USER};PWD={PASSWORD}'
        print(connection_string)
    
        self.connection_string = connection_string
        self.conn = None

    def __enter__(self):
        self.conn = pyodbc.connect(self.connection_string)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
            
    def getConnectionString(self):
        return self.connection_string 
    
    def getConnection(self):
        return self.__enter__()



# Usage example
def main():
    
    db_conn = DatabaseConnection().getConnection()
    data_op = DataOperations(db_conn)

    query = "SELECT TOP 10 * FROM dbo.AllSessions"
    results = data_op.fetch_data(query)
    for row in results:
        print(row)

    # Example of executing a command
    # command = "UPDATE Users SET name = 'John' WHERE id = 1"
    # data_op.execute_command(command)

if __name__ == "__main__":
    main()
