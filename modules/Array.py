# coding: utf-8

import os
import numpy as np

from PIL import Image


class Array(object):

    # 常量设置，代表矩阵4个方向的边
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
            return 'Array object of {}'.format(self.image_path)
        else:
            return 'Empty Array object'

    def hjoin(self, other):
        """
        水平合并
        :param other: <Array> 参与合并的另一个 Array 对象
        :return: <Array> 合并后的 Array 对象
        """
        return Array().load_array(np.hstack((self.image_array, other.image_array)))

    def vjoin(self, other):
        """
        垂直合并
        :param other: <Array> 参与合并的另一个 Array 对象
        :return: <Array> 合并后的 Array 对象
        """
        return Array().load_array(np.vstack((self.image_array, other.image_array)))

    def load_image(self, image_path):
        """
        加载图片
        :param image_path: <str> 图片的路径
        :return: <Array> self
        """
        self.image_path = image_path

        # 检测图片是否存在
        if not os.path.exists(image_path):
            print('No such a image')
            return self

        # 生成 image 对象
        self.image_obj = Image.open(image_path).convert('RGB')
        self.width = self.image_obj.size[0]
        self.height = self.image_obj.size[1]
        self.image_to_array()
        del self.image_obj
        return self

    def image_to_array(self):
        """
        将图片转换成矩阵
        :return: <Array> self
        """
        # np.sum(array, axis=2)
        # 沿第二个坐标轴求和
        # 最终生成图片的灰度矩阵
        self.image_array = np.sum(np.asarray(self.image_obj), axis=2) // 3
        return self

    def binary(self):
        """
        图片二值化
        :return: <Array> self
        """
        self.image_array = self.image_array // 128
        return self

    def convert_to_image(self, image_path):
        image_array = self.image_array
        image = Image.fromarray(image_array.astype(np.uint8))
        image.save(image_path)

    def load_array(self, array):
        self.image_array = np.array(array)
        return self

    def get_edge(self, direction):
        """
        得到图像矩阵的边缘向量
        :param direction: 对应的边缘
        :return: <array> 边缘向量
        """
        if direction == Array.LEFT:
            return self.image_array[:, 0]
        elif direction == Array.TOP:
            return self.image_array[0]
        elif direction == Array.RIGHT:
            return self.image_array[:, self.width - 1]
        elif direction == Array.BOTTOM:
            return self.image_array[self.height - 1]
        else:
            return self.image_array[:, 0]

    def match(self, array=None, direction=2, kernel=(0.1, 0.8, 0.1)):
        """
        计算余弦相似度
        :param image:
        :return:
        """
        begin_edge = self.get_edge(direction) / 255
        white_edge = np.array([1] * len(begin_edge))
        end_edge = array.get_edge((direction + 2) % 4) / 255 if array else white_edge
        # begin_edge = self.convolution(begin_edge, np.array(kernel))
        # end_edge = self.convolution(end_edge, np.array(kernel))

        cos_theta = np.dot(begin_edge, end_edge) / np.linalg.norm(begin_edge) / np.linalg.norm(end_edge)
        return cos_theta

        # edge_diff = begin_edge - end_edge
        # counter = 0
        # for diff in edge_diff:
        #     if diff < 0.1:
        #         counter += 1
        # return counter / len(begin_edge)

    def convolution(self, vector, kernel):
        kernel = kernel / sum(kernel)
        new_vector = vector.copy()
        vector_len = len(vector)
        kernel_len = len(kernel)
        center_index = kernel_len // 2

        for x in range(vector_len):
            new_value = 0
            begin_index = center_index - x if center_index - x >= 0 else 0
            end_index = center_index + vector_len - x if center_index + vector_len - x < kernel_len else kernel_len - 1
            for y in range(begin_index, end_index):
                new_value += vector[x + y - center_index] * kernel[y]
            new_vector[x] = new_value

        return new_vector
