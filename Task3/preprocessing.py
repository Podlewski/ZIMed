import os
import pandas as pd
import numpy as np


def find_uuid_in_folders(uuid, all_files):
    for file in all_files:
        filename = file.split('/')[-1].split('.')[0]
        if filename == uuid:
            return file
    return 'a'


fs = []
db_folder = './dcm_files/db'
df = pd.read_csv('dcm_files/my_description_balanced.csv')

paths = np.empty(df.shape[0])
folders = os.listdir(db_folder)
all_files = []
for folder in folders:
    files = os.listdir(os.path.join(db_folder, folder))
    for file in files:
        all_files.append(db_folder + '/' + folder + '/' + file)


df['path'] = df['uuid'].apply(lambda x: find_uuid_in_folders(x, all_files))

df.to_csv('./dcm_files/my_description_balanced_with_path.csv', index=False)