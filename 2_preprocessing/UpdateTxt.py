

def updateTxt():
    file_write = open(r"E:\python_code\LDA\data\知网情感词典总和.txt", "w", encoding='utf-8')
    file_read = open(r"E:\python_code\LDA\data\知网正面情感词典.txt", "r", encoding='utf-8')
    file_read_F = open(r"E:\python_code\LDA\data\知网负面情感词典.txt", "r", encoding='utf-8')
    text_list = file_read.readlines()
    for index,str in enumerate(text_list):
        s=str.rstrip()
        print(s)
        file_write.write(s+' 1'+'\n')

    text_list_F=file_read_F.readlines()
    for index,str in enumerate(text_list_F):
        s=str.rstrip()
        print(s)
        file_write.write(s+' -1'+'\n')


    print('更新完成')

    file_write.close()
    file_read.close()
    file_read_F.close()

updateTxt()