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

from modules.ImageUtils import ImageUtils


def main():
    image_obj_ = []

    max_left = 0
    max_left_index = 0
    image_path_ = os.listdir('res/attachments/2/')
    for index in range(len(image_path_)):
        image_obj = ImageUtils().open('res/attachments/2/' + image_path_[index])
        image_obj.image_to_array().binary()
        if sum(image_obj.get_edge(ImageUtils.LEFT)) > max_left:
            max_left = sum(image_obj.get_edge(ImageUtils.LEFT))
            max_left_index = index

        image_obj_.append(image_obj)

    join_image = image_obj_[max_left_index]
    del image_obj_[max_left_index]

    while True:
        max_match = 0
        max_match_index = 0
        for index in range(len(image_obj_)):
            current_match = join_image.match(image_obj_[index])
            if current_match > max_match:
                max_match = current_match
                max_match_index = index

        join_image = join_image + image_obj_[max_match_index]
        print(image_obj_[max_match_index])
        del image_obj_[max_match_index]

        if not image_obj_:
            break

    join_image.convert_to_image('test.jpg')

if __name__ == '__main__':
    main()