# coding=UTF-8
import xlrd
import xlwt
import numpy as np
from xlutils.copy import copy

# 新建表格
def excel_int(path, sheet_name):
    workbook = xlwt.Workbook()  # 新建一个工作簿
    workbook.add_sheet(sheet_name)  # 在工作簿中新建一个表格
    workbook.save(path)  # 保存工作簿
    print("新建表格成功，表格名称为：",path)

# 写入表头
def excel_write_title(path, titels):
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    for j in range(0, len(titels)):
        new_worksheet.write(0, j, "".join(titels[j]))  # 表格中写入数据（对应的行）
    new_workbook.save(path)  # 保存工作簿

# 向表格按列写入一维数组（列表）插入
def excel_write_array(path, value, column):
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    for i in range(0, len(value)):
        # 向表格中写入数据（对应的列），初始位置加1（因为有表头）
        new_worksheet.write(i+1, column, float(value[i]))
    new_workbook.save(path)  # 保存工作簿

# 向表格按列写入一维数组（插入字符串列表）
def excel_write_array_str(path, value, column):
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    for i in range(0, len(value)):
        # 向表格中写入数据（对应的列），初始位置加1（因为有表头）

        new_worksheet.write(i+1, column, "".join(value[i]))
    new_workbook.save(path)  # 保存工作簿