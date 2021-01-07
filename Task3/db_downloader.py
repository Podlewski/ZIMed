import requests
import zipfile
import io
import os
from tqdm import tqdm

db_folder = './dcm_files/db'
if not os.path.isdir(db_folder):
    os.mkdir(db_folder)

urls_path = './dcm_files/cq500_files.txt'
with open(urls_path, 'r') as file:
    urls = file.readlines()

for url in tqdm(urls):
    if url[-1] == '\n':
        url = url[:-1]
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(os.path.join(db_folder))
