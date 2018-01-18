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

# Step 1: Obtain 2D slices from 3D images.
#   A: Extract 2D slices from 3D images with 3DSlicer
#   B: Save the files in a common image format (PNG)
#   C: Check the behaviour and management of the chosen file format (PNG)

# 1.A:  This step is done with the open-source software 3DSlicer, which 
#       they are extracted DICOM files for each slice from. It is explained in
#       the notebook. After this step the user is suppossed to have the
#       following directory structure:
#   .
#   ├── brain_inspect.py
#   ├── computer_vision_notebook_02.ipynb
#   ├── computer_vision_notebook.ipynb
#   ├── datos
#   │   ├── dicom
#   │   │   ├── CSF
#   │   │   │   ├── ...
#   │   │   │   └── IMG0392.dcm
#   │   │   ├── GM
#   │   │   │   ├── ...
#   │   │   │   └── IMG0392.dcm
#   │   │   ├── WM
#   │   │   │   ├── ...
#   │   │   │   └── IMG0392.dcm
#   │   │   └── I3T
#   │   │       ├── ...
#   │   │       └── IMG0392.dcm
#   │   ├── I3TCSF.hdr
#   │   ├── I3TCSF.img
#   │   ├── I3TGM.hdr
#   │   ├── I3TGM.img
#   │   ├── I3T.hdr
#   │   ├── I3T.img
#   │   ├── I3TWM.hdr
#   │   ├── I3TWM.img
#   │   ├── I3T.zip
#   │   └── png
#   │       ├── CSF
#   │       ├── GM
#   │       ├── I3T
#   │       └── WM
#   ├── lib
#   │   ├── dicom_to_png.py
#   │   └── __init__.py
#   └── README.md

# DICOM files are not supported by common visualizer. They are 
# converted to PNG to verify the correct construction of the image. 
# However, as is pointed out in the Notebook, PNG pixels are vector style 
# (redundant vector for grayscale images) while DICOM ones are scalars, thus 
# it is a good choice to process images from DICOM ones.

# 1.B:  This step is done with a simple conversor, mixing SimpleITK and 
#       Matplotlib libraries. It is supposed to convert from dicom to png but
#       it could actually converty to any format supported by Matplotlib.
from lib.dicom_to_png import dicom_to_png

dicom_to_png("datos/dicom/WM/")
dicom_to_png("datos/dicom/GM/")
dicom_to_png("datos/dicom/CSF/")
dicom_to_png("datos/dicom/I3T/")

# 1.C: This step is only expanded in Jupyter Notebook as a complementary
# but strongly suggested inspection

# Step 2: Locate blobs in 2D





















