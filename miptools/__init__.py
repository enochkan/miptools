import matplotlib.pyplot as plt
import pydicom
import numpy as np
import scipy.ndimage
from PIL import Image

# {
#     helper functions
# }

def visualize_img(img):
    plt.imshow(img, cmap=plt.cm.bone) 
    plt.axis('off')
    plt.show()

def save_img(img, output, size=None, extension='png'):
    image_2d = img.astype('float32')
    image_2d_scaled = (np.maximum(image_2d, 0) / image_2d.max()) * 255.0
    image_2d_scaled = np.uint8(image_2d_scaled)
    #resize if necessary
    if size:
        image_2d_scaled = cv2.resize(img_2d_scaled, dsize=size, interpolation=cv2.INTER_CUBIC)
    # Write the PNG file
    if extension == 'png':
        im = Image.fromarray(image_2d_scaled)
        im.save(output+'.png')
    if extension == 'jpg':
        im = Image.fromarray(image_2d_scaled)
        im.save(output+'.jpg')

def min_max(img, l, w):
    return (img - (l-w/2))/w

def get_dicom_field(x):
    return int(x[0]) if type(x) == pydicom.multival.MultiValue else int(x)
    
def get_meta(dcm):
    dicom_fields = [dcm[('0028','1050')].value,
                    dcm[('0028','1051')].value,]
    return [get_dicom_field(x) for x in dicom_fields]

# {
#     main functions
# }

def preprocess(path, org='brain', windowing=None, resample=False, visualize=False, save=False, save_filename='sample', extension='png'):
    if org == 'brain':
        if windowing is not None:
            img = brain_windowing(path, windowing, resample)
            # implement other preprocessing
    # implement other orgs

    if visualize:
        visualize_img(img)
    if save:
        save_img(img, output=save_filename, extension=extension)
        

def brain_windowing(path, mode, resample):
    dcm = pydicom.dcmread(path)
    if mode == 'bsb':
        return bsb_window(dcm)
    elif mode == 'simple':
        center, width = get_meta(dcm)
        return window_image(dcm, center, width, resample)
    elif mode == 'sigmoid_brain':
        return window_image(dcm, 40, 80, resample, True)

def window_image(dcm, window_center, window_width, resample, sigmoid=False):
    img = dcm.pixel_array * dcm.RescaleSlope + dcm.RescaleIntercept
    if sigmoid:
        U = 1.0
        eps = (1.0 / 255.0)
        ue = np.log((U / eps) - 1.0)
        W = (2 / window_width) * ue
        b = ((-2 * window_center) / window_width) * ue
        z = W * img + b
        img = U / (1 + np.power(np.e, -1.0 * z))    
        img = (img - np.min(img)) / (np.max(img) - np.min(img))
    else:
        img_min = window_center - window_width // 2
        img_max = window_center + window_width // 2
        img = np.clip(img, img_min, img_max)


    # resampling
    # Determine current pixel spacing
    if resample:
        new_spacing = [1, 1]
        spacing = np.array(dcm.PixelSpacing, dtype=np.float32)
        
        resize_factor = spacing / new_spacing
        new_real_shape = img.shape * resize_factor
        new_shape = np.round(new_real_shape)
        real_resize_factor = new_shape / img.shape
        new_spacing = spacing / real_resize_factor
        
        img = scipy.ndimage.interpolation.zoom(img, real_resize_factor, mode='nearest')

    return img

def bsb_window(dcm, resample=False):
    brain_img = window_image(dcm, 40, 80, resample)
    subdural_img = window_image(dcm, 80, 200, resample)
    bone_img = window_image(dcm, 600, 2000, resample)
    brain_img = min_max(brain_img, 40, 80)
    subdural_img = min_max(brain_img, 80, 200)
    bone_img = min_max(brain_img, 600, 2000)

    img = np.array([brain_img, subdural_img, bone_img]).transpose(1,2,0)
    return img

preprocess('./data/test.dcm', org='brain', windowing='bsb', resample=True, visualize=False, save=True)