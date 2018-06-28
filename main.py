#!/usr/bin/python3.6
# coding: utf-8

#
#                            _ooOoo_
#                           o8888888o
#                           88" . "88
#                           (| -_- |)
#                           O\  =  /O
#                        ____/`---'\____
#                      .'  \\|     |//  `.
#                     /  \\|||  :  |||//  \
#                    /  _||||| -:- |||||-  \
#                    |   | \\\  -  /// |   |
#                    | \_|  ''\---/''  |   |
#                    \  .-\__  `-`  ___/-. /
#                  ___`. .'  /--.--\  `. . __
#               ."" '<  `.___\_<|>_/___.'  >'"".
#              | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#              \  \ `-.   \_ __\ /__ _/   .-` /  /
#         ======`-.____`-.___\_____/___.-`____.-'======
#                            `=---='
#        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#                      Buddha Bless, No Bug !

import os
import random

from modules.Array import Array


def shred_horizontal():
    array_ = []

    max_left = 0
    max_left_index = 0
    image_path_ = os.listdir('res/attachments/1/')
    for index in range(len(image_path_)):
        array = Array().load_image('res/attachments/1/' + image_path_[index])
        if sum(array.get_edge(Array.LEFT)) > max_left:
            max_left = sum(array.get_edge(Array.LEFT))
            max_left_index = index

        array_.append(array)

    join_image = array_[max_left_index]
    del array_[max_left_index]

    while True:
        max_match = 0
        max_match_index = 0
        for index in range(len(array_)):
            current_match = join_image.match(array_[index])
            if current_match > max_match:
                max_match = current_match
                max_match_index = index

        join_image = join_image.hjoin(array_[max_match_index])
        print(array_[max_match_index])
        del array_[max_match_index]

        if not array_:
            break

    join_image.convert_to_image('test.jpg')

def shred_h_and_v():
    # 使用贪心算法
    # 生成样本池
    array_pool = []
    image_path_ = os.listdir('res/attachments/3/')
    random.shuffle(image_path_)  # 对样本池进行洗牌，测试算法稳定性
    for index in range(len(image_path_)):
        array = Array().load_image('res/attachments/3/' + image_path_[index])
        array_pool.append(array)

    row = 11
    column = 19
    array_matrix = [[object for x in range(column)]for y in range(row)]
    for y in range(row):
        for x in range(column):
            max_match = 0
            max_match_index = 0
            for index in range(len(array_pool)):
                match = 0
                match += array_pool[index].match(None if x == 0 else array_matrix[y][x - 1], Array.LEFT)
                match += array_pool[index].match(None if y == 0 else array_matrix[y - 1][x], Array.TOP)
                match += array_pool[index].match(None, Array.RIGHT) if x == column - 1 else 0
                match += array_pool[index].match(None, Array.BOTTOM) if y == row - 1 else 0

                if match > max_match:
                    max_match = match
                    max_match_index = index

            array_matrix[y][x] = array_pool[max_match_index]
            del array_pool[max_match_index]


    # 根据生成的 array_matrix 矩阵阵列合并图片
    image_join_ = []
    for y in range(row):
        image_row = array_matrix[y][0]
        for x in range(1, column):
            image_row = image_row.hjoin(array_matrix[y][x])
        image_join_.append(image_row)

    image_join = image_join_[0]
    for y in range(1, row):
        image_join = image_join.vjoin(image_join_[y])
    image_join.convert_to_image('test.jpg')


if __name__ == '__main__':
    shred_h_and_v()