#!/usr/bin/python
# -*- coding: latin-1
###############################################################################

###############################################################################
## Title:                   brain_inspect.py                                  #
## Author:                  Jose Etxeberria Mendez                            #
## Release date:            19/02/2018                                        #
## Brief description:       Analize brain slices, locate and characterize     #
##                          temporal lobule.                                  #
## Language version:        Python 2.7.12                                     #
## Tested over OS:            Ubuntu 16.04 LTS                                  #
## Tested over processor:   Intel(R) Core(TM) i7-3632QM CPU (x86_64)          #
###############################################################################

###############################################################################
## Large description:                                                         #
##      This file executes secuencially the different commands that together  #
##      form an 3D images inspection and the treatement of their corresponding#
##      2D slices to extract images information. Brain temporal lobule must be# 
##      located and it must be analized the necesity of including domain      # 
##      knowledge in the different vision process description levels.         #
##                                                                            #
## Main steps:                                                                #
##      1 - Obtain 2D slices from 3D images                                   #
##      2 - Locate blobs in 2D                                                #
##      3 - Identify objects in 2D                                            #
##      4 - Characterize turns and grooves of gray matter (GM)                #
###############################################################################
## Notification:    The current program is expanded in a Jupyter Notebook that# 
##                  allows the user to interact with the code in a easy way   #
##                  to achieve a better comprehension. The steps to follow to #
##                  properly execute the notebook, having access to the       #
##                  associated files, are explained in the README.md file of  #
##                  the repository that contains such files and the notebook: #
##                  https://github.com/jetxeberria/computer_vision.git        #
###############################################################################

###############################################################################
## Descripción extendida:                                                     #
##      Este archivo se encarga de la ejecución secuencial de las distintas   #
##      órdenes que en conjunto conforman la inspección de una serie de       #
##      imágenes 3D y el procesamiento de sus cortes 2D correspondientes para #
##      extraer información de las imágenes. Se debe localizar el lobulo      #
##      temporal del cerebro y analizar la necesidad de aporte de conocimiento#
##      del dominio en los distintos niveles de descripción del proceso de    # 
##      visión.                                                               #
##                                                                            #
## Pasos principales:                                                         #
##      1 - Obtención de cortes 2D a partir de imágenes 3D                    #
##      2 - Localización de blobs en 2D                                       #
##      3 - Identificación de objetos en 2D                                   #
##      4 - Caracterización de giros y surcos de la materia gris (GM)         #
###############################################################################
## Notificación:    El presente programa es expandido en un Notebook Jupyter  #
##                  que permite al usuario interactuar con el código de una   #
##                  manera fácil para lograr una mejor comprensión. Los pasos #
##                  a seguir para ejecutar correctamente el notebook, teniendo#
##                  acceso a los ficheros asociados, están explicados en el   #
##                  archivo README.md del repositorio que contiene dichos     #
##                  ficheros y el notebook:                                   #
##                  https://github.com/jetxeberria/computer_vision.git        #
###############################################################################

###############################################################################

# At starting point the user is suppossed to have the following directory 
# structure:
#   .
#   ├── brain_inspect.py
#   ├── computer_vision_notebook_02.ipynb
#   ├── computer_vision_notebook_01.ipynb
#   ├── datos
#   │   ├── I3TCSF.hdr
#   │   ├── I3TCSF.img
#   │   ├── I3TGM.hdr
#   │   ├── I3TGM.img
#   │   ├── I3T.hdr
#   │   ├── I3T.img
#   │   ├── I3TWM.hdr
#   │   ├── I3TWM.img
#   │   └── preprocess
#   │       ├── CSF/
#   │       ├── GM/
#   │       ├── I3T/
#   │       └── WM/
#   ├── lib
#   │   ├── blob_lib.py
#   │   ├── image_manager.py
#   │   ├── imobj_lib.py
#   │   ├── locate_blobs.py
#   │   ├── logger_lib.py
#   │   ├── matter_lib.py
#   │   ├── MRI_inspector.py
#   │   ├── slice_lib.py
#   │   └── __init__.py
#   └── README.md

###############################################################################
##---------------------------------------------------------------------------##
###############################################################################

from matplotlib import pyplot as plt    # Used for image showing
import time                             # Executing time calculator
import numpy as np                      # Used for arrays management
import lib.logger_lib as logger         # Log creation
import lib.MRI_inspector as mri         # 3D objects management
import sys                              # Used to locate file in disk

source_dir = sys.path[0]
plt.rcParams["image.cmap"] = "gray"

# Start log
log = logger.Logger(source_dir+'/evaluation/logs/log.txt')
start_time = time.clock()
log_file_heading = 'File: '+__file__.split('/')[-1]+' '
log_class_heading = log_file_heading+'Class: None '
log_method_heading = log_class_heading+'Method: None ::: '
log.write_log('log',log_method_heading+'Start time: '+str(start_time)\
    +' seconds.')

###############################################################################
##---------------------------------------------------------------------------##
###############################################################################

# Step 1: Obtain 2D slices from 3D images.
#   A: Include data files path and names.
#   B: Make matter objects with the file names and path.
#   C: Read image into matter_objects.
#   D: Preprocess image.
#   E: Make slices objects respect to each matter.
#   F: Save each slice matrix in a common image format. (PNG)
#   G: Check the behaviour and management of PNG. (Only in notebook)

## Step 1.A: Include data files path and names.
inspector = mri.MRI_inspect(log)
inspector.set_files_path(source_dir+'/datos/')
inspector.set_files_names(['I3TWM.hdr','I3TGM.hdr','I3TCSF.hdr','I3T.hdr'])

## Step 1.B: Make matter objects with the file names and path.
inspector.make_matter_objs()

for matter_obj in inspector.matter_obj_list:
    print ('Files processing initialization:')
    ## Step 1.C: Read image into matter_objects.
    print ('Reading file {}...'.format(matter_obj.file_MRI_name))
    matter_obj.read_file()

    ## Step 1.D: Preprocess image.
    print ('Preprocessing 3D image...')
    matter_obj.preprocess()

    print ('Binarizing 3D image...')
    matter_obj.binarize(threshold=80)

    ## Step 1.E: Make slices objects respect to each matter.
    print ('Making slice objects of 3D image...')
    matter_obj.make_slice_objs()
    print ('Done.\n')



## Step 1.F: Save each slice matrix in a common image format. (PNG)
if '-save' in sys.argv:
    for matter_obj in inspector.matter_obj_list:
        print ('Saving slices of matter \'{}\'...'.format(matter_obj.name))
        for slice_obj in matter_obj.slices_obj_list:
            slice_obj.save_slice(source_dir+'/datos/preprocessed/'+matter_obj.name+'/',\
                fext='.png')
        print ('Done.\n')

## Step 1.G: Check the behaviour and management of PNG (Only in notebook)

###############################################################################
##---------------------------------------------------------------------------##
###############################################################################

# Step 2: Locate blobs in 2D
#   A: Segment slices into different blobs by differently labelling them.
#   B: Make blob objects respect to each slice.
#   C: Locate centroids and inner regions for future processing.
#   D: Plot blobs labelled with centroids as label position.

# It is performed blob localization and objects creation for WM, GM and CSF:
print ('Blobs processing:')
for matter_obj in inspector.matter_obj_list[:-2]: 
    print ('Finding blobs of slices of matter {}...'.format(matter_obj.name))
    for slice_obj in matter_obj.slices_obj_list:
        ## Step 2.A: Segment slices into different blobs.
        slice_obj.find_slice_labels()
        ## Step 2.B: Make blob objects respect to each slice
        slice_obj.make_blob_objs()
    print ('Blob objects of each slice are created.')
print ('Done.\n')

## Step 2.C: Locate centroids and inner regions for future processing.
for matter_obj in inspector.matter_obj_list[:-2]:
    print ('Locating centroids and inner regions of blobs of slices of matter '\
        '{}...'.format(matter_obj.name))
    for slice_obj in matter_obj.slices_obj_list:
        for blob_obj in slice_obj.blobs_obj_list:
            blob_obj.find_blob_centroid()
            blob_obj.find_inner_region()
    print ('Centroids and inner regions located.'\
        '{}...'.format(matter_obj.name))
print ('Done.\n')

## Step 2.D: Plot blobs labelled with centroids as label position.
if '-plot' in sys.argv:
    for matter_obj in inspector.matter_obj_list[:-1]:
        print ('Plotting slices labelled of matter \'{}\''\
            '...'.format(matter_obj.name))
        out_plot_dir = source_dir+'/datos/labelled/'+matter_obj.name+'/'
        for slice_obj in matter_obj.slices_obj_list:
            slice_obj.plot_slice_labels(out_plot_dir, f_ext='.png')
        print ('Slices labelled stored at \'{}\'.'.format(out_plot_dir))
    print ('Done.\n')

################################################################################
###---------------------------------------------------------------------------##
################################################################################
#
## Step 3: Identify objects in 2D
##   A: Explicitly name matter objects to ease management
##   B: Make Image Object slices. Each slice stores the slices of all matters.
##   C: Find objects type 1 (GM) by checking their relation with White Matter.
##   D: Make Image Objects type 1 class instances for each found matching blob.
##   E: Find objects type 2 (GM+WM) by checking the relation between themselves.
##   F: Make Image Objects type 2 class instances for each found matching blob.
##   G: Find objects type 3 (GM+WM, global) by checking the relation between
##       themselves and performing blob erosion
##   H: Make Image Objects type 3 class instances for each found matching blob.
#
### Step 3.A: Explicitly name matter objects to ease management
#i3twm, i3tgm, i3tcsf, i3t = inspector.essay_matter_access(inspector.matter_obj_list)
#
### Step 3.B: Make Image Object slices.
print ('Structure image objects information in a classes family')
print ('Making objects \'imobj_slice\' to store in a unique object the slices of '\
    'different matters...')
inspector.make_imobj_slice_objects(inspector.matter_obj_list)
print ('Done.\n')


print ('Finding objects of type \'imobj_type1\' for each \'imobj_slice\'. Each '\
    'object stores a blob that satisfices the type 1 object constraints...')
count=0
for imobj_slice in inspector.imobj_slice_obj_list:
    ## Step 3.C: Find objects type 1 (GM)
    imobj_slice.find_imobjs_type1()
    ## Step 3.D: Make Image Objects type 1
    imobj_slice.make_imobj_objects_type1()
    if len(imobj_slice.type1_imobjs_list) > 0:
        count += 1
print ('{} imslices have objects of type \'imobj_type1\''.format(count))

print ('Finding objects of type \'imobj_type2\' for each \'imobj_slice\'. Each '\
    'object stores a blob pair that satisfices the type 2 object constraints...')
count=0
for imobj_slice in inspector.imobj_slice_obj_list:
    ## Step 3.E: Find objects type 2 (GM+WM)
    imobj_slice.find_imobjs_type2()
    ## Step 3.F: Make Image Objects type 2
    imobj_slice.make_imobj_objects_type2()
    if len(imobj_slice.type2_imobjs_list) > 0:
        count += 1
print ('{} imslices have objects of type \'imobj_type2\''.format(count))
print ('Done.\n')

###############
##########
#####
#slice_proof = inspector.imobj_slice_obj_list[125]
#slice_proof.find_imobjs_type3()
#slice_proof.make_imobj_objects_type3()

#if len(slice_proof.type3_imobjs_list) > 0:
 #   for imobj3 in slice_proof.type3_imobjs_list:
 #       print ('in imslice {} there are a imobj of type {} at position {}'\
 #           .format(imobj3.imslice_number, imobj3.obj_type, imobj3.imobj_position))

#    fig, ax0 = plt.subplots()
#    ax0.imshow(slice_proof.type3_imobjs_list[0].imobj_lbl, cmap='nipy_spectral')
#    ax0.set_title('imobj3-{}_slc{}.imobj_lbl'\
#        .format(slice_proof.type3_imobjs_list[0].imobj_position,\
#        slice_proof.type3_imobjs_list[0].imslice_number))

#if len(slice_proof.type3_imobjs_list) == 2:
#    fig, ax1 = plt.subplots()
#    ax1.imshow(slice_proof.type3_imobjs_list[1].imobj_lbl, cmap='nipy_spectral')
#    ax1.set_title('imobj3-{}_slc{}.imobj_lbl'\
#        .format(slice_proof.type3_imobjs_list[1].imobj_position,\
#        slice_proof.type3_imobjs_list[1].imslice_number))

#plt.show()

#slice_proof.plot_imslice_labels(source_dir+'/datos/labelled_objs/imslice0.png', f_ext='.png')

#####
##########
###############
print ('Finding objects of type \'imobj_type3\' for each \'imslice\'. Each '\
    'object stores a blob pair that satisfices the type 3 object constraints...')
count=0
for imobj_slice in inspector.imobj_slice_obj_list:
    ## Step 3.G: Find objects type 3 (GM+WM, global)
    imobj_slice.find_imobjs_type3()
    ## Step 3.H: Make Image Objects type 3
    imobj_slice.make_imobj_objects_type3()
    if len(imobj_slice.type3_imobjs_list) > 0:
        count += 1
print ('{} imslices have objects of type \'imobj_type3\''.format(count))
print ('Done.\n')

################################################################################
###---------------------------------------------------------------------------##
################################################################################
#
#
###############
##########
#####
if '-plot_objs' in sys.argv:
    print ('Plotting image object slices with blobs of interest labelled...')
    out_plot_dir = source_dir+'/datos/labelled_objs/'
    count=0
    for i, image_slice in enumerate(inspector.imobj_slice_obj_list):
        fill = 4 - len(list(str(i)))
        slice_name = 'imslice'+'0'*fill+str(i)

        if len(image_slice.type1_imobjs_list) > 0 or len(image_slice.type2_imobjs_list)\
                or len(image_slice.type3_imobjs_list):
            image_slice.plot_imslice_labels(out_plot_dir+slice_name, f_ext='.png')
            count+=1
        else:
            slc_shape = image_slice.wm_slice_obj.slc_arr.shape
            image_slice.plot_imslice_labels(out_plot_dir+slice_name, \
                f_ext='.png', shape=slc_shape)
    print ('Image Objects found in {} imslices, labelled and stored at \'{}\''\
        .format(count, out_plot_dir))
    print ('Done.\n')
#####
##########
###############





