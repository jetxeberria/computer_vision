from matplotlib import pyplot as plt, image as img
import SimpleITK as sitk
import os

def dicom_to_png(dicom_dir, out_fext='.png'):
    plt.rcParams['image.cmap'] = 'gray'

    out_dir = dicom_dir[:dicom_dir.find('/dicom')+1]+out_fext[1:]\
        +dicom_dir[dicom_dir.find('dicom/')+5:]


    # DICOM Reader
    print ('Reading Dicom directory: ', dicom_dir)
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(dicom_dir)
    reader.SetFileNames(dicom_names)
    image = reader.Execute()

    size = image.GetSize()

    # PNG Writer
    for i in range(size[2]):
        slice_i = sitk.GetArrayFromImage(image[:,:,i])
        out_fname = out_dir\
            +dicom_names[i][dicom_names[i].rfind('/'):dicom_names[i].find('.')]\
            +out_fext
        img.imsave(out_fname, slice_i)


