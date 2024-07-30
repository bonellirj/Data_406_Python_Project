# %%
import pandas as pd
import sys
import os
import pyodbc
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.engine_factory import getConnection as engine_factory
from db.conn_factory import getConnection as conn_factory


def _insert_csv_to_db(fileName, table_name):

    filepath = '../../data_files/dataset_1_users/'+fileName

    df = pd.read_csv(filepath)
    print("  - ", f"{filepath}: File Loaded")

    try:
        engine = engine_factory()
        connection = engine.connect()
        transaction = connection.begin()
        df.to_sql(table_name, con=connection, if_exists='append', index=False)  
        transaction.commit()
        print("  - ", f"{table_name}: Table Loaded")
    except SQLAlchemyError as e:
        if 'transaction' in locals():
            transaction.rollback()
        print("  - ", f"{table_name}: Fail. Rollback. Error: {str(e)}")
        
    finally:
        if 'connection' in locals():
            connection.close()



def sync_data_base_users_dim_tables():
    _insert_csv_to_db('dim_App_version.csv', 'dw.Dim_Version_Appssss')

 # %%
