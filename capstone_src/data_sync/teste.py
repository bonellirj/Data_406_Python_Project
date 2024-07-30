import pandas as pd
import sys
import os

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ..db.engine_factory import getConnection as engine_factory

fileName = 'dim_App_version.csv'
table_name = 'dw.Dim_Version_App'

script_dir  = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
filepath = os.path.join(project_root, "data_files", "dataset_1_users", fileName)
filepath = filepath.replace("capstone_src\\","")
print(filepath)

# filepath = '../../data_files/dataset_1_users/'+fileName

df = pd.read_csv(filepath)
print("  - ", f"{filepath}: File Loaded")

engine = engine_factory()

print("Engine: ",engine)

df.to_sql(table_name, con=engine, if_exists='append', index=False)

print("  - ", f"{table_name}: Table Loaded")