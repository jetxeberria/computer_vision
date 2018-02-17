from inspect import stack                   # To write log
import locate_blobs as loc                  # Locate blobs functions
import numpy as np
from matplotlib import pyplot as plt

log_file_heading = 'File: '+__file__.split('/')[-1]+' '

class ImageObject1(object):
    blob = None
    imobj_lbl = None
    obj_type = 0
    imslice_number = 0
    imobj_number = 0
    
    def __init__(self, log, blob1, num):
        self.log = log
        self.log_class_heading = log_file_heading+"Class: "\
            +self.__class__.__name__
        log_method_heading = self.log_class_heading+" Method: "+stack()[0][3]\
            +" ::: "
        self.log.write_log("log",log_method_heading+"Initialization called")

        self.obj_type = 1
        self.blob = blob1
        self.imslice_number = self.blob.slice_number
        self.imobj_number = num
        self.imobj_lbl = self.blob.blob_mask

class ImageObject2(object):
    blob_gm = None
    blob_wm = None
    imobj_lbl = None
    obj_type = 0
    imslice_number = 0
    imobj_number = 0

    def __init__(self, log, blob2, num):
        self.log = log
        self.log_class_heading = log_file_heading+"Class: "\
            +self.__class__.__name__
        log_method_heading = self.log_class_heading+" Method: "+stack()[0][3]\
            +" ::: "
        self.log.write_log("log",log_method_heading+"Initialization called")

        self.obj_type = 2
        self.blob_wm = blob2[0]
        self.blob_gm = blob2[1]
        self.imslice_number = self.blob_wm.slice_number
        self.imobj_number = num
        blobs2_lbl = np.zeros(blob2[0].blob_mask.shape)
        blobs2_lbl[blob2[0].blob_mask > 0] = 2 # num*2+1  # Starts at 0
        blobs2_lbl[blob2[1].blob_mask > 0] = 3 # num*2+2
        self.imobj_lbl = blobs2_lbl

class ImageObject3(object):
    blobs_gm = None
    blobs_wm = None
    imobj_lbl = None
    obj_type = 0
    imslice_number = 0
    imobj_position = ''

    def __init__(self, log, blobs3, position):
        self.log = log
        self.log_class_heading = log_file_heading+"Class: "\
            +self.__class__.__name__
        log_method_heading = self.log_class_heading+" Method: "+stack()[0][3]\
            +" ::: "
        self.log.write_log("log",log_method_heading+"Initialization called")

        self.obj_type = 3
        self.blobs_wm = blobs3[0]
        self.blobs_gm = blobs3[1]
        self.imslice_number = self.blobs_gm[0].slice_number
        self.imobj_position = position

        blobs3_lbl = np.zeros(self.blobs_gm[0].blob_mask.shape)

        for blob in self.blobs_wm:
            blobs3_lbl[blob.blob_mask > 0] = 2 # num*2+1  # Starts at 0

        for blob in self.blobs_gm:
            blobs3_lbl[blob.blob_mask > 0] = 3 # num*2+2

        self.imobj_lbl = blobs3_lbl


class ImageObjectSlice(object):
    wm_slice_obj = None
    gm_slice_obj = None
    csf_slice_obj = None
    i3t_slice_obj = None
    type1_blobs = []
    type2_blobs_gm = []
    type2_blobs_wm = []
    type3_blobs_gm = []
    type3_blobs_wm = []
    type1_imobjs_list = []
    type2_imobjs_list = []
    type3_imobjs_list = []
    imslice_num = 0
    
    def __init__(self, log, wm_slice, gm_slice, csf_slice, i3t_slice, stct):
        self.log = log
        self.log_class_heading = log_file_heading+"Class: "\
            +self.__class__.__name__
        log_method_heading = self.log_class_heading+" Method: "+stack()[0][3]\
            +" ::: "
        self.log.write_log("log",log_method_heading+"Initialization called")
        self.wm_slice_obj = wm_slice
        self.gm_slice_obj = gm_slice
        self.csf_slice_obj = csf_slice
        self.i3t_slice_obj = i3t_slice
        self.imslice_num = wm_slice.slc_number
        self.loc = loc.Locate_blobs(self.log)
        self.stct = stct

    def find_imobjs_type1(self, wm_slice=None, gm_slice=None):
        '''
        Stores as an attribute a list with the candidate blobs of type 1.
        By default takes self object attributes.

        Parameters:
                    wm_slice:       <lib.slice_lib.Slice>
                                    Object 'Slice' of matter 'wm'.
                    gm_slice:       <lib.slice_lib.Slice>
                                    Object 'Slice' of matter 'gm'.

        Updates object atributes:
                    type1_blobs:    <list>
                                    List of objects of class 'Blob' of gray 
                                    matter that matchs the constraints to 
                                    conform an object of class 'ImageObjects1' 
                                    (Image Object of type 1).
        '''
        if wm_slice is None:
            wm_slice = self.wm_slice_obj
        if gm_slice is None:
            gm_slice = self.gm_slice_obj

        blobs1 = self.loc.characterize_blobs_type1(wm_slice.blobs_obj_list,\
                gm_slice.blobs_obj_list)
        self.type1_blobs = blobs1

    def find_imobjs_type2(self, wm_slice=None, gm_slice=None):
        '''
        Stores as attributes paired lists with the candidate blobs of type 2 of 
        each matter. 
        By default takes self object attributes.

        Parameters:
                    wm_slice:       <lib.slice_lib.Slice>
                                    Object 'Slice' of matter 'wm'.
                    gm_slice:       <lib.slice_lib.Slice>
                                    Object 'Slice' of matter 'gm'.

        Updates object atributes:
                    type2_blobs_wm:  <list>
                                    List of objects of class 'Blob' of white matter
                    type2_blobs_gm:  <list>
                                    List of objects of class 'Blob' of gray matter
        '''
        if wm_slice is None:
            wm_slice = self.wm_slice_obj
        if gm_slice is None:
            gm_slice = self.gm_slice_obj

        blobs2 = self.loc.characterize_blobs_type2(wm_slice.blobs_obj_list,\
                gm_slice.blobs_obj_list)
        if len(blobs2) > 0:
            self.type2_blobs_wm = blobs2[0]
            self.type2_blobs_gm = blobs2[1]

        else:
            self.type2_blobs_wm = []
            self.type2_blobs_gm = []

    def find_imobjs_type3(self, wm_slice=None, gm_slice=None):
        '''
        Stores as an attribute a list with the candidate blobs of type 3. First 
        locate candidate regions of blobs. Then, they are created 'Blob' objects
        using selected regions. From this point, the process is similar as 
        previous image objects finding, characterizing candidate blobs of 
        type 3.
        By default takes self object attributes.

        Parameters:
                    wm_slice:       <lib.slice_lib.Slice>
                                    Object 'Slice' of matter 'wm'.
                    gm_slice:       <lib.slice_lib.Slice>
                                    Object 'Slice' of matter 'gm'.

        Updates object atributes:
                    type3_blobs_wm:  <list>
                                    List of objects of class 'Blob' of white 
                                    matter.
                    type3_blobs_gm:  <list>
                                    List of objects of class 'Blob' of gray 
                                    matter.
        '''
        if wm_slice is None:
            wm_slice = self.wm_slice_obj
        if gm_slice is None:
            gm_slice = self.gm_slice_obj

        # If there is no blob of GM in this slice, there is no 
        # imobject type 3, and 'type3_blobs_gm' and 'type3_blobs_wm' return a 
        # empty list.
        new_wm_lbls = []
        new_gm_lbls = []
        if len(gm_slice.blobs_obj_list) > 0:
            # Estimate regions and extract the labelled images
            new_wm_lbls, new_gm_lbls = \
                self.loc.find_candidate_regions_type3(wm_slice, gm_slice)

        region_wm_blobs = []
        if len(new_wm_lbls) > 0:
            # Create 'Blob' objects with the new blobs stored in the labelled images
            region_wm_blobs = self.stct.create_blob_objs(new_wm_lbls, \
                self.imslice_num, wm_slice.matter_kind)
            for blob in region_wm_blobs:
                blob.find_blob_centroid()

        region_gm_blobs = []
        if len(new_gm_lbls) > 0:
            region_gm_blobs = self.stct.create_blob_objs(new_gm_lbls, \
                self.imslice_num, gm_slice.matter_kind)
            for blob in region_gm_blobs:
                blob.find_blob_centroid()
        
        # Evaluate which blobs are of type 3.
        blobs3 = []
        if len(region_gm_blobs) > 0:
            blobs3 = self.loc.characterize_blobs_type3(region_wm_blobs, \
                region_gm_blobs, wm_slice, gm_slice)

        if len(blobs3) > 0:
            
            if len(blobs3) == 2:
                self.type3_blobs_wm = blobs3[0]
                self.type3_blobs_gm = blobs3[1]
            elif len(blobs3) == 1:
                self.type3_blobs_gm = blobs3[0]
        
        else:
            self.type3_blobs_wm = []
            self.type3_blobs_gm = []

    def make_imobj_objects_type1(self, blobs_type1=None):
        '''
        Stores as an attribute a list of the objects created of class 
        'ImageObject1'. Each objecty is conformed by each blob stored in 
        'blobs_type1' that are GM blobs previously considered to be of such type.
        By default takes self object attributes.

        Parameters:
                    blobs_type1:       <list>
                                    List of objects of class 'Blob' that match
                                    the constraints of Image Object type 1.

        Updates object atributes:
                    type1_imobjs_list: <list>
                                    List of objects of class 'ImageObject1'.
        '''
        if blobs_type1 is None:
            blobs_type1 = self.type1_blobs

        if len(blobs_type1) == 0:
            self.type1_imobjs_list = []
        else:
            self.type1_imobjs_list = self.stct.create_imobj_objects_type1(blobs_type1)

    def make_imobj_objects_type2(self, blobs_type2=None):
        '''
        Stores as an attribute a list of the objects created of class 
        'ImageObject2'. Each objecty is conformed by each blob stored in 
        'blobs_type2' that are GM blobs previously considered to be of such type.
        By default takes self object attributes.

        Parameters:
                    blobs_type2:           <tuple>
                                    Paired lists of objects of type 'Blob' 
                                    of gray and white matter that match the 
                                    constraints to be an object of class 
                                    'ImageObject2'.
                                    (wm_blobs, gm_blobs)

        Updates object atributes:
                    type2_imobjs_list: <list>
                                    List of objects of class 'ImageObject2'. 
        '''
        if blobs_type2 is None:
            blobs_type2 = (self.type2_blobs_wm, self.type2_blobs_gm)

        if len(blobs_type2[0]) == 0:
            self.type2_imobjs_list = []
        else:
            self.type2_imobjs_list = self.stct.create_imobj_objects_type2(blobs_type2)

    def make_imobj_objects_type3(self, blobs_type3=None):
        '''
        Stores as an attribute a list of the objects created of class 
        'ImageObject3'. Each objecty is conformed by each blob stored in 
        'blobs_type3' that are GM blobs previously considered to be of such type.
        By default takes self object attributes.

        Parameters:
                    blobs_type3:           <tuple>
                                    Paired lists of objects of class 'Blob', of 
                                    white and gray matter respectively, that 
                                    match the constraints to conform 
                                    objects of class 'ImageObjects3' (Image 
                                    Object of type 3).

        Updates object atributes:
                    type3_imobjs_list:           <list>
                                    List of objects of class 'ImageObject3'. 
        '''
        if blobs_type3 is None:
            blobs_type3 = (self.type3_blobs_wm, self.type3_blobs_gm)

        if len(blobs_type3[1]) == 0:
            self.type3_imobjs_list = []
        else:
            self.type3_imobjs_list = self.stct.create_imobj_objects_type3(blobs_type3)


    def plot_imslice_labels(self, o_path, t1_imobjs=None, t2_imobjs=None, \
            t3_imobjs=None, f_ext='.png', shape=None):
        '''
        Plots the blobs of the three types found in the slices in a file in 
        'o_path' with extension 'f_ext'.
        By default takes self object attributes.

        Parameters:
                    o_path:           <str>
                                    Output path of the plots.
                    t1_imobjs:           <list>
                                    List of objects of class 'ImageObject1'. 
                    t2_imobjs:           <list>
                                    List of objects of class 'ImageObject2'. 
                    t3_imobjs:           <list>
                                    List of objects of class 'ImageObject3'. 
                    f_ext:           <str>
                                    Extension of the output file.
                    shape:           <tuple>
                                    Dimensions of the slice for the cases with
                                    no object of no type.

        Output:
                    Image file stored at 'o_path'.
        '''
        if t1_imobjs is None:
            t1_imobjs = self.type1_imobjs_list
        if t2_imobjs is None:
            t2_imobjs = self.type2_imobjs_list
        if t3_imobjs is None:
            t3_imobjs = self.type3_imobjs_list

        if len(t1_imobjs) > 0:
            shape = t1_imobjs[0].imobj_lbl.shape
        elif len(t2_imobjs) > 0:
            shape = t2_imobjs[0].imobj_lbl.shape
        elif len(t3_imobjs) > 0:
            shape = t3_imobjs[0].imobj_lbl.shape

        # Merge the labelled masks of the image objects of type 1
        type1_blobs_lbls = np.zeros(shape)
        if len(t1_imobjs) > 0:
            # For each image object merge its labelled mask
            for type1_im in t1_imobjs:
                type1_blobs_lbls = type1_im.imobj_lbl + type1_blobs_lbls

        # Merge the labelled masks of the objects of type 2
        type2_blobs_lbls = np.zeros(shape)
        if len(t2_imobjs) > 0:
            # For each image object merge its labelled mask
            for type2_im in t2_imobjs:
                type2_blobs_lbls = type2_im.imobj_lbl + type2_blobs_lbls

        # Merge the labelled masks of the objects of type 3
        type3_blobs_lbls = np.zeros(shape)
        if len(t3_imobjs) > 0:
            # For each image object merge its labelled mask
            for type3_im in t3_imobjs:
                type3_blobs_lbls = type3_im.imobj_lbl + type3_blobs_lbls

        all_blobs_lbls = type1_blobs_lbls + type2_blobs_lbls + type3_blobs_lbls

        blobs1 = []
        for imobj1 in t1_imobjs:
            blobs1.append(imobj1.blob)

        blobs2 = []
        for imobj2 in t2_imobjs:
            blobs2.append((imobj2.blob_wm, imobj2.blob_gm))

        blobs3 = []
        for imobj3 in t3_imobjs:
            blobs3.append((imobj3.blobs_wm, imobj3.blobs_gm, imobj3.imobj_position))

        self.loc.plot_labels(o_path+f_ext, all_blobs_lbls, blobs1, blobs2, blobs3)


