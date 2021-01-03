import pydicom
import matplotlib.pyplot as plt

filepath = 'CT000238.dcm'
ds = pydicom.filereader.dcmread(filepath)
print(ds)

plt.imshow(ds.pixel_array, cmap=plt.cm.seismic)
plt.show()