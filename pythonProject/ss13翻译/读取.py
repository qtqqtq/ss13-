import os
import re
import csv

folder_path='D:\skyrat\Skyrat-tg-master\code\game\objects\items'
re_list=['(?<=name = ".improper ).*(?=")','(?<=name = ".proper ).*(?=")','(?<=name = ").*(?=")','(?<=desc = ").*(?=")']

#返回[匹配内容，正则表达式，匹配物品]
def search_file(file_path):
    f=open(file_path,'r',encoding='UTF-8')
    stat=os.stat(file_path)
    result=[]
    for string in f.readlines():
        if list(string)[0]=='/':
            id=re.match('.*',string).group()
        for r_e in re_list:
            match=re.search(r_e,string)
            if match!=None and match not in result:
                result.append([match.group(),r_e,id])
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
    text,r_e,id=next(f_string)
    switch=False
    for line in range(len(change_f)):
        old_file_line=list(change_f[line])
        if re.match('.*',change_f[line]).group()==id:
            switch=True
        elif line=='\n':
            switch=False
        if switch:
            match=re.search(r_e,change_f[line])
            if match!=None:
                old_file_line=old_file_line[:match.span()[0]]+list(text)+old_file_line[match.span()[1]:]
                try:
                    text,r_e,id=next(f_string)
                except StopIteration:
                    pass
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
            file_tree = search_folder(folder_path)
            with open('file_tree.csv', 'w', newline='',encoding='UTF-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['文件路径','正则表达式'])
                for file in file_tree.keys():
                    for line in file_tree[file]:
                        writer.writerow([file,line[1],line[2]])
            with open('text.csv', 'w', newline='',encoding='UTF-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['索引','文本内容','翻译内容'])
                index=iter(range(100000000))
                for file in file_tree.keys():
                    for line in file_tree[file]:
                        writer.writerow([next(index),line[0],''])
        elif enter=='w':
            with open('file_tree.csv', 'r', newline='',encoding='UTF-8') as csvfile:
                tree_reader = csv.reader(csvfile)
                with open('text.csv', 'r', newline='', encoding='UTF-8') as text:
                    text_reader = csv.reader(text)
                    new_file_tree={}
                    #i的结构((文件路径，正则表达式，物品id)，(索引，文本内容）)
                    for i in zip(tree_reader,text_reader):
                        if i[0][0]=='文件路径':
                            continue
                        if len(i[1])==2:
                            new_text=i[1][1]
                        elif i[1][2]=='':
                            new_text=i[1][1]
                        else:new_text=i[1][2]
                        if i[0][0] in new_file_tree:
                            new_file_tree[i[0][0]].append([new_text,i[0][1],i[0][2]])
                        else:
                            new_file_tree[i[0][0]]=[[new_text,i[0][1],i[0][2]]]

            for file_path in new_file_tree.keys():
                write_file(file_path,new_file_tree)

