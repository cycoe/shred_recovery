# coding: utf-8

import os
import numpy as np

from PIL import Image


class ImageUtils(object):

    LEFT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3

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

    def __add__(self, other):
        return ImageUtils().load_array(np.hstack((self.image_array, other.image_array)))

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

    def convert_to_image(self, image_path):
        image_array = self.image_array * 255
        image = Image.fromarray(image_array.astype(np.uint8))
        image.save(image_path)

    def load_array(self, array):
        self.image_array = array
        return self

    def binary(self):
        self.image_array = self.image_array // 128
        return self

    def get_edge(self, axis=0):
        """
        得到图像矩阵的边缘向量
        :param axis: 对应的边缘
        :return: <array> 边缘向量
        """
        if axis == ImageUtils.LEFT:
            return self.image_array[:, 0]
        elif axis == ImageUtils.TOP:
            return self.image_array[0]
        elif axis == ImageUtils.RIGHT:
            return self.image_array[:, self.width - 1]
        elif axis == ImageUtils.BOTTOM:
            return self.image_array[self.height - 1]
        else:
            return self.image_array[:, 0]

    def match(self, image):
        """
        计算余弦相似度
        :param image:
        :return:
        """
        right_edge = self.get_edge(ImageUtils.RIGHT)
        left_edge = image.get_edge(ImageUtils.LEFT)
        cos_theta = np.dot(right_edge, left_edge) / np.linalg.norm(right_edge) / np.linalg.norm(left_edge)
        return 0.5 + 0.5 * cos_theta