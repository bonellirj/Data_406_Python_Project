class DataOperations:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def fetch_data(self, query):
        with self.db_connection as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return results

    def execute_command(self, command):
        with self.db_connection as conn:
            cursor = conn.cursor()
            cursor.execute(command)
            conn.commit()