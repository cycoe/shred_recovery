# coding: utf-8

import os
import numpy as np

from PIL import Image


class ImageUtils(object):

    def __init__(self):
        self.image_path = None
        self.image_obj = None
        self.image_array = None

        self.width = 0
        self.height = 0

    def __str__(self):
        if self.image_path:
            return 'ImageUtils object of {}'.format(self.image_path)
        else:
            return 'Empty ImageUtils object'

    def open(self, image_path):
        self.image_path = image_path
        if not os.path.exists(image_path):
            print('No such a image')
            return self

        self.image_obj = Image.open(image_path).convert('RGB')
        self.width = self.image_obj.size[0]
        self.height = self.image_obj.size[1]
        self.black_array = np.zeros(self.image_obj.size)
        self.white_array = np.ones(self.image_obj.size) * 255
        return self

    def image_to_array(self):
        if not self.image_obj:
            return self

        self.image_array = np.sum(np.asarray(self.image_obj), axis=2) // 3
        return self

    def binary(self):
        if not self.image_array:
            self.image_to_array()
        self.image_array = np.where(
            self.image_array > 127,
            self.white_array,
            self.black_array
        )
        return self
    