import os
import re
import csv

def search_file(file_path):
    f=open(file_path,'r',encoding='UTF-8')
    stat=os.stat(file_path)
    result=[]
    for line in range(stat.st_size):
        string=f.readline()
        match_name=re.search('(?<=name = ").*(?=")',string)
        match_desc=re.search('(?<=desc = ").*(?=")',string)
        if match_name!=None:result.append([line,match_name.span(),match_name.group(),'name'])
        if match_desc!=None:result.append([line,match_desc.span(),match_desc.group(),'desc'])
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
    change_f=f.readlines()
    f_string=file_tree[file_path]
    for line,span,string in f_string:
        old_file_line=list(change_f[line])
        #将旧文本中的第span[0]+3个元素到span[1]+3个元素替换为file_tree中的键值（正则表达式对象）的group属性
        old_file_line=old_file_line[:span[0]]+list(string)+old_file_line[span[1]:]
        change_f[line]=''.join(old_file_line)
    f.close()
    fw = open(file_path, 'w', encoding='UTF-8')
    for line in change_f:
        fw.write(line)
    fw.close()

#储存结构{绝对路径：【【行数，文本起始位置，文本内容】，【。。。】，，。。。。】，绝对路径：【。。。】}
if __name__=='__main__':
    file_tree=search_folder(r'D:\skyrat\Skyrat-tg-master(3)\Skyrat-tg-master\code\game\objects\items')
    enter='None'
    while enter!='q':
        enter=str(input('输入r读出文件，输入w写入文件，输入q退出:'))
        if enter=='r':
            with open('file_tree.csv', 'w', newline='',encoding='GB18030') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['文件路径','行数','字符串位置','文本内容'])
                for file in file_tree.keys():
                    for line in file_tree[file]:
                        writer.writerow([file,line[0],line[1],line[2]])
        elif enter=='w':
            with open('file_tree.csv', 'r', newline='',encoding='GB18030') as csvfile:
                reader = csv.reader(csvfile)
                new_file_tree={}
                #i的结构(文件路径，行数，文本始末位置，文本内容)
                for i in reader:
                    if i[0]=='文件路径':
                        continue
                    pattern = re.compile(r'\d+')  # 查找数字
                    span = pattern.findall(i[2])
                    if i[0] in new_file_tree:
                        new_file_tree[i[0]].append([int(i[1]),(int(span[0]),int(span[1])),i[3]])
                    else:
                        new_file_tree[i[0]]=[[int(i[1]),(int(span[0]),int(span[1])),i[3]]]
            for file_path in new_file_tree.keys():
                write_file(file_path,new_file_tree)
        print('操作中')
