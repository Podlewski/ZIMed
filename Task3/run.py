import os
import shutil
import pandas as pd

from flask import Flask, request, Response
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin

from Task3.DICOM_parser import parse_files, image_3D

UPLOAD_FOLDER = r'.\dcm_files\loaded'
ALLOWED_EXTENSIONS = {'dcm'}
IMAGES = pd.DataFrame()
METADATA = pd.DataFrame()
ORDER = []

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 256 * 1024 * 1024  # 256 MB
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # DO NOT CACHE


def get_filename_by_number(number: int) -> str:
    return ORDER[number][0]


@app.route('/metadata/', methods=['GET', 'POST'])
@cross_origin()
def get_dicom_metadata():
    global ORDER
    global METADATA
    global IMAGES
    reset()

    if request.method == 'POST':
        files = request.files
        dic = files.to_dict(flat=False)
        for val in dic:
            dic[val][0].save(os.path.join(UPLOAD_FOLDER, secure_filename(dic[val][0].filename)))
        ORDER, IMAGES, METADATA = parse_files()
    print("Gotowy!")
    return Response(status=200)


@app.route('/obrazki/<int:filenumber>/', methods=['GET'])
@cross_origin()
def get_images(filenumber):
    global IMAGES
    filename = get_filename_by_number(filenumber)
    if not filename:
        return Response(status=404)

    img = IMAGES.loc[filename, 'image']
    return Response(img, status=200, content_type='image/png')


@app.route('/opisy/<int:filenumber>/', methods=['GET'])
@cross_origin()
def get_descriptions(filenumber):
    global METADATA
    filename = get_filename_by_number(filenumber)
    if not filename:
        return Response(status=404)
    meta = METADATA.loc[filename, 'html']
    return Response(meta, status=200, content_type='text/html')


def reset():
    global ORDER
    global METADATA
    global IMAGES
    IMAGES = pd.DataFrame()
    METADATA = pd.DataFrame()
    ORDER = []
    filepath_files = './dcm_files/converted'
    filepath_results = './dcm_files/loaded'
    filepath_3D = './dcm_files/3D'
    try:
        shutil.rmtree(filepath_files, ignore_errors=True)
        shutil.rmtree(filepath_results, ignore_errors=True)
        shutil.rmtree(filepath_3D, ignore_errors=True)
    except OSError as e:
        print("Error deleting %s or %s : %s" % (filepath_results, filepath_files, e.strerror))
        return Response(status=505)

    try:
        os.mkdir(filepath_files)
        os.mkdir(filepath_results)
        os.mkdir(filepath_3D)
    except OSError as e:
        print("Error deleting %s or %s : %s" % (filepath_results, filepath_files, e.strerror))
        return Response(status=506)

    return Response(status=200)


@app.route('/obrazki/3D/', methods=['GET'])
@cross_origin()
def get_3D_view():
    img = image_3D()
    return Response(img, status=200, content_type='image/png')


if __name__ == '__main__':
    reset()
    app.run(debug=True)
