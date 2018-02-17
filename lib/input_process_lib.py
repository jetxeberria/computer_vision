from inspect import stack                   # To write log
import SimpleITK as sitk
import numpy as np
import sys                                  # To manage input arguments

log_file_heading = 'File: '+__file__.split('/')[-1]+' '

class Input_process(object):
    
    def __init__(self, log):
        self.log = log
        self.log_class_heading = log_file_heading+"Class: "\
            +self.__class__.__name__
        log_method_heading = self.log_class_heading+" Method: "+stack()[0][3]\
            +" ::: "
        self.log.write_log("log",log_method_heading+"Initialization called")

    def read_input(self, i_path, i_fname):
        '''
        Reads the file pointed by the inputs with the Simple ITK image file
        reader method. Returns the result to the caller.

        Parameters:
                    i_path:     <str>
                                Path to 3D files directory.
                                i.e. /path/to/directory/

                    i_fname:    <str>
                                Name of 3D file.
                                i.e. 'filename.extension'

        Returns:
                    image:      <SimpleITK.SimpleITK.Image>
                                Image 3D. 
        '''

        reader = sitk.ImageFileReader()
        reader.SetFileName(i_path+i_fname)
        image = reader.Execute()

        return image

    def preprocess_serie(self, input_serie):
        '''
        Perform normalization over input 3-dimensional image with SimpleITK 
        method and get the numpy array version of the image. After that,
        perform transposing and rotating operations to properly display the
        image series. Returns the result to the caller.

        Parameters:
                    input_serie:    <SimpleITK.SimpleITK.Image>
                                    3-dimensional image.

        Returns:
                    turn:           <numpy.ndarray>
                                    3-dimensional numpy array of the image. 
        '''
        norm = sitk.Normalize(input_serie)
        npa = sitk.GetArrayFromImage(norm)
        trans = np.transpose(npa, (0,2,1))
        rot = trans[::-1,:,:]
        turn = rot[:,:,::-1]

        return turn

    def binarize_serie(self, input_s, thres_percent):
        '''
        Perform thresholding over the 'input_s'. Get the mask of the values over
        the 'thres_percent' percentage of the input values range.

        Parameters:
                    input_s:        <numpy.ndarray>
                                    3d array of the image to be binarized.
                    thres_percent:  <int>
                                    percent value over which pixels are going 
                                    to be selected.

        Returns:
                    thres_serie:    <numpy.ndarray>
                                    3d array of the image binarized over 
                                    threshold. 
        '''

        max_ = np.max(input_s)
        min_ = np.min(input_s)
        threshold = ((max_ - min_) / 100.0 ) * thres_percent + min_
        thres_serie = input_s > threshold

        if '-debug' in sys.argv:
            print ('binarizing:: max_: {} min_: {} threshold: {}'.format(max_,\
                min_, threshold))

        return thres_serie
