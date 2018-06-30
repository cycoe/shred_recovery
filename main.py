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
import time
import numpy as np

from modules.Array import Array
from modules.Ant import Ant


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print('function <{}> running for {} seconds'.format(func.__name__, str(end - start)))
        return result
    return wrapper


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


def select_from_prob(vector, path):
    vector = vector.copy()
    for locale in path:
        vector[locale] = 0
    pointer = random.random() * sum(vector)
    for index in range(len(vector)):
        pointer -= vector[index]
        if pointer <= 0:
            return index

def cost_cal(cost_matrix, path):
    cost = 0
    for index in range(len(path) - 1):
        cost += cost_matrix[path[index]][path[index + 1]]
    return cost

@timer
def ants_algorithm():
    array_pool = []
    image_path_ = os.listdir('res/attachments/1/')
    random.shuffle(image_path_)  # 对样本池进行洗牌，测试算法稳定性
    for index in range(len(image_path_)):
        array = Array().load_image('res/attachments/1/' + image_path_[index])
        array_pool.append(array)

    alpha = 1
    beta = 2
    decay = 0.5
    site_num = len(array_pool)
    pheromone_ant = site_num
    site_cost = 1 - np.array([[array_pool[y].match(array_pool[x], Array.RIGHT) for x in range(site_num)] for y in range(site_num)])
    site_pheromone = np.array([[1] * site_num] * site_num)

    best_cost = 1000
    best_path = []
    for cycle in range(20):
        pheromone_temp = np.array([[0 for x in range(site_num)] for y in range(site_num)])
        for ant_index in range(20):
            ant = Ant(cycle, site_num)
            for move in range(site_num - 1):
                site_prob = site_pheromone[ant.locale] ** alpha * (0.1 / (site_cost[ant.locale] + 0.1)) ** beta
                next_site = select_from_prob(site_prob, ant.path)
                ant.move(next_site)

            total_cost = cost_cal(site_cost, ant.path)

            if cost_cal(site_cost, ant.path) < best_cost:
                best_cost = total_cost
                best_path = ant.path

            pheromone_per_cost = 2 / total_cost

            for index in range(site_num - 1):
                previous = ant.path[index]
                next = ant.path[index + 1]
                pheromone_temp[previous][next] += pheromone_per_cost

        site_pheromone = site_pheromone * decay
        site_pheromone += pheromone_temp

    image_join = array_pool[best_path[0]]
    for index in range(1, site_num):
        image_join = image_join.hjoin(array_pool[best_path[index]])
    image_join.convert_to_image('test.jpg')

if __name__ == '__main__':
    ants_algorithm()