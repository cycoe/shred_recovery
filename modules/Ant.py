# coding: utf-8

import random


class Ant(object):

    def __init__(self, id, site_num):
        self.id = id
        self.site_num = site_num
        self.__init_data()

    def __init_data(self):
        """
        初始化蚂蚁的数据
        :return:
        """
        self.path = []
        self.total_cost = 0.0
        self.move_count = 0
        self.locale = -1

        locale = random.randint(0, self.site_num - 1)
        self.locale = locale
        self.path.append(locale)
        self.move_count += 1

    def move(self, locale):
        self.locale = locale
        self.path.append(locale)
        self.move_count += 1