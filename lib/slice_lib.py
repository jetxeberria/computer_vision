from inspect import stack                   # To write log
from matplotlib import image as im      # Read images
import locate_blobs as loc          # Locate blobs functions


log_file_heading = 'File: '+__file__.split('/')[-1]+' '

class Slice(object):

    slc_arr = None
    slc_name = ''
    slc_lbl = None
    lbls_num = 0
    blobs_obj_list = []
    slc_number = None
    matter_kind = ''
    
    def __init__(self, log, slice_2d, slice_name, matter_name, stct):
        self.log = log
        self.log_class_heading = log_file_heading+"Class: "\
            +self.__class__.__name__
        log_method_heading = self.log_class_heading+" Method: "+stack()[0][3]\
            +" ::: "
        self.log.write_log("log",log_method_heading+"Initialization called")

        self.slc_arr = slice_2d
        self.slc_name = slice_name
        self.matter_kind = matter_name
        self.slc_number = int(slice_name[slice_name.find('slice')+5:])
        self.stct = stct
        self.loc = loc.Locate_blobs(self.log)

    def save_slice(self, out_path, fext='.png'):
        '''
        Stores as an attribute the result of
        By default takes self object attributes.

        Parameters:
                    out_path:           <classtype>
                                    description
                    fext:           <classtype>
                                    description
        '''

        raw_input('out_path: type: {}'.format(type(out_path)))
        raw_input('fext: type: {}'.format(type(fext)))

        im.imsave(out_path+self.slc_name+fext, self.slc_arr)

    def find_slice_labels(self, img_slice=None):
        '''
        Stores as attributes the list and number resulting of finding labels of
        the 2d image pointed by 'img_slice'. 
        By default takes self object attributes.

        Parameters:
                    img_slice:           <numpy.ndarray>
                                    2d image to find labels from.

        Updates object atributes:
                    slc_lbl:           <numpy.ndarray>
                                    Array differently labelled for each blob. 
                                    Has the same shape as input array.
                    lbls_num:           <int>
                                    Number of different blobs found. 
        '''
        if img_slice is None:
            img_slice = self.slc_arr

        self.slc_lbl, self.lbls_num = self.loc.find_labels(img_slice)

    def make_blob_objs(self, slice_labelled=None, slc_n=None, mat_knd=None):
        '''
        Stores as an attribute the result of using the 2d array pointed by 
        'slice_labelled' to create objects of class 'Blob'.
        By default takes self object attributes.

        Parameters:
                    slice_labelled: <numpy.ndarray>
                                    Array differently labelled for each blob. 
                    slc_n:           <int>
                                    Number of slice. 
                    mat_knd:         <str>
                                    Matter kind of the object

        Updates object atributes:
                    blobs_obj_list:  <list>
                                    List of objects of class 'Blob'. 
        '''
        if slice_labelled is None:
            slice_labelled = self.slc_lbl
        if slc_n is None:
            slc_n = self.slc_number
        if mat_knd is None:
            mat_knd = self.matter_kind

        if self.lbls_num == 0:
            self.blobs_obj_list = []
        else:
            self.blobs_obj_list = self.stct.create_blob_objs(slice_labelled, slc_n,\
                mat_knd)

    def plot_slice_labels(self, o_path, slic=None, blob_objs=None, f_ext='.png'):
        '''
        Stores as an attribute the result of
        By default takes self object attributes.

        Parameters:
                    o_path:           <classtype>
                                    description
                    slic:           <classtype>
                                    description
                    blob_objs:           <classtype>
                                    description
                    f_ext:           <classtype>
                                    description

        Updates object atributes:
                    None
        '''
        if slic is None:
            slic = self.slc_lbl
        if blob_objs is None:
            blob_objs = self.blobs_obj_list

        raw_input('o_path: type: {}'.format(type(o_path)))
        raw_input('slic: type: {}'.format(type(slic)))
        raw_input('blob_objs: type: {}'.format(type(blob_objs)))
        raw_input('f_ext: type: {}'.format(type(f_ext)))

        self.loc.plot_labels(o_path+self.slc_name+f_ext, slic, blob_objs)



