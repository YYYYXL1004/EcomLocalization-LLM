from openpyxl import load_workbook
import pandas as pd
import numpy as np
import xlrd


# 基于文件名和表格名删除一些行和一些列，注意没有备份。
# flsh是指文件名flname和表格名sheetname
import XlsxToXls

def del_flsh_rows_cols(flname, sheetname, rowd):  # 基于文件名和表格名删除一些行和一些列
    """基于文件名和表格名删除一些行和一些列
    要删的行序数放在rowd表格中，要删的列序数放在cold表格中
    本程序的关键是删除的行或列序数都必须是从大的开始删除，这样才不会乱序"""
    wb = load_workbook(flname)
    #print(wb)
    ws = wb['Sheet1']
    #print(ws)
    rowd = sorted(rowd, reverse=True)
    #print(rowd)

    for r in rowd:
        #print(r)
        ws.delete_rows(r+1)
    wb.save(flname)# 记得要保存。
    print('删除结束')


def delete(fname,export_name,delete_flag): #传入delete_flag为false
    XlsxToXls.xlsx_to_xls(fname,export_name,delete_flag)

    # 读取文件，并记录关键字列为空的行数，存入数组中

    file = export_name
    book = xlrd.open_workbook(file)  # 打开工作簿
    print('当前工作表名称:', book.sheet_names())  # 输出当前工作表的名称
    sheet = book.sheet_by_index(0)  # sheet变量赋值为第1个工作表
    sheet_name = sheet[0]

    rows = sheet.nrows  # rows为行数
    cols = sheet.ncols  # cols为列数
    print('该工作表有%d行，%d列.' % (rows, cols))

    # 导入excel数据
    data_cutted = pd.read_excel(file, usecols=['content_cutted'])

    # 转化为list列表
    array_cutted = np.array(data_cutted)
    cutted_list = array_cutted.tolist()

    # 数组记录关键字列为空的行标
    num = []

    j = 1
    while j < rows:
        if len(sheet.cell_value(j, 3)) == 0:
            #print(j)
            num.append(j)
            #print('第二行第二列的单元格内容为:%s' % (sheet.cell_value(j, 3)))
        j += 1

    #print(num)

    del_flsh_rows_cols(fname, sheet_name, num)