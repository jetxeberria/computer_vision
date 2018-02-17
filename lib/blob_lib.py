from inspect import stack                   # To write log
import numpy as np
import locate_blobs as loc          # Locate blobs functions

log_file_heading = 'File: '+__file__.split('/')[-1]+' '

class Blob(object):
    blob_num = None
    blob_ctrd = None
    blob_mask = None
    inner_mask = None
    slice_number = None
    props = None    
    matter_kind = ''

    def __init__(self, log, mask_arr, slc_numb, properties, mat_kind):
        self.log = log
        self.log_class_heading = log_file_heading+"Class: "\
            +self.__class__.__name__
        log_method_heading = self.log_class_heading+" Method: "+stack()[0][3]\
            +" ::: "
        self.log.write_log("log",log_method_heading+"Initialization called")

        self.blob_num = properties.label
        self.blob_mask = mask_arr
        self.slice_number = slc_numb
        self.matter_kind = mat_kind
        self.props = properties
        self.loc = loc.Locate_blobs(self.log)

    def find_blob_centroid(self, blob_props=None):
        '''
        Stores as an attribute the result of rounding the centroid coord of the
        blob.
        By default takes self object attributes.

        Parameters:
                    blob_props:     <skimage.measure._regionprops._RegionProperties>
                                    Blob properties, such as area, centroid, ...

        Updates object atributes:
                    blob_ctrd:      <numpy.ndarray>
                                    Coords of the centroid as integers 
        '''
        if blob_props is None:
            blob_props = self.props

        self.blob_ctrd = np.round(blob_props.centroid)

    def find_inner_region(self, b_mask=None, b_props=None):
        '''
        Stores as an attribute the result of creating a mask of the inner 
        region of the blob.
        By default takes self object attributes.

        Parameters:
                    b_mask:          <numpy.ndarray>
                                    Image of the blob with the shape of the
                                    slices.
                    b_props:        <skimage.measure._regionprops._RegionProperties>
                                    Properties of the blob.

        Updates object atributes:
                    inner_mask:     <numpy.ndarray>
                                    Inner region with the shape of given mask. 
        '''
        if b_mask is None:
            b_mask = self.blob_mask
        if b_props is None:
            b_props = self.props

        inner_region = self.loc.blob_inner_region(b_props)
        self.inner_mask = self.loc.relocate_blob(b_mask.shape, inner_region, b_props)


