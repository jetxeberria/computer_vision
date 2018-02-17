from skimage import measure as msr          # To measure region props
from inspect import stack                   # To write log
import numpy as np
import matter_lib as matt
import slice_lib as slc
import blob_lib as blb
import imobj_lib as imobj


log_file_heading = 'File: '+__file__.split('/')[-1]+' '

class Structure(object):
    
    def __init__(self, log):
        self.log = log
        self.log_class_heading = log_file_heading+"Class: "\
            +self.__class__.__name__
        log_method_heading = self.log_class_heading+" Method: "+stack()[0][3]\
            +" ::: "
        self.log.write_log("log",log_method_heading+"Initialization called")


    def create_matter_objs(self, fpath, fnames):
        '''
        Returns the list cointaining the result of creating a object of class 
        'Matter' for each pointed file.

        Parameters:
                    fpath:          <str>
                                    Path to files directory.
                                    /path/to/directory/

                    fnames:         <list>
                                    List with the names of files. 
                                    ['filename.extension',...] 

        Returns:
                    matters_list:   <list>
                                    List of objects of class 'Matter' created. 
        '''
        matters_list = []
        for name in fnames:
            matter_obj = matt.Matter(self.log, fpath, name, self)
            matters_list.append(matter_obj)

        return matters_list

    def create_slice_objs(self, image_3d, mat_name):
        '''
        Returns the list cointaining the result of creating objects of class 
        'Slice'. There is an object for each slice of the given 'image_3d' image.

        Parameters:
                    image_3d:       <numpy.ndarray>
                                    3d array image from whose slices are created
                                    the 'Slice' class objects.
                    mat_name:       <str>
                                    Name to be set as attribute of the object.

        Returns:
                    slices_list:    <list>
                                    A list of the objects created of class
                                    'Matter'.
        '''
        slices_list = []
        for i in range(image_3d.shape[2]):
            slice_i = image_3d[...,i]
            fill = 4 - len(list(str(i)))
            slice_name = 'slice'+'0'*fill+str(i)
            slice_obj = slc.Slice(self.log, slice_i, slice_name, mat_name, self)
            slices_list.append(slice_obj)

        return slices_list

    def create_blob_objs(self, labelled_slice, slice_number, slice_kind):
        '''
        Returns the list cointaining the result of creating objects of class 
        'Blob'. There is an object for each blob found in the given 
        'labelled_slice' image.

        Parameters:
                    labelled_slice:           <numpy.ndarray>
                                    2d image differently labelled for each blob.
                    slice_number:           <int>
                                    Number of slice. 
                    slice_kind:           <str>
                                    Matter kind of the object

        Returns:
                    blobs_list:           <list>
                                    A list of the objects created of class
                                    'Blob'.
        '''
        blobs_list = []
        blob_props_list = msr.regionprops(labelled_slice)# [1:]  Exclude background
        for blob_props in blob_props_list:
            mask = labelled_slice == blob_props.label
            mask = mask.astype(np.int)
            blob_obj = blb.Blob(self.log, mask, slice_number, blob_props,\
                slice_kind)
            blobs_list.append(blob_obj)

        return blobs_list

    def create_imobj_slice_objs(self, matter_list):
        '''
        Returns the list cointaining the result of creating objects of class 
        'ImageObjectSlice'. Each object is conformed by the slices of all
        matters and there are as many objects as slices are extracted from each 
        matter.

        Parameters:
                    matter_list:           <list>
                                    List of objects of class 'Matter'

        Returns:
                    imobj_slices_list:           <list>
                                    List of objects of clas 'ImageObjectSlice' 
        '''
        wm = matter_list[0]
        gm = matter_list[1]
        csf = matter_list[2]
        i3t = matter_list[3]

        imobj_slices_list = []
        for wm_slc, gm_slc, csf_slc, i3t_slc in zip(wm.slices_obj_list, \
                gm.slices_obj_list, csf.slices_obj_list, \
                i3t.slices_obj_list):
            imobj_slice_obj = imobj.ImageObjectSlice(self.log, wm_slc, gm_slc,\
                csf_slc, i3t_slc, self)
            imobj_slices_list.append(imobj_slice_obj)

        return imobj_slices_list

    def create_imobj_objects_type1(self, blob1_list):
        '''
        Returns the list cointaining the result of creating objects of class 
        'ImageObject1'. Each object is conformed by each blob stored in 
        'blob1_list'.

        Parameters:
                    blob1_list:           <list>
                                    List of objects of class 'Blob' that match
                                    the constraints of Image Object type 1.

        Returns:
                    imobj1_list:           <list>
                                    List of objects of class 'ImageObject1'. 
        '''
        imobj1_list = []
        for num, blob1 in enumerate(blob1_list):
            imobj1_obj = imobj.ImageObject1(self.log, blob1, num)
            imobj1_list.append(imobj1_obj)

        return imobj1_list

    def create_imobj_objects_type2(self, blobs2_list):
        '''
        Returns the list cointaining the result of creating objects of class 
        'ImageObject2'. Each object is conformed by each pair of blobs stored in 
        'blob2_list'.

        Parameters:
                    blobs2_list:     <tuple>
                                    Paired lists of objects of class 'Blob' that
                                    match the constraints of Image Object type 2.

        Returns:
                    imobj2_list:     <list>
                                    List of objects of class 'ImageObject2'. 
        '''

        imobj2_list = []
        for num, blobs2 in enumerate(zip(*blobs2_list)):
            imobj2_obj = imobj.ImageObject2(self.log, blobs2, num)
            imobj2_list.append(imobj2_obj)

        return imobj2_list

    def create_imobj_objects_type3(self, blobs3_list):
        '''
        Returns the list cointaining the result of creating objects of class 
        'ImageObject3'. Each object is conformed by each pair of blobs stored in 
        'blob3_list'. Blobs are differentiated according to their position as 
        'left' or 'right'.

        Parameters:
                    blobs3_list:     <tuple>
                                    Paired lists of objects of class 'Blob' that
                                    match the constraints of Image Object type 3.

        Returns:
                    blobs3_list:     <list>
                                    List of objects of class 'ImageObject3'. 
        '''
        wm_blobs3 = blobs3_list[0]
        gm_blobs3 = blobs3_list[1]
        left_blobs = ([], [])
        right_blobs = ([], [])
        for wm_blob3 in wm_blobs3:
            if (wm_blob3.blob_ctrd[1] < 150):
                left_blobs[0].append(wm_blob3)

            elif (wm_blob3.blob_ctrd[1] > 200):
                right_blobs[0].append(wm_blob3)

        for gm_blob3 in gm_blobs3:
            if (gm_blob3.blob_ctrd[1] < 150):
                left_blobs[1].append(gm_blob3)

            elif (gm_blob3.blob_ctrd[1] > 200):
                right_blobs[1].append(gm_blob3)

        imobj3_list = []
        if len(left_blobs[1])!=0:    # This means that there is at least a GM blob
            imobj3_list.append(imobj.ImageObject3(self.log, left_blobs, 'left'))

        if len(right_blobs[1])!=0:   # This means that there is at least a GM blob
            imobj3_list.append(imobj.ImageObject3(self.log, right_blobs, 'right'))

        return imobj3_list
        

