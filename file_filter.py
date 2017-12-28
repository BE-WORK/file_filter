# -*- coding: utf-8 -*-

import os
import random


def select_files(folder_path):
    # 将Windows路径格式转换成Python路径格式
    folder_path = '/'.join(folder_path.split('\\'))
    if folder_path[len(folder_path) - 1] != '/':
        folder_path += '/'

    files = os.listdir(folder_path)
    files.sort()

    # 先创建2个列表，列表的元素还是列表，其中一个列表用于分类，另一个用于标记
    file_list = list()
    for i in range(20):
        file_list.append(list())
    mark_list = list()
    for i in range(20):
        mark_list.append([0] * 30)

    # 遍历文件，将文件分成20个类别，每个类别只含有一种网页
    page_type = 0
    cnt = 0
    for file in files:
        file_list[page_type].append(file)
        cnt += 1
        if cnt == 30:
            cnt = 0
            page_type += 1

    # 遍历每一个列表，标记出异常文件
    for i in range(20):  # 遍历20个类别
        for j, file in enumerate(file_list[i]):  # 遍历每个类别中的每个文件
            cnt = 0
            for k in range(10):  # 随机选择当前类别的10个文件和当前文件比较大小
                if abs(os.path.getsize(folder_path + file) - os.path.getsize(
                        folder_path + file_list[i][random.randint(0, 29)])) > 102400:
                    cnt += 1
            if cnt > 5:  # 如果和超过半数文件大小差异大，则判为异常，进行标记
                mark_list[i][j] = 1

    # 检测，如果有超过10个不正常文件，则说明数据本身可能有问题
    wrong = False
    for i in range(20):
        cnt = 0
        for mark in mark_list[i]:
            cnt += mark
        print cnt
        if cnt > 10:
            wrong = True
            print 'There may be something wrong with "' + '-'.join(file_list[i][0].split('-')[0:2]) + '"'
    if wrong:  # 如果数据本身有问题，则退出
        return

    # 遍历文件，剔除异常文件
    for i in range(20):
        for j in range(30)[::-1]:  # 每个类别对应的列表从后往前遍历
            if mark_list[i][j] == 1:
                os.remove(folder_path + file_list[i][j])
                file_list[i].pop(j)

        if len(file_list[i]) > 20:  # 如果有多余文件，则删除
            for k in range(10):
                if len(file_list[i]) > 20:
                    os.remove(folder_path + file_list[i][len(file_list[i]) - 1])
                    file_list[i].pop()

    # 遍历文件，重命名文件
    for i in range(20):
        idx = 41
        for j, file in enumerate(file_list[i]):  # 先将文件集重命名到一个没有冲突的名字范围
            src_name = folder_path + file
            dst_name = folder_path + '-'.join(file.split('-')[0:2]) + '-' + str(idx)
            os.rename(src_name, dst_name)
            file_list[i][j] = '-'.join(file.split('-')[0:2]) + '-' + str(idx)
            idx += 1

        for j, file in enumerate(file_list[i]):
            src_name = folder_path + file
            dst_name = folder_path + '-'.join(file.split('-')[0:2]) + '-' + str(j + 1) + '.pcap'
            os.rename(src_name, dst_name)
            file_list[i][j] = '-'.join(file.split('-')[0:2]) + '-' + str(j + 1) + '.pcap'


if __name__ == '__main__':
    folder_path = raw_input("Please enter the path of target folder(Windows Format):")
    select_files(folder_path)
