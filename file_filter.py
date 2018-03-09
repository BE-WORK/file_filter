# -*- coding: utf-8 -*-

import os
import random


def select_files(folder_path, num_page=20, num_src_file=30, num_target_file=20):
    # 将Windows路径格式转换成Python路径格式
    folder_path = '/'.join(folder_path.split('\\'))
    if folder_path[len(folder_path) - 1] != '/':
        folder_path += '/'

    files = os.listdir(folder_path)
    files.sort()

    # 先创建2个列表，列表的元素还是列表，其中一个列表用于分类，另一个用于标记
    file_list = list()
    for i in range(num_page):
        file_list.append(list())
    mark_list = list()
    for i in range(num_page):
        mark_list.append([0] * num_src_file)

    # 遍历文件，将文件分成num_page个类别，每个类别只含有一种网页
    page_type = 0
    cnt = 0
    for file_name in files:
        file_list[page_type].append(file_name)
        cnt += 1
        if cnt == num_src_file:
            cnt = 0
            page_type += 1

    # 标记异常文件
    size_diff = 51200  # 初始化的文件大小差异为512KB
    # 遍历每一个列表，标记出异常文件
    for i in range(num_page):  # 遍历num_page个网页
        for j, file_name in enumerate(file_list[i]):  # 遍历每个网页对应的每个文件
            cnt = 0
            for k in range(num_src_file - num_target_file):  # 随机选择当前网页的num_src_file-num_target_file个文件和当前文件比较大小
                if abs(os.path.getsize(folder_path + file_name) - os.path.getsize(
                        folder_path + file_list[i][random.randint(0, num_src_file - 1)])) > size_diff:
                    cnt += 1
            if cnt > (num_src_file - num_target_file) / 2:  # 如果和超过半数文件大小差异大，则判为异常，进行标记
                mark_list[i][j] = 1

        # 标记完当前网页的异常文件之后，进行统计
        num_outlier = 0
        for mark in mark_list[i]:
            num_outlier += mark
        if num_outlier <= num_src_file - num_target_file:
            print str(num_outlier) + '(' + str(size_diff / 1024) + 'KB)' + '-'.join(file_list[i][0].split('-')[0:2])
        else:  # 对于当前网页，文件大小差异较大，需调整size_diff的值继续筛选
            this_size_diff = size_diff
            print str(num_outlier) + '(' + str(this_size_diff / 1024) + 'KB)' + '-'.join(
                file_list[i][0].split('-')[0:2])
            while True:
                # 将当前网页对应的异常文件标记置0
                for m in range(len(mark_list[i])):
                    mark_list[i][m] = 0

                # 增大size_diff，对当前网页继续筛选
                this_size_diff += 51200
                for j, file_name in enumerate(file_list[i]):  # 遍历当前网页的每个文件
                    cnt = 0
                    for k in range(
                            num_src_file - num_target_file):  # 随机选择当前网页的num_src_file-num_target_file个文件和当前文件比较大小
                        if abs(os.path.getsize(folder_path + file_name) - os.path.getsize(
                                folder_path + file_list[i][random.randint(0, num_src_file - 1)])) > this_size_diff:
                            cnt += 1
                    if cnt > (num_src_file - num_target_file) / 2:  # 如果和超过半数文件大小差异大，则判为异常，进行标记
                        mark_list[i][j] = 1

                # 重新统计增大size_diff的值后，当前网页异常文件的数量
                num_outlier = 0
                for mark in mark_list[i]:
                    num_outlier += mark
                print str(num_outlier) + '(' + str(this_size_diff / 1024) + 'KB)' + '-'.join(
                    file_list[i][0].split('-')[0:2])
                if num_outlier <= num_src_file - num_target_file:  # 可以筛选出当前网页的目标文件，退出while循环
                    break

    # 遍历文件，剔除异常文件
    for i in range(num_page):
        for j in range(num_src_file)[::-1]:  # 每个类别对应的列表从后往前遍历
            if mark_list[i][j] == 1:
                os.remove(folder_path + file_list[i][j])
                file_list[i].pop(j)

        if len(file_list[i]) > num_target_file:  # 如果有多余文件，则删除
            for k in range(10):
                if len(file_list[i]) > num_target_file:
                    os.remove(folder_path + file_list[i][len(file_list[i]) - 1])
                    file_list[i].pop()

    # 遍历文件，重命名文件
    for i in range(num_page):
        idx = num_src_file + 1
        for j, file_name in enumerate(file_list[i]):  # 先将文件集重命名到一个没有冲突的名字范围
            src_name = folder_path + file_name
            dst_name = folder_path + '-'.join(file_name.split('-')[0:2]) + '-' + str(idx)
            os.rename(src_name, dst_name)
            file_list[i][j] = '-'.join(file_name.split('-')[0:2]) + '-' + str(idx)
            idx += 1

        for j, file_name in enumerate(file_list[i]):
            src_name = folder_path + file_name
            dst_name = folder_path + '-'.join(file_name.split('-')[0:2]) + '-' + str(j + 1) + '.pcap'
            os.rename(src_name, dst_name)
            file_list[i][j] = '-'.join(file_name.split('-')[0:2]) + '-' + str(j + 1) + '.pcap'


if __name__ == '__main__':
    parameter = raw_input(
        "请按以下格式输入参数，其中文件夹路径是Windows格式。\nFolder_Path Number_Page Number_Src_File Number_Target_File\n:")
    parameters = parameter.split(' ')
    if len(parameters) == 1:
        select_files(parameter)
    else:
        select_files(parameters[0], int(parameters[1]), int(parameters[2]), int(parameters[3]))
