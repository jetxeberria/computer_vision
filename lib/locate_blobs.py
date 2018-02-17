from matplotlib import pyplot as plt 
from skimage import measure as msr
from skimage import morphology as mph
from skimage import draw
from scipy import ndimage as ndi
from scipy import spatial as spt
from inspect import stack                   # To write log
import numpy as np
import sys

log_file_heading = 'File: '+__file__.split('/')[-1]+' '

class Locate_blobs(object):
    
    def __init__(self, log):
        self.log = log
        self.log_class_heading = log_file_heading+"Class: "\
            +self.__class__.__name__
        log_method_heading = self.log_class_heading+" Method: "+stack()[0][3]\
            +" ::: "
        self.log.write_log("log",log_method_heading+"Initialization called")

    def find_labels(self, im2d):
        '''
        Returns the array and number resulting of differently labelling not
        connected blobs of 'im2d' image. The connectivity is set by pixels 
        neighbouring as 8-neighbour, i.e. a 3x3 matrix of ones.

        Parameters:
                    im2d:           <numpy.ndarray>
                                    2d array image whose blobs are going to be
                                    labelled.

        Returns:
                    labelled_arr:   <numpy.ndarray>
                                    Array differently labelled for each blob. 
                                    Has the same shape as input array.
                    labels_number:  <int>
                                    Number of different blobs found. 
        '''
        labelled_arr,labels_number = msr.label(im2d, connectivity=2, return_num=True)

        return labelled_arr, labels_number

    def plot_labels(self, out_f_path, lbl_slice, blobs, blobs2=None, blobs3=None):
        '''
        Plots the blobs of the three types found in the slices in a file in 
        'o_path' with extension 'f_ext'.
        For each type annotates its reference:
            - White color for single number are for objects of type 1. The 
                number is the slice's blob number that corresponds to that
                object.
            - Blue or white color (the second in case it is printed alone) for
                the structure '#:#' for objects of type 2. The numbers 
                corresponds to the white matter slice's blob number and the 
                gray matter's one respectively.
            - Green color for single word are for objects of type 3. The word
                is the position of the type 3 object, either 'left' or 'right'.

        Parameters:
                    out_f_path:     <str>
                                    Output path of the plots.
                    lbl_slice:      <numpy.ndarray>
                                    2d image array to display.
                    blobs:          <list>
                                    List of blobs of the objects of class 
                                    'ImageObject1'. 
                    blobs2:          <list>
                                    List of blobs of the objects of class 
                                    'ImageObject2'.
                    blobs3:          <list>
                                    List of blobs of the objects of class 
                                    'ImageObject3'.

        Returns:
                    None 
        '''
        # Plot image
        fig=plt.figure()
        plt.imshow(lbl_slice, cmap='nipy_spectral')
        plt.axis('on')

        # Annotate different labels
        # If in 'blobs' there is a single-dimension array, iterate over them
        if np.asarray(blobs).ndim == 1:
            for blob in blobs:
                # Annotate blob number in centroid location
                plt.annotate( s=str(blob.blob_num), xycoords='data', \
                    xy=tuple(np.array(blob.blob_ctrd)[::-1]), color=(0.9, 0.9, 0.9))

        # Just in case it is passed type 2 blobs as unique argument
        elif np.asarray(blobs).ndim == 2:
            for blob_wm, blob_gm in blobs:
                # Annotate inner:outer blob number in centroid location
                plt.annotate( s=str(blob_wm.blob_num)+':'+str(blob_gm.blob_num),\
                    xycoords='data', xy=tuple(np.array(blob_wm.blob_ctrd)[::-1]),\
                    color=(0.9, 0.9, 0.9))

        # If 'blobs2' correctly has dimension 2, iterate over its pairs
        if blobs2 is not None:
            if np.asarray(blobs2).ndim == 2:
                for blob_wm, blob_gm in blobs2:
                    # Annotate inner:outer blob number in centroid location
                    plt.annotate( s=str(blob_wm.blob_num)+':'+str(blob_gm.blob_num),\
                        xycoords='data', xy=tuple(np.array(blob_wm.blob_ctrd)[::-1]),\
                        color=(0.1, 0.1, 0.9))

        # If 'blobs3' correctly has dimension 3, iterate over its pairs
        if blobs3 is not None:
            if np.asarray(zip(blobs3)).ndim == 3:
                for blobs_wm, blobs_gm, position in blobs3:
                    # Annotate inner:outer blob number in centroid location
                    gm_mask = np.zeros(lbl_slice.shape)
                    for blob in blobs_gm:
                        gm_mask[blob.blob_mask>0] = 1
                    center = np.round(msr.regionprops(gm_mask.astype(np.int))[0].centroid)
                    center = (center[1], center[0])
                    plt.annotate( s=str(position), xycoords='data', xy=center,\
                        color=(0.1, 0.9, 0.1))





#            for blob_wm in zip(*blobs)[0]:
#                plt.annotate( s=str(blob_wm.blob_num), xycoords='data', \
#                    xy=tuple(np.array(blob_wm.blob_ctrd)[::-1]), color=(0.9, 0.2, 0.2))
#            for blob_gm in zip(*blobs)[1]:
#                plt.annotate( s=str(blob_gm.blob_num), xycoords='data', \
#                    xy=tuple(np.array(blob_gm.blob_ctrd)[::-1]), color=(0.2, 0.2, 0.9))
        plt.savefig(out_f_path)
        plt.close(fig)

    def blob_inner_region(self, props):
        '''
        Returns the image resulting of extracting the inner region of the blob.

        Parameters:
                    props:          <skimage.measure._regionprops._RegionProperties>
                                    Properties of the blob.

        Returns:
                    inner_region:           <numpy.ndarray>
                                    Inner region of the blob in a image of the 
                                    same size as blob bbox 
        '''
        image = props.image
        filled_image = props.filled_image
        inner_region = filled_image.astype(np.int) - image.astype(np.int)

        return inner_region

    def relocate_blob(self, output_shape, subimage, blob_props):
        '''
        Returns the image 'subimage' extended in an empty image of shape 
        'output_shape'.

        Parameters:
                    output_shape:           <tuple>
                                    Output image dimensions desired.
                                    (x_dim, y_dim) 
                   subimage:           <numpy.ndarray>
                                    Image of a blob or a region of the main image.
                   blob_props:      <skimage.measure._regionprops._RegionProperties>
                                    Properties of the given blob.

        Returns:
                    subimage_resized:           <numpy.ndarray>
                                    Blob or region extended to the desired shape. 
        '''
        b_props = blob_props
        ref_corner = b_props.bbox
        subimage_resized = np.zeros(output_shape)
        coords = np.where(subimage==True)
        for coord in zip(*coords):
            x = coord[0] + ref_corner[0]
            y = coord[1] + ref_corner[1]
            subimage_resized[x, y] = 1

        return subimage_resized

    def characterize_blobs_type1(self, wm_blobs_list, gm_blobs_list):
        '''
        Returns in a list the 'Blob' objects of gray matter that match the 
        constraints to be considered as object of type 1. 
        These are:  
            - having a medium size 2000 > area > 3.
            - having its centroid in the lower half of the image, excluding the
                center zone.
            - having no correspondence between its inner mask and no gray nor 
                white blob.

        Parameters:
                    wm_blobs_list:  <list>
                                    List of objects of class 'Blob' of white matter
                    gm_blobs_list:  <list>
                                    List of objects of class 'Blob' of gray matter

        Returns:
                    type1_blobs:    <list>
                                    List of objects of class 'Blob' from gray 
                                    matter.
        '''
        type1_blobs = []
        for i, gm_blob in enumerate(gm_blobs_list):
            # Check if it is too big
            is_big = 0
            if gm_blob.props.area > 2000:
                is_big = 1

            # Check if it is too small
            is_noise = 0
            if gm_blob.props.area < 3:
                is_noise = 1

            # Check if its centroid is in candidate region
            is_out = 0
            if (gm_blob.blob_ctrd[0] < 90) or (200 > gm_blob.blob_ctrd[1] > 150):
                is_out = 1

            # Check if it is empty ('is_something' must be 0):
            # By NOT HAVING correspondence between its inner area and any white
            # matter blob.
            is_something = 0
            wm_corr = 0
            for wm_blob in wm_blobs_list:
                wm_corr = correspondence(gm_blob.inner_mask, wm_blob.blob_mask)
                if wm_corr > 0: 
                    is_something += wm_corr
            # And by NOT HAVING correspondence between its inner area and any other 
            # gray matter blob.
            self_corr = 0
            for j in range(len(gm_blobs_list)):
                if j != i:
                    self_corr = correspondence(gm_blob.inner_mask, \
                        gm_blobs_list[j].blob_mask)
                if self_corr > 5:
                    is_something += self_corr

            # Check if blob supports all constrains 
            #   empty:              is_something = 0
            #   correct size:       is_big = 0 and is_noise = 0
            #   correct_location:   is_out = 0
            if np.all([is_something == 0, is_big == 0, is_noise == 0, is_out == 0]):
                type1_blobs.append(gm_blob)

        return type1_blobs

    def characterize_blobs_type2(self, wm_blobs_list, gm_blobs_list):
        '''
        Returns in a list pairs of the 'Blob' objects of white matter and gray 
        matter that match the constraints to be considered as objects of type 2.
        These are:  
            - having a medium size 2000 > area > 3.
            - having its centroid in the lower half of the image, excluding the
                center zone.
            - having no correspondence between its inner mask and no other gray
                matter blob. 
            - having correspondence between its inner mask and a white matter 
                blob.

        Parameters:
                    wm_blobs_list:   <list>
                                    List of objects of class 'Blob' of white matter
                    gm_blobs_list:  <list>
                                    List of objects of class 'Blob' of gray matter

        Returns:
                    type2_blobs:           <classtype>
                                    List of pairs of objects of class 'Blob' of 
                                    both matters.
        '''
        type2_blobs = []

        # If there is no blob of GM or of WM in this slice, there is no 
        # imobject type 2, and 'type2_blobs' returns empty
        # If there is no found candidate blob, 'type2_blobs' returns also empty.

        if len(wm_blobs_list) > 0 and len(gm_blobs_list) > 0:
            for i, gm_blob in enumerate(gm_blobs_list):

                # Check if it is too big
                is_big = 0
                if gm_blob.props.area > 2000:
                    is_big = 1

                # Check if it is too small
                is_noise = 0
                if gm_blob.props.area < 3:
                    is_noise = 1

                # Check if its centroid is in candidate region
                is_out = 0
                if (gm_blob.blob_ctrd[0] < 90) or (200 > gm_blob.blob_ctrd[1] > 150):
                    is_out = 1

                # Check if it has a hole
                no_hole = 0
                if np.sum(gm_blob.inner_mask) < 3:
                    no_hole = 1

                # Check if its hole is filled

                # Check if its hole is properly filled
                # By NOT HAVING correspondence between its inner area and any other
                # gray matter blob.
                is_trash = 0
                self_corr = 0
                for j, gm_blob2 in enumerate(gm_blobs_list):
                    if j != i:
                        self_corr = correspondence(gm_blob.inner_mask, \
                            gm_blob2.blob_mask)
                    if self_corr > 0:
                        is_trash = 1

                # By HAVING correspondence between its inner area and any white
                # matter blob.
                wm_candidate = None
                min_corr = 0
                for wm_blob in wm_blobs_list:
                    wm_corr = correspondence(gm_blob.inner_mask, wm_blob.blob_mask)
                    if wm_corr > min_corr: 
                        min_corr = wm_corr
                        wm_candidate = wm_blob

                # Check if blob supports all constrains
                #   has hole:           no_hole = 0
                #   hole is filled:     min_corr > 0
                #   correct size:       is_big = 0 and is_noise = 0
                #   correct location:   is_out = 0
                if np.all([no_hole == 0, min_corr > 0, is_big == 0, \
                        is_noise == 0, is_out == 0]):
                    type2_blobs.append((wm_candidate, gm_blob))

            type2_blobs = zip(*type2_blobs)

        return type2_blobs

    def find_candidate_regions_type3(self, wm_slice, gm_slice):
        '''
        Returns a 2d image array with candidate regions extracted from original 
        blobs.To do so, first it is extracted a mask merging the 'wm_slice' mask
        and the 'gm_slice' one, this is encouraged by previously dilating 
        'wm_slice' mask, as it is the inner region, to ensure the mixed mask has
        no holes between gray matter and white matter masks.
        Then, it is performed a serie of erosion - dilation - erosion - dilation
        over the mixed mask with custom structure elements (that defines 
        neighbouring)
        The result is transformed to get the euclidean distance of each pixel 
        from the background and it is performed a smooth thresholding over it.
        The resulting regions are the seeds that are used as init points to 
        the watershed algorithm that will draw a dispersion of them along the
        distance image, given as argument. 
        Finally, the resulting labelled regions are masked with both white and
        gray matter masks, leading the blobs of each matter labelled as the 
        seeds point.

        Parameters:
                    wm_slice:           <lib.slice_lib.Slice>
                                    Object 'Slice' of matter 'wm'.
                    gm_slice:           <lib.slice_lib.Slice>
                                    Object 'Slice' of matter 'gm'.

        Returns:
                    wm_blobs_lbl:           <list>
                                    2d image of the differenced regions of 
                                    white matter labelled by watershed algorithm
                    gm_blobs_lbl:           <list>
                                    2d image of the differenced regions of 
                                    gray matter labelled by watershed algorithm
        '''
        # If there is no found candidate blob, 'type3_blobs' returns also empty.

        # Lets mix wm and gm masks to avoid holes in the gm blobs, then
        # performing morphology operations won't counterpose blobs inner
        # regions.
        image_gm = gm_slice.slc_arr
        image_wm = wm_slice.slc_arr
        image_wm_dilated = mph.dilation(image_wm, np.ones((5,5)))   
        image_mix = np.copy(image_gm)
        image_mix[image_wm_dilated > 0] = 1

        # Generate structure elements to differently erode and dilate 
        # image
        struct_elem_A = np.array([[1,0,0,0,0,0,0,0,0,0,1],
                                  [1,1,0,0,0,0,0,0,0,1,1],
                                  [1,1,1,1,1,1,1,1,1,1,1],
                                  [1,1,0,0,0,0,0,0,0,1,1],
                                  [1,0,0,0,0,0,0,0,0,0,1]])

        struct_elem_B = np.array([[1,0,0,0,0,0,0,0,1],
                                  [1,1,1,1,1,1,1,1,1],
                                  [1,0,0,0,0,0,0,0,1]])

        # Perform erosion transformation to expand black areas and attempt 
        # to split global blob. Small bright areas, that often are noise,
        # disappear.
        ero1 = mph.erosion(image_mix, selem=struct_elem_A)

        # Perform dilation transformation to recover image main shape. 
        # Enlarge bright areas, which could undo our splitting, but can
        # be driven with a structure element, different of such used in 
        # erosion.
        dil1 = mph.dilation(ero1, selem=struct_elem_B)

        # Performing erosion again it is achieved a good splitting of lower
        # blobs
        ero2 = mph.erosion(dil1, selem=struct_elem_A)
        
        # It is performed dilation again to recover at least a shade of the
        # original shape.
        dil2 = mph.dilation(ero2, selem=np.ones((3,3)))

        # Now, let's find the blobs:

        # It is performed euclidean distance transformation. For each true 
        # pixel it is given the distance measure from background. Ascends 
        # to farest regions from background.
        dist = ndi.distance_transform_edt(dil2)

        # They are gonna be discarded the pixels with values under the 10% 
        # of the value range, as they are the frontiers of foreground.
        thres_percent = np.float64(5)
        threshold = thres_per_percent(dist, thres_percent)

        # By performing this, it is attempted to split main blob in small 
        # ones
        key_image = dist > threshold

        # Label the regions
        seeds = msr.label(key_image)

###############
##########
#####
#            plt.imshow(seeds, cmap='nipy_spectral')
#            plt.show()
#            raw_input('got seeds. lets improve them')
#####
##########
###############

        # Merge neigh seeds regions
        merged_seeds =  merge_neigh_seeds(seeds)

###############
##########
#####
#            plt.imshow(merged_seeds, cmap='nipy_spectral')
#            plt.show()
#            raw_input('seeds merged. lets purge them')
#####
##########
###############

        # Discard seeds small regions
        purged_seeds= ignore_small_seeds(merged_seeds)

###############
##########
#####
#            plt.imshow(purged_seeds, cmap='nipy_spectral')
#            plt.show()
#            raw_input('seeds purged. lets perform watershed over them')
#####
##########
###############

        # And the key of the process: Perform watershed algorithm over the 
        # distance image with the taken seeds and with the original image as
        # mask
#            labels = mph.watershed(dist, purged_seeds, mask=image_gm, compactness=10)
        labels = mph.watershed(dist, purged_seeds, mask=None, compactness=10)
     
###############
##########
#####
#            plt.imshow(labels, cmap='nipy_spectral')
#            plt.show()
#            raw_input('labels resulted from watershed, lets split by matters')
#####
##########
###############
        
        # Supress white matter mask from labels image to obtain GM segmented
        # image.
        wm_blobs_lbl = np.copy(labels)
        gm_blobs_lbl = np.copy(labels)

        wm_blobs_lbl[image_wm == 0] = 0
        gm_blobs_lbl[image_gm == 0] = 0

###############
##########
#####
#            fig, axes = plt.subplots(2,2)
#            axes[0,0].imshow(seeds, cmap='nipy_spectral')
#            axes[0,0].set_title('seeds')
#            axes[0,1].imshow(merged_seeds, cmap='nipy_spectral')
#            axes[0,1].set_title('merged_seeds')
#            axes[1,0].imshow(purged_seeds, cmap='nipy_spectral')
#            axes[1,0].set_title('purged_seeds')
#            axes[1,1].imshow(labels, cmap='nipy_spectral')
#            axes[1,1].set_title('labels')
#            plt.show()
#            raw_input('these are the blobs by matters, lets characterize them') 
#            fig, axes = plt.subplots(2,2)
#            axes[0,0].imshow(labels, cmap='nipy_spectral')
#           axes[0,0].set_title('labels')
#           axes[0,1].imshow(purged_seeds, cmap='nipy_spectral')
##           axes[0,1].set_title('purged_seeds')
#           axes[1,0].imshow(wm_blobs_lbl, cmap='nipy_spectral')
#           axes[1,0].set_title('wm_blobs_lbl')
#           axes[1,1].imshow(gm_blobs_lbl, cmap='nipy_spectral')
#           axes[1,1].set_title('gm_blobs_lbl')
#          plt.show()
#          raw_input('these are the blobs by matters, lets characterize them')
#####
##########
###############


        return wm_blobs_lbl, gm_blobs_lbl


###############
##########
#####
#            selected_wm_left, selected_wm_right = self.characterize_blobs_type3_wm#(wm_blobs_lbl)
#            selected_gm_left, selected_gm_right = self.characterize_blobs_type3_gm(gm_blobs_lbl)
#
#
#            gm_props = msr.regionprops(labels)            
#            for region_props in gm_props:
#                fig, ax = plt.subplots()
#                ax.imshow(region_props.image)
#                ax.set_title('region_props{}_area.png'.format(region_props.label))
#                plt.show()
#
#        raw_input()

                     

#        return (selected_wm_left
#####
##########
###############

    def characterize_blobs_type3(self, wm_blobs_list, gm_blobs_list, \
            original_wm_slice, original_gm_slice):
        '''
        Returns either a list of pairs of white and gray matter 'Blob' objects, 
        or a list of pair of an empty list and a gray matter 'Blob' objects,
        that match the constraints to be considered as objects of type 3. 
        This characterization takes in count groups of blobs instead of previous
        ones that takes single ones or pairs.
        Each blob is characterized in different steps with own constraints.
        If there is no 'Blob' that match the constraints returns an empty list.

        Parameters:
                    wm_blobs_list:     <list>
                                    List of objects of class 'Blob' of white matter.
                    gm_blobs_list:     <list>
                                    List of objects of class 'Blob' of gray matter.
                    original_wm_slice: <lib.slice_lib.Slice>
                                    Object of class 'Slice' of white matter.
                    original_gm_slice: <lib.slice_lib.Slice>
                                    Object of class 'Slice' of gray matter.

        Returns:
                    type3_blobs:     <tuple>
                                    Pair of lists of objects of class 'Blob', of 
                                    white and gray matter respectively.
                                    i.e. (wm_blobs, gm_blobs)
        '''
        type3_blobs = []

        # If there is no blob of GM in this slice, there is no 
        # imobject type 3, and 'type3_blobs' returns empty
        # If there is no found candidate blob, 'type3_blobs' returns also empty.

        if len(gm_blobs_list) > 0:

            mask_wm = original_wm_slice.slc_arr
            mask_gm = original_gm_slice.slc_arr
            image_mix = np.copy(mask_gm)
            image_mix[mask_wm > 0] = 1
            mix_labels = msr.label(image_mix)
            mix_props = msr.regionprops(mix_labels)

            # Locate biggest blob. It is suppossed to be the main blob.
            max_area = 0
            main_mixed_blob = None
            for blob_p in mix_props:
                if blob_p.area > max_area:
                    main_mixed_blob = blob_p
                    max_area = blob_p.area

            # Create a mask with exclusively the main blob.
            main_mixed_blob_mask = np.zeros(original_wm_slice.slc_arr.shape)
            main_mixed_blob_mask[mix_labels == main_mixed_blob.label] = 1

            type3_wm_blobs = self.characterize_blobs_type3_wm(wm_blobs_list, \
                main_mixed_blob_mask) 
            type3_gm_blobs = self.characterize_blobs_type3_gm(gm_blobs_list, \
                main_mixed_blob_mask) 

            if len(type3_gm_blobs) > 0:
                if len(type3_wm_blobs) > 0:
                    type3_blobs = (type3_wm_blobs, type3_gm_blobs)
                else:
                    type3_blobs = (type3_gm_blobs,)  # This trick ease length measure
            else:
                type3_blobs = ()

        return type3_blobs

    def characterize_blobs_type3_wm(self, wm_blobs, main_mask):
        '''
        Returns in a list the 'Blob' objects of white matter that match the 
        constraints to be considered as object of type 3. 
        These are:  
            - having a medium size 2000 > area > 3.
            - having its centroid in the lower half of the image, excluding the
                center zone. 
            - having correspondence between its mask and the biggest blob of 
                the mixed mask, stored in 'main_mask'.

        Parameters:
                    wm_blobs:           <list>
                                    List of objects of class 'Blob' of white 
                                    matter.
                    main_mask:           <numpy.ndarray>
                                    2d image array of the main blob of the 
                                    mixed mask.

        Returns:
                    blobs_ty3_wm:           <list>
                                    List of objects of class 'Blob' of white 
                                    matter.
        '''
        blobs_ty3_wm = []

###############
##########
#####
#        print ('wm_blobs: {} type: {}'.format(np.sum(np.unique(wm_blobs, \
#            return_counts=True)[1]), type(wm_blobs[0])))
#        ax = plt.subplots()
#        ax.imshow(main_mask)
#        ax.set_title('main_mask')
#        plt.show()
#        raw_input()
#####
##########
###############
        if len(wm_blobs)>0:
            if '-debug' in sys.argv:
                print ('Checking WM blobs for type 3 objects. Slice {}'.format(\
                    wm_blobs[0].slice_number))
        for i, wm_blob in enumerate(wm_blobs):
    
            # Check if it is too big
            is_big = 0
            if wm_blob.props.area > 2000:
                is_big = 1
        
            # Check if it is too small
            is_noise = 0
            if wm_blob.props.area < 3:
                is_noise = 1
        
            # Check if its centroid is in candidate region
            is_out = 0
            if (wm_blob.blob_ctrd[0] < 95) or (200 > wm_blob.blob_ctrd[1] > 150):
                is_out = 1
        
            # Check if the blob lies over the original MAIN mixed blob with
            # a high level correspondence. This means that the blobs were 
            # merged to the main blob.

            wm_corr = correspondence(main_mask, wm_blob.blob_mask)
      
            is_correlated = 0
#temp            max_discordance = 5
#temp            if wm_corr > (wm_blob.props.area - max_discordance):
#temp                is_correlated = 1 
 
###############
##########
#####
#            max_discordance = 5
            if wm_corr > wm_blob.props.area*0.8:
                is_correlated = 1 

            if '-debug' in sys.argv:
                print ('Blob {} flags: is_big {} is_noise {} is_out {} '\
                    'is_correlated {}'.format(wm_blob.blob_num, is_big, \
                    is_noise, is_out, is_correlated))
#####
##########
############### 
        
            # Check if blob supports all constrains
            #   correct size:       is_big = 0 and is_noise = 0
            #   correct location:   is_out = 0
            #   was main blob:      is_correlated = 1
            if np.all([is_big == 0, is_noise == 0, is_out == 0, is_correlated == 1]):
                blobs_ty3_wm.append(wm_blob)

###############
##########
#####
#                fig, ax = plt.subplots()
#                ax.imshow(wm_blob.blob_mask)
#                ax.set_title('wm candidate accepted')
#                plt.show()

 #           else:

 #               fig, ax = plt.subplots()
 #               ax.imshow(wm_blob.blob_mask)
 #               ax.set_title('wm candidate denied')
 #               plt.show()


#        print ('blobs_ty3_wm: {}'.format(blobs_ty3_wm))
#        raw_input()
#####
##########
###############

        return blobs_ty3_wm
    

    def characterize_blobs_type3_gm(self, gm_blobs, main_mask):
        '''
        Returns in a list the 'Blob' objects of gray matter that match the 
        constraints to be considered as object of type 3. 
        These are:  
            - having a medium size 3000 > area > 15 
            - having its centroid in the lower half of the image, excluding the
                center zone. 
            - having correspondence between its mask and the biggest blob of 
                the mixed mask, stored in 'main_mask'.

        Parameters:
                    gm_blobs:        <list>
                                    List of objects of class 'Blob' of gray 
                                    matter.
                    main_mask:       <numpy.ndarray>
                                    2d image array of the main blob of the 
                                    mixed mask.

        Returns:
                    blobs_ty3_gm:    <list>
                                    List of objects of class 'Blob' of gray 
                                    matter.
        '''
        blobs_ty3_gm = []
        
        if len(gm_blobs)>0:
            if '-debug' in sys.argv:
                print ('Checking WM blobs for type 3 objects. Slice {}'.format(\
                    gm_blobs[0].slice_number))

        for i, gm_blob in enumerate(gm_blobs):
    
            # Check if it is too big
            is_big = 0
            if gm_blob.props.area > 3000:
                is_big = 1
        
            # Check if it is too small
            is_noise = 0
            if gm_blob.props.area < 15:
                is_noise = 1
        
            # Check if its centroid is in candidate region
            is_out = 0
            if (gm_blob.blob_ctrd[0] < 95) or (200 > gm_blob.blob_ctrd[1] > 150):
                is_out = 1
    
            # Check if the blob lies over the original MAIN mixed blob with
            # a high level correspondence. This means that the blobs were 
            # merged to the main blob.
            gm_corr = correspondence(main_mask, gm_blob.blob_mask)
        
            is_correlated = 0
            if gm_corr > gm_blob.props.area*0.8:
                is_correlated = 1 
###############
##########
#####
            if '-debug' in sys.argv:
                print ('Blob {} flags: is_big {} is_noise {} is_out {} '\
                    'is_correlated {}'.format(gm_blob.blob_num, is_big, \
                    is_noise, is_out, is_correlated))
#####
##########
############### 
     
            # Check if blob supports all constrains
            #   has hole:           no_hole = 0
            #   hole is filled:     min_corr > 0
            #   correct size:       is_big = 0 and is_noise = 0
            #   correct location:   is_out = 0
            if np.all([is_big == 0, is_noise == 0, is_out == 0, is_correlated == 1]):
                blobs_ty3_gm.append(gm_blob)
###############
##########
#####
#                fig, ax = plt.subplots()
#                ax.imshow(gm_blob.blob_mask)
#                ax.set_title('gm candidate accepted')
#                plt.show()
#            
#            else:
#                fig, ax = plt.subplots()
#                ax.imshow(gm_blob.blob_mask)
#                ax.set_title('gm candidate denied')
#                plt.show()
#####
##########
###############        

        return blobs_ty3_gm




        

def correspondence(matrixA, matrixB):
    '''
    Returns the number of pixels of 'matrixB' that have the same positions as 
    the ones in 'matrixA'.

    Parameters:
                matrixA:           <numpy.ndarray>
                                Matrix of reference with which compare.
                matrixB:           <numpy.ndarray>
                                Matrix candidate to occupy reference matrix.
                                

    Returns:
                correspondence:  <numpy.int64>
                                Number of pixels that match between matrix 
    '''
    mA_sum = np.sum(matrixA).astype(np.int)
    mSub = np.copy(matrixA)
    mSub[matrixB > 0] = 0
    mSub_sum = np.sum(mSub).astype(np.int)
    correspondence = mA_sum - mSub_sum

    return correspondence

def thres_per_percent(image, percentage):
    '''
    Returns the real value of the 'percentage' of the 'image' range values.
    i.e. plus minimum value.

    Parameters:
                image:           <numpy.ndarray>
                                2d image array to get range values from.
                percentage:           <numpy.float64>
                                percentage of range values desired.

    Returns:
                threshold:           <numpy.float64>
                                value of the set percentage of the image range 
                                values.
    '''
    thres_percent = percentage
    max_ = np.max(image)
    min_ = np.min(image)
    threshold = ((max_ - min_) / 100.0 ) * thres_percent + min_

    return threshold

def ignore_small_seeds(seeds_mask):
    '''
    Returns a labelled image .

    Parameters:
                seeds_mask:           <numpy.ndarray>
                                Labelled 2d image.

    Returns:
                new_seeds_mask:           <numpy.ndarray>
                                Labelled 2d image of the same shape as input one
                                with small blobs discarded.
    '''
    # They are discarded the small seeds regions
    seeds_props = msr.regionprops(seeds_mask)
    choosen_seeds = []
    for prop in seeds_props:
        if prop.area > 5:
            choosen_seeds.append(prop)
    # Generate new seeds mask with the choosen regions
    new_seeds_mask = np.zeros(seeds_mask.shape)
    for seed in choosen_seeds:
        new_seeds_mask[seeds_mask==seed.label]=seed.label

    return new_seeds_mask

def merge_neigh_seeds(seeds_mask):
    '''
    Returns a labelled image equal to 'seeds_mask' with the regions that are 
    close set as the same label and with a line of the same label merging their
    centroids.

    Parameters:
                seeds_mask:     <numpy.ndarray>
                                Labelled 2d image.
    Returns:
                merged_seeds:   <numpy.ndarray>
                                Labelled 2d image of the same shape as input one
                                with close blobs merged. 
    '''
    #They are merged close regions.
    min_distance = 10000
    seeds_props = msr.regionprops(seeds_mask.astype(np.int))

    pairs = []
    nearest_neigh = None
    for i, prop_i in enumerate(seeds_props):
        for j, prop_j in enumerate(seeds_props):
            if i!=j:
                blobs_distance = spt.distance.euclidean(prop_i.centroid, \
                    prop_j.centroid)
                if blobs_distance < min_distance:
                    min_distance = blobs_distance
                    nearest_neigh = prop_j
        if nearest_neigh is not None:
            pair = [prop_i, nearest_neigh]
            pairs.append(pair)
        else:
            pair = []
        
        min_distance = 10000

    merge_this = []
    for pair in pairs:
        pair_distance = spt.distance.euclidean(pair[0].centroid, pair[1].centroid)
        if pair_distance < 15:
            merge_this.append(pair)
    
    merged_seeds = np.copy(seeds_mask)
    # For each pair the second member takes the label of the first one and it 
    # is drawn a line of the same label between them
    for seeds_pair in merge_this:
        # Relabel second member of pair 
        merged_seeds[seeds_mask==seeds_pair[1].label] = seeds_pair[0].label

        # Draw a line between blobs
        c0_x, c0_y = np.array(seeds_pair[0].centroid).astype(np.int)
        c1_x, c1_y = np.array(seeds_pair[1].centroid).astype(np.int)
        rr,cc = draw.line(c0_x, c0_y, c1_x, c1_y)
        merged_seeds[rr,cc] = seeds_pair[0].label

    return merged_seeds
