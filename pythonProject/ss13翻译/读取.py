import os
import re
import csv
import pandas as pd

def search_file(file_path):
    re_list=['(?<=name = ".improper ).*(?=")','(?<=name = ".proper ).*(?=")','(?<=name = ").*(?=")','(?<=desc = ").*(?=")']
    f=open(file_path,'r',encoding='UTF-8')
    stat=os.stat(file_path)
    result=[]
    for string in f.readlines():
        for r_e in re_list:
            match=re.search(r_e,string)
            if match!=None and match not in result:
                result.append([match.group(),r_e])
                break
    f.close()
    return result

def search_folder(folder_path):
    result={}
    for root,dirs,files in os.walk(folder_path):
        for file_name in files:
            result.update({root+'\\'+file_name:search_file(root+'\\'+file_name)})
    return result

def write_file(file_path,file_tree):
    f = open(file_path, 'r', encoding='UTF-8')
    #change_f是需要改变并写入文件的文本
    change_f=f.readlines()
    f_string=iter(file_tree[file_path])
    text,r_e=next(f_string)
    for line in range(len(change_f)):
        old_file_line=list(change_f[line])
        ls=re.search(r_e,change_f[line])
        if ls!=None:
            old_file_line=old_file_line[:ls.span()[0]]+list(text)+old_file_line[ls.span()[1]:]
            try:
                text,r_e=next(f_string)
            except StopIteration:
                break
        change_f[line]=''.join(old_file_line)
    f.close()
    fw = open(file_path, 'w', encoding='UTF-8')
    for line in change_f:
        fw.write(line)
    fw.close()

#储存结构{绝对路径：【【文本内容，正则表达式】，【。。。】，，。。。。】，绝对路径：【。。。】}
if __name__=='__main__':
    enter='None'
    while enter!='q':
        enter=str(input('输入r读出文件，输入w写入文件，输入q退出:'))
        print('操作中')
        if enter=='r':
            file_tree = search_folder(r'D:\skyrat\Skyrat-tg-master\code\game\objects\items')
            with open('file_tree.csv', 'w', newline='',encoding='GB18030') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['文件路径','文本内容','正则表达式'])
                for file in file_tree.keys():
                    for line in file_tree[file]:
                        writer.writerow([file,line[0],line[1]])
            csv = pd.read_csv('file_tree.csv', encoding='GB18030')
            csv.to_excel('file_tree.xlsx', sheet_name='data')
        elif enter=='w':
            data_xls = pd.read_excel('file_tree.xlsx', index_col=0)
            data_xls.to_csv('file_tree.csv', encoding='GB18030')
            with open('file_tree.csv', 'r', newline='',encoding='GB18030') as csvfile:
                reader = csv.reader(csvfile)
                new_file_tree={}
                #i的结构(文件路径，文本内容,正则表达式)
                for i in reader:
                    if i[1]=='文件路径':
                        continue
                    if i[1] in new_file_tree:
                        new_file_tree[i[1]].append([i[2],i[3]])
                    else:
                        new_file_tree[i[1]]=[[i[2],i[3]]]

            for file_path in new_file_tree.keys():
                write_file(file_path,new_file_tree)

