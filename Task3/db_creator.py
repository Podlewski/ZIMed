import requests
import zipfile
import io
import os
import pandas as pd
import pydicom
import shutil
import uuid
import json

from tqdm import tqdm
from termcolor import cprint

if not os.path.isdir('./dcm_files'):
    os.mkdir('./dcm_files')

if not os.path.isdir('./dcm_files/db'):
    os.mkdir('./dcm_files/db')

if not os.path.isdir('./dcm_files/db/described_images'):
    os.mkdir('./dcm_files/db/described_images')


df_initial_manual_labeling = pd.read_excel('./dcm_files/descriptions.xlsx',
                                           usecols=['SOPInstanceUID',
                                                    'SeriesInstanceUID',
                                                    'StudyInstanceUID',
                                                    'labelName'
                                                    ]
                                           )
df_extrapolation_all = pd.read_excel('./dcm_files/descriptions.xlsx',
                                     sheet_name='ExtrapolationToAllSeries',
                                     usecols=['SOPInstanceUID',
                                              'SeriesInstanceUID',
                                              'StudyInstanceUID',
                                              'labelName'
                                              ]
                                     )
df_extrapolation_selected = pd.read_excel('./dcm_files/descriptions.xlsx',
                                          sheet_name='ExtrapolationToSelectedSeries',
                                          usecols=['SOPInstanceUID',
                                                   'SeriesInstanceUID',
                                                   'StudyInstanceUID',
                                                   'labelName'
                                                   ]
                                          )

db_folder = './dcm_files/db'

urls_path = './dcm_files/cq500_files.txt'
with open(urls_path, 'r') as file:
    urls = file.readlines()

temporary_dir = 'temp_dir'
my_description = []


def uid_exists(df: pd.DataFrame, study_instance: str, series_instance: str, sop_instance: str):
    label = df[(df['StudyInstanceUID'] == study_instance) &
               (df['SeriesInstanceUID'] == series_instance) &
               (df['SOPInstanceUID'] == sop_instance)]['labelName']
    if label.shape[0] == 0:
        return None
    ret = label.values[0]
    return ret


def move_file(path: str, db_folder: str, label: str, source_file: str, my_description: list, backup_file, url: str):
    uid = uuid.uuid4()
    new_folder_name = url.split('/')[-1].split('.')[0].lower()
    if not os.path.isdir('./dcm_files/db/described_images/' + new_folder_name):
        os.mkdir('./dcm_files/db/described_images/' + new_folder_name)
    new_path = db_folder + '/described_images/' + new_folder_name + '/' + str(uid) + '.dcm'
    message = {"uuid": str(uid),
               "sop_instance": sop_instance,
               "series_instance": series_instance,
               "study_instance": study_instance,
               "category": label,
               "description_source": source_file}
    backup_file.write(json.dumps(message))
    backup_file.write('\n')
    my_description.append(message)
    shutil.move(path, new_path)


backup_file = open("description_backup.log", "w")

for url in tqdm(urls):
    print(f"\nPrzetwarzam {url}")
    # Remove unnecessary folder
    if os.path.isdir(os.path.join(db_folder, temporary_dir)):
        shutil.rmtree(os.path.join(db_folder, temporary_dir))

    path = db_folder
    # Download zip
    if url[-1] == '\n':
        url = url[:-1]
    try:
        r = requests.get(url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        path += '/' + temporary_dir
        z.extractall(os.path.join(path))
    except Exception as err:
        cprint(f'Plik {url} jest uszkodzony. Błąd: {err}', 'white', attrs=['blink'])
        continue
    print("Zakończono pobieranie pliku zip.")

    # Choose just these file series which are in description
    main_folder_name = os.listdir(path)[0]
    path += '/' + main_folder_name
    path += '/' + 'Unknown Study'
    folders_to_check = os.listdir(path)
    founded = 0
    for folder in folders_to_check:
        fpath = path + '/' + folder
        files = os.listdir(fpath)
        for file in files:
            path_to_file = fpath + '/' + file
            ds = pydicom.filereader.dcmread(path_to_file)
            sop_instance = ds.SOPInstanceUID
            series_instance = ds.SeriesInstanceUID
            study_instance = ds.StudyInstanceUID

            label = uid_exists(df_initial_manual_labeling, study_instance, series_instance, sop_instance)
            if label:
                move_file(path=path_to_file,
                          db_folder=db_folder,
                          label=label,
                          my_description=my_description,
                          source_file='InitialManualLabeling',
                          backup_file=backup_file,
                          url=url)
                founded += 1
                continue
            label = uid_exists(df_extrapolation_all, study_instance, series_instance, sop_instance)
            if label:
                move_file(path=path_to_file,
                          db_folder=db_folder,
                          label=label,
                          my_description=my_description,
                          source_file='ExtrapolationToAllSeries',
                          backup_file=backup_file,
                          url=url)
                founded += 1
                continue
            label = uid_exists(df_extrapolation_selected, study_instance, series_instance, sop_instance)
            if label:
                move_file(path=path_to_file,
                          db_folder=db_folder,
                          label=label,
                          my_description=my_description,
                          source_file='ExtrapolationToSelectedSeries',
                          backup_file=backup_file,
                          url=url)
                founded += 1
                continue
    message = f"Znaleziono {founded} pasujących plików."
    cprint(message, 'yellow')

backup_file.close()

"""
Download time: 8:49:49
"""

my_description_df = pd.DataFrame(my_description)
print(my_description_df.groupby(by='category').count()['uuid'])
"""
category
Chronic             3043
Epidural             341
Intraparenchymal    6257
Intraventricular    2481
Subarachnoid        7468
Subdural            3819
Name: uuid, dtype: int64
"""

df_chronic = my_description_df[my_description_df['category'] == 'Chronic']
df_intraventricular = my_description_df[my_description_df['category'] == 'Intraventricular']
df_intraparenchymal = my_description_df[my_description_df['category'] == 'Intraparenchymal']
df_subarachnoid = my_description_df[my_description_df['category'] == 'Subarachnoid']
df_subdural = my_description_df[my_description_df['category'] == 'Subdural']
df_epidural = my_description_df[my_description_df['category'] == 'Epidural']

df_chronic_sample = df_chronic.sample(frac=1)
df_intraventricular_sample = df_intraventricular.sample(frac=1)
df_intraparenchymal_sample = df_intraparenchymal.sample(frac=0.5)
df_subarachnoid_sample = df_subarachnoid.sample(frac=0.45)
df_subdural_sample = df_subdural.sample(frac=0.85)
df_epidural_sample = df_epidural.sample(frac=1)
frames = [df_epidural_sample, df_subdural_sample, df_subarachnoid_sample, df_intraparenchymal_sample,
          df_intraventricular_sample, df_chronic_sample]
df_balanced = pd.concat(frames)
df_balanced_shuffled = df_balanced.sample(frac=1)
print(df_balanced_shuffled.groupby(by='category').count()['uuid'])
"""
category
Chronic             3043
Epidural             341
Intraparenchymal    3128
Intraventricular    2481
Subarachnoid        3361
Subdural            3246
Name: uuid, dtype: int64
"""

df_balanced_shuffled.to_csv('./dcm_files/my_description_balanced.csv', index=False)
my_description_df.to_csv('./dcm_files/my_description.csv', index=False)