# %%
import pandas as pd
import os

columns = [
    'User', 'Session #', 'Session duration', 'App version', 'Country', 'Crashes', 'Device', 
    'Device class', 'Device time', 'Display height', 'Display width', 'Distinct screens', 
    'Events', 'Gestures', 'City', 'OS version', 'Platform', 'Rage gestures', 'Screen visits', 
    'Session ID', 'Upload time', 'Custom label'
]
files = [
    '../../../data_files/sessions_01.csv', '../../../data_files/sessions_02.csv', '../../../data_files/sessions_03.csv',
    '../../../data_files/sessions_04.csv', '../../../data_files/sessions_05.csv', '../../../data_files/sessions_06.csv',
    '../../../data_files/sessions_07.csv', '../../../data_files/sessions_08.csv', '../../../data_files/sessions_09.csv',
    '../../../data_files/sessions_10.csv', '../../../data_files/sessions_11.csv', '../../../data_files/sessions_12.csv'
]

def process_file(file_path, output_dir):

    df = pd.read_csv(file_path, delimiter=',')
    df = df[columns]
    
    output_path = os.path.join(output_dir, os.path.basename(file_path))
    
    df.to_csv(output_path, sep=';', index=False)

# Diretório de saída
output_dir = '../../../data_files/output_directory'
os.makedirs(output_dir, exist_ok=True)

# Processar todos os arquivos
for file in files:
    process_file(file, output_dir)

print("Todos os arquivos foram processados e salvos com delimitador ponto-e-vírgula.")
# %%
