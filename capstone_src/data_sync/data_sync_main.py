# %%
import sys
import os

# project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(project_root)

from step_1_create_tables import setup_data_base_users_dim_tables as setup_data_base_users_dim_tables
from step_1_create_tables import setup_data_base_users_fact_table as setup_data_base_users_fact_table
from step_2_dim_sync import sync_data_base_users_dim_tables as sync_data_base_users_dim_tables

print("Setting up database users")
print(" ")
print("- " * 40)

print("Task 1: Creating DIM tables")
setup_data_base_users_dim_tables()
print(" ")
print("- " * 40)

print("Task 2: Creating FACT tables")
setup_data_base_users_fact_table()
print(" ")
print("- " * 40)

print("Task 3: Syncing DIM tables")
sync_data_base_users_dim_tables()
print(" ")
print("- " * 40)

# print("Task 4: Syncing FACT tables")
# setup_data_base_users_fact_table()
# print(" ")
# print("- " * 40)


# %%
