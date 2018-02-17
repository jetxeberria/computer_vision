from inspect import stack                   # To write log
import matter_lib as matt
import structure as sct             # Structure objects hierarchy


log_file_heading = 'File: '+__file__.split('/')[-1]+' '

class MRI_inspect(object):
    files_MRI_path = ''
    files_MRI_names = []
    matter_obj_list = []
    related_blob_list = []
    imobj_slice_obj_list = []

    def __init__(self, log):
        self.log = log
        self.log_class_heading = log_file_heading+"Class: "\
            +self.__class__.__name__
        log_method_heading = self.log_class_heading+" Method: "+stack()[0][3]\
            +" ::: "
        self.log.write_log("log",log_method_heading+"Initialization called")
        self.struct = sct.Structure(self.log)

    def set_files_path(self, files_path):
        '''
        Stores as an attribute the path Magnetic Resonance Image files are 
        stored in.

        Input parameters:
                    files_path:     <str>
                                    Path to MRI directory.
                                    /path/to/directory/

        Updates object atributes:
                    files_MRI_path: <str>
                                    Path to MRI directory 
        '''
        self.files_MRI_path = files_path

    def set_files_names(self, files_names):
        '''
        Stores as an attribute the MRI file names.

        Input parameters:
                    files_names:     <list>
                                    List with the names of files. 
                                    ['filename.extension',...] 

        Updates object atributes:
                    files_MRI_names: <list>
                                    List with the names of files. 
        '''
        self.files_MRI_names = files_names

    def make_matter_objs(self, filespath=None, filesnames=None):
        '''
        Stores as an attribute the list resulting of using the files pointed by
        'filespath' and 'filesnames' to create objects of class 'Matter'.
        By default takes self object attributes.

        Input parameters:
                    filespath:     <str>
                                    Path to files directory 
                                    /path/to/directory/
                    filesnames:     <list>
                                    List with the names of files. 
                                    ['filename.extension',...] 

        Updates object atributes:
                    matter_obj_list: <list>
                                    List of objects of class 'Matter'. 
        '''
        if filespath is None:
            filespath = self.files_MRI_path
        if filesnames is None:
            filesnames = self.files_MRI_names

        self.matter_obj_list = self.struct.create_matter_objs(filespath, filesnames)

#    def essay_matter_access(self, matters_to_name):
#        '''
#        Description.
#
#        Parameters:
 #                   name:           <classtype>
 #                                   description
#
#        Returns:
#                    name:           <classtype>
#                                    description 
#        '''
#
#        raw_input('matters_to_name: type: {}'.format(type(matters_to_name)))
#
#        for matter in matters_to_name:
#            if matter.name=='I3TWM':
#                i3twm_obj = matter
#            if matter.name=='I3TGM':
#                i3tgm_obj = matter
#            if matter.name=='I3TCSF':
#                i3tcsf_obj = matter
#            if matter.name=='I3T':
#                i3t_obj = matter
#
#        raw_input('i3twm_obj: type: {}'.format(type(i3twm_obj)))
#        raw_input('i3tgm_obj: type: {}'.format(type(i3tgm_obj)))
#        raw_input('i3tcsf_obj: type: {}'.format(type(i3tcsf_obj)))
#        raw_input('i3t_obj: type: {}'.format(type(i3t_obj)))
#
#        return i3twm_obj, i3tgm_obj, i3tcsf_obj, i3t_obj

    def make_imobj_slice_objects(self, matter_objs=None):
        '''
        Stores as an attribute the list resulting of using the 'Matter' objects 
        pointed by 'matter_objs' to create objects of class 'ImageObjectSlice'.
        Each object is conformed by the slices of all matters and there are as
        many objects as slices are extracted from each matter.
        By default takes self object attributes.

        Parameters:
                    matter_objs:    <list>
                                    List of objects of class 'Matter'

        Updates object atributes:
           imobj_slice_obj_list:    <list>
                                    List of objects of class 'ImageObjectSlice' 
        '''
        if matter_objs is None:
            matter_objs = self.matter_obj_list

        self.imobj_slice_obj_list = self.struct.create_imobj_slice_objs(matter_objs)
