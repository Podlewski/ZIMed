import pydicom
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np


def get_metadata(filename: str, METADATA, IMAGES):
    ds = pydicom.filereader.dcmread(filename)

    fig = plt.figure()
    fig.patch.set_visible(False)

    ax = fig.add_subplot(111)

    plt.axis('off')
    plt.imshow(ds.pixel_array, cmap=plt.cm.seismic)

    extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    filename = filename.split(".")[0].split("/")[-1]
    plt.savefig(f'./dcm_files/converted/{filename}.png', bbox_inches=extent, format='png')

    with open(f'./dcm_files/converted/{filename}.png', 'rb') as image_file:
        # encoded_string = base64.b64encode(image_file.read())
        encoded_string = image_file.read()

    img = encoded_string
    IMAGES.append({"filename": filename, "image": img})
    ds.PixelData = '->'

    df = pd.DataFrame(ds.values())
    df[0] = df[0].apply(lambda x: pydicom.dataelem.DataElement_from_raw(x)
    if isinstance(x, pydicom.dataelem.RawDataElement)
    else x)
    df['name'] = df[0].apply(lambda x: x.name)
    df['value'] = df[0].apply(lambda x: x.value)
    df['tags'] = df[0].apply(lambda x: str(x).split(')')[0].split('(')[1])
    df = df[['tags', 'name', 'value']]
    html = df.to_html(table_id="opisy")
    METADATA.append({"filename": filename, "html": html})
    # return [filename, int(ds.InstanceNumber)]
    return [filename, int(ds.SliceThickness)]


def image_3D():
    path = 'dcm_files/loaded'
    dir_list = os.listdir(path)
    files = []
    for file in dir_list:
        files.append(pydicom.filereader.dcmread(os.path.join(path, file)))

    print("file count: {}".format(len(files)))

    # skip files with no SliceLocation (eg scout views)
    slices = []
    skipcount = 0
    for f in files:
        if hasattr(f, 'SliceLocation'):
            slices.append(f)
        else:
            skipcount = skipcount + 1

    print("skipped, no SliceLocation: {}".format(skipcount))

    # ensure they are in the correct order
    slices = sorted(slices, key=lambda s: s.SliceLocation)

    # pixel aspects, assuming all slices are the same
    ps = slices[0].PixelSpacing
    ss = slices[0].SliceThickness
    ax_aspect = ps[1] / ps[0]
    sag_aspect = ps[1] / ss
    cor_aspect = ss / ps[0]

    # create 3D array
    img_shape = list(slices[0].pixel_array.shape)
    img_shape.append(len(slices))
    img3d = np.zeros(img_shape)

    # fill 3D array with the images from the files
    for i, s in enumerate(slices):
        img2d = s.pixel_array
        img3d[:, :, i] = img2d

    # plot 3 orthogonal slices
    a1 = plt.subplot(2, 2, 1)
    plt.imshow(img3d[:, :, img_shape[2] // 2], cmap=plt.cm.seismic)
    a1.set_aspect(ax_aspect)

    a2 = plt.subplot(2, 2, 2)
    plt.imshow(img3d[:, img_shape[1] // 2, :], cmap=plt.cm.seismic)
    a2.set_aspect(sag_aspect)

    a3 = plt.subplot(2, 2, 3)
    plt.imshow(img3d[img_shape[0] // 2, :, :].T, cmap=plt.cm.seismic)
    a3.set_aspect(cor_aspect)

    plt.savefig(f'./dcm_files/converted/image_3D.png', format='png')

    with open(f'./dcm_files/converted/image_3D.png', 'rb') as image_file:
        encoded_string = image_file.read()
    return encoded_string


def parse_files():
    IMAGES = []
    METADATA = []
    path = 'dcm_files/loaded'
    dir_list = os.listdir(path)
    sets = []
    for file in dir_list:
        metas = get_metadata(filename=f'{path}/{file}', METADATA=METADATA, IMAGES=IMAGES)
        sets.append(metas)
    imgs = pd.DataFrame(IMAGES).set_index('filename')
    meta = pd.DataFrame(METADATA).set_index('filename')
    sets = sorted(sets, key=lambda IS: IS[1])
    return sets, imgs, meta


# Właściwie ta funkcja to całe zadanie na 3
def print_DICOM_in_terminal(filename):
    # Wczytanie metadanych
    ds = pydicom.filereader.dcmread(filename)
    # Rysowanie obrazka
    fig = plt.figure()
    fig.patch.set_visible(False)
    fig.add_subplot(111)
    plt.axis('off')
    plt.imshow(ds.pixel_array, cmap=plt.cm.seismic)
    plt.show()
    print(ds)


# print_DICOM_in_terminal(r'.\dcm_files\example_dicom.dcm')