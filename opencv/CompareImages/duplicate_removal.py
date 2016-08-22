# -*- coding: utf-8 -*-
from skimage.measure import structural_similarity as ssim
import cv2
import os
import numpy as np

similar = 0.8  # 确定相似度，大于此数值的图片说明重复，删掉
images_path = '/media/wac/a74b0c6a-d07e-4a3f-b9b8-8796e932fce5/cornetto/'

def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])

	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

def traverse_dir(rootDir):
    images = []
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        print path
        images.append(path)
        if os.path.isdir(path):
            traverse_dir(path)
    return images


def Compare_images(imageA, imageB):
    # compute the mean squared error and structural similarity
	# index for the images
    imageA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    imageB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
    m = mse(imageA, imageB)
    s = ssim(imageA, imageB)
    return m,s


images_path = traverse_dir(images_path)

deleted_images = []
for image_path in images_path:
    try:
        img = cv2.imread(image_path)
        if (img.shape[0] > 500000):
            continue
        # print img.shape
    except:
        continue

    # img_height = np.size(img, 0)
    # img_width = np.size(img, 1)
    for image_path_in in images_path:
        try:
            img_in = cv2.imread(image_path_in)
            if (img.shape[0] > 500000):
                continue
        except:
            continue
        # img_in_height = np.size(img_in, 0)
        # img_in_width = np.size(img_in, 1)

        if (img is not None and img.shape is not None and img_in.shape is not None and img.shape == img_in.shape):  #尺寸一样才比对
            m,s = Compare_images(imageA=img,imageB=img_in)
            if (s>similar and image_path != image_path_in):   #大于此数值，文件名不相同的图片说明重复，删掉
                    print s,image_path,image_path_in
                    os.remove(image_path_in)
                    print "Deleted image:"+image_path_in