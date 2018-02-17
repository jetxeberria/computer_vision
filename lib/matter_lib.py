from inspect import stack                   # To write log
import input_process_lib as inp


log_file_heading = 'File: '+__file__.split('/')[-1]+' '

class Matter(object):
    file_MRI_name = ''
    file_MRI_path = ''
    sitk_img = None
    npa_img = None
    img3d = None
    name = ''
    slices_obj_list = []
    
    def __init__(self, log, filepath, filename, stct):
        self.log = log
        self.log_class_heading = log_file_heading+"Class: "\
            +self.__class__.__name__
        log_method_heading = self.log_class_heading+" Method: "+stack()[0][3]\
            +" ::: "
        self.log.write_log("log",log_method_heading+"Initialization called")

        self.file_MRI_name = filename
        self.file_MRI_path = filepath
        self.name = filename[:filename.rfind('.')]
#        self.struct = sct.Structure(self.log)
        self.in_proc = inp.Input_process(self.log)
        self.stct = stct

    def read_file(self, f_path=None, f_name=None):
        '''
        Stores as an attribute the result of reading a 3D (f.hdr+f.img) file 
        pointed by the inputs. 
        By default takes self object attributes.

        Parameters:
                    f_path:         <str>
                                    Path to 3D files directory.
                                    /path/to/directory/
                    f_name:         <str>
                                    Name of 3D file.
                                    'filename.extension'

        Updates object atributes:
                    sitk_img:       <SimpleITK.SimpleITK.Image>
                                    Image 3D. 
        '''
        if f_path is None:
            f_path = self.file_MRI_path
        if f_name is None:
            f_name = self.file_MRI_name

        self.sitk_img = self.in_proc.read_input(f_path, f_name)

    def preprocess(self, original=None):
        '''
        Stores as an attribute the result of performimg a basic processing 
        over the input file, such as normalization and a serie of rotations, 
        such as up-down rotating, right-left flipping and back-front turning. 
        By default takes self object attributes.

        Parameters:
                    original:       <SimpleITK.SimpleITK.Image>
                                    3-dimensional image.

        Updates object atributes:
                    npa_img:           <numpy.ndarray>
                                    3-dimensional numpy array of the image 
                                    normalized and well-oriented. 
        '''
        if original is None:
            original = self.sitk_img

        self.npa_img = self.in_proc.preprocess_serie(original)


    def binarize(self, to_binary=None, threshold=80):
        '''
        Stores as an attribute the result of performing thresholding over the 
        'to_binary' input 3-d image. Get the mask of the values over the 
        'threshold' percentage of the input values range.
        By default takes self object attributes.

        Parameters:
                    to_binary:      <numpy.ndarray>
                                    3d array image to be binarized.
                    threshold:      <int>
                                    percent value over which pixels are going 
                                    to be selected.

        Updates object atributes:
                    img3d:           <numpy.ndarray>
                                    3d array image binarized. 
        '''
        if to_binary is None:
            to_binary = self.npa_img

        if self.name == 'I3T':
            self.img3d = to_binary
        else:
            self.img3d = self.in_proc.binarize_serie(to_binary, threshold)

    def make_slice_objs(self, img3d=None, matt_name=None):
        '''
        Stores as an attribute the result of using the 3d array pointed by 
        'img3d' to create objects of class 'Slice'.
        By default takes self object attributes.

        Parameters:
                    img3d:           <numpy.ndarray>
                                    3d array image to slice.
                matt_name:           <str>
                                    Name to be set as attribute of the object.

        Updates object atributes:
          slices_obj_list:           <list>
                                    List of objects of class 'Matter'. 
        '''
        if img3d is None:
            img3d = self.img3d
        if matt_name is None:
            matt_name = self.name

        self.slices_obj_list = self.stct.create_slice_objs(img3d, matt_name)

