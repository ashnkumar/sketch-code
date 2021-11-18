from __future__ import absolute_import

import os
import sys
import shutil

import numpy as np
from PIL import Image
import cv2
from tensorflow.keras.preprocessing.image import ImageDataGenerator

class ImagePreprocessor:

    def __init__(self):
        pass

    def build_image_dataset(self, data_input_folder, augment_data=True):

        print("Converting images from {} into arrays, augmentation: {}".format(data_input_folder, augment_data))
        resized_img_arrays, sample_ids = self.get_resized_images(data_input_folder)

        if augment_data == 1:
            self.augment_and_save_images(resized_img_arrays, sample_ids, data_input_folder)
        else:
            self.save_resized_img_arrays(resized_img_arrays, sample_ids, data_input_folder)

    def get_img_features(self, png_path):
        img_features = self.resize_img(png_path)
        assert(img_features.shape == (256,256,3))
        return img_features


   ##########################################
   ####### PRIVATE METHODS ##################
   ##########################################



    def save_resized_img_arrays(self, resized_img_arrays, sample_ids, output_folder):
        count = 0
        for img_arr, sample_id in zip(resized_img_arrays, sample_ids):
            npz_filename = "{}/{}.npz".format(output_folder, sample_id)
            np.savez_compressed(npz_filename, features=img_arr)
            retrieve = np.load(npz_filename)["features"]
            assert np.array_equal(img_arr, retrieve)
            count += 1
        print("Saved down {} resized images to folder {}".format(count, output_folder))
        del resized_img_arrays

    def augment_and_save_images(self, resized_img_arrays, sample_ids, data_input_folder):
        datagen = ImageDataGenerator(
                                 rotation_range=2,
                                 width_shift_range=0.05,
                                 height_shift_range=0.05,
                                 zoom_range=0.05
                                )
        keras_generator = datagen.flow(resized_img_arrays,sample_ids,batch_size=1)
        count = 0
        for i in range(len(resized_img_arrays)):
            img_arr, sample_id = next(keras_generator)
            img_arr = np.squeeze(img_arr)
            npz_filename = "{}/{}.npz".format(data_input_folder, sample_id[0])
            im = Image.fromarray(img_arr.astype('uint8'))
            np.savez_compressed(npz_filename, features=img_arr)
            retrieve = np.load(npz_filename)["features"]
            assert np.array_equal(img_arr, retrieve)
            count += 1
        print("Saved down {} augmented images to folder {}".format(count, data_input_folder))
        del resized_img_arrays

    def get_resized_images(self, pngs_input_folder):
        all_files = os.listdir(pngs_input_folder)
        png_files = [f for f in all_files if f.find(".png") != -1]
        images = []
        labels = []
        for png_file_path in png_files:
            png_path = "{}/{}".format(pngs_input_folder, png_file_path)
            sample_id = png_file_path[:png_file_path.find('.png')]
            resized_img_arr = self.resize_img(png_path)
            images.append(resized_img_arr)
            labels.append(sample_id)
        return np.array(images), np.array(labels)

    def resize_img(self, png_file_path):
        img_rgb = cv2.imread(png_file_path)
        img_grey = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        img_adapted = cv2.adaptiveThreshold(img_grey, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, 101, 9)
        img_stacked = np.repeat(img_adapted[...,None],3,axis=2)
        resized = cv2.resize(img_stacked, (200,200), interpolation=cv2.INTER_AREA)
        bg_img = 255 * np.ones(shape=(256,256,3))
        bg_img[27:227, 27:227,:] = resized
        bg_img /= 255
        return bg_img


































