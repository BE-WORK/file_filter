# 简述
这是一个文件过滤工具，用于滤除采集的网页流量文件集中大小异常的文件。

# 环境
Windows 10 + Python 2 + Pycharm 2017.3

# 使用
直接运行脚本，根据提示输入对应的参数值。总共有Folder_Path Number_Page Number_Src_File Number_Target_File这4个参数，分别对应采集到的数据集所在的文件夹路径（Windows格式）、网页种类的数目、每种网页采集的文件数目、挑选的目标文件数目。第一个为必填参数，后3个为可选参数，默认为20，30，20，根据具体情况选择输入。程序的输出结果是对每一个网页，筛选出Number_Target_File个文件。