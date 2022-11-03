import os
import  re as re
import csv

file_info=[
    {
        'folder_path':'D:\skyrat\Skyrat-tg-master\code\game\objects\items',
        're_list':['(?<=name = ".improper ).*(?=")','(?<=name = ".proper ).*(?=")','(?<=name = ").*(?=")','(?<=desc = ").*(?=")'],
        'file_name':'text.csv',
        'filetree_name':'file_tree.csv',
        'encoding':'UTF-8',
        'id':'True'
    }
    ,
    {
        'folder_path': 'D:\skyrat\Skyrat-tg-master\code\game\objects\structures',
        're_list': ['(?<=name = ".improper ).*(?=")', '(?<=name = ".proper ).*(?=")', '(?<=name = ").*(?=")','(?<=desc = ").*(?=")'],
        'file_name': 'structures_text.csv',
        'filetree_name': 'structures_file_tree.csv',
        'encoding':'UTF-8',
        'id':'True'
    }
    ,
    {
        'folder_path': 'D:\skyrat\Skyrat-tg-master\code\game\objects\effects',
        're_list': ['(?<=name = ".improper ).*(?=")', '(?<=name = ".proper ).*(?=")', '(?<=name = ").*(?=")','(?<=desc = ").*(?=")'],
        'file_name': 'effects_text.csv',
        'filetree_name': 'effects_file_tree.csv',
        'encoding':'UTF-8',
        'id':'True'
    }
    ,
    {
        'folder_path':r'D:\skyrat\Skyrat-tg-master\tgui\packages\tgui\interfaces',
        're_list': ['(?<=title=").*(?=")','(?<=content=").*(?=")'],
        'file_name':'interface_text.csv',
        'filetree_name':'interface_file_tree.csv',
        'encoding':'UTF-8',
        'id':'False'
    }
    ,
    {
        'folder_path':'D:\skyrat\Skyrat-tg-master\code\modules',
        're_list':['(?<=name = ".improper ).*(?=")','(?<=name = ".proper ).*(?=")','(?<=name = ").*(?=")','(?<=desc = ").*(?=")'],
        'file_name':'modules_text.csv',
        'filetree_name':'modules_file_tree.csv',
        'encoding':'UTF-8',
        'id':'True',
        'ban_filetype':'png'
    }
    ,
    {
        'folder_path':'D:\skyrat\Skyrat-tg-master\code\game\machinery',
        're_list':['(?<=name = ".improper ).*(?=")','(?<=name = ".proper ).*(?=")','(?<=name = ").*(?=")','(?<=desc = ").*(?=")'],
        'file_name':'machinery_text.csv',
        'filetree_name':'machinery_file_tree.csv',
        'encoding':'UTF-8',
        'id':'True'
    }
    ,
    {
        'folder_path':r'D:\skyrat\Skyrat-tg-master\code\game\turfs',
        're_list':['(?<=name = ".improper ).*(?=")','(?<=name = ".proper ).*(?=")','(?<=name = ").*(?=")','(?<=desc = ").*(?=")'],
        'file_name':'turfs_text.csv',
        'filetree_name':'turfs_file_tree.csv',
        'encoding':'UTF-8',
        'id':'True'
    }
    ,
    {
        'folder_path':r'D:\skyrat\Skyrat-tg-master\strings',
        're_list': ['.*'],
        'file_name':'string_txt_text.csv',
        'filetree_name':'string_txt_file_tree.csv',
        'encoding':'UTF-8',
        'id':'False',
        'ban_filetype':['json','toml']
    }
]

#返回[匹配内容，正则表达式，匹配物品]
def search_file(file_path,re_list,id_tf,encoding):
    global count
    try:
        f=open(file_path,'r',encoding=encoding)
    except UnicodeDecodeError:
        f=open(file_path, 'rb', encoding=encoding)
    result=[]
    tmp_string=''
    #用来检查一个id是否已经存在,仅在id不存在时生效
    id_check_list=[]
    try:
        for string in f.readlines():
            if id_tf=='False':
                id=re.match('.*',tmp_string).group()
            if list(string)[0]=='/' and id_tf=='True':
                id=re.match('.*',string).group()
            for r_e in re_list:
                matchre=re.compile(r_e)
                match=matchre.search(string)
                if match!=None and match not in result:
                    result.append([match.group(0),r_e,id])
                    count+=1
                    break
            #传递到下一次迭代
            if string not in id_check_list:
                tmp_string=string
                id_check_list.append(string)
        f.close()
        return result
    except UnicodeDecodeError:
        print('读取'+file_path+'时出现编码错误')

def search_folder(folder_path,re_list,id_tf,encoding,ban_filetype):
    result={}
    for root,dirs,files in os.walk(folder_path):
        for file_name in files:
            if re.search(".([a-z|A-Z]*?)$",file_name).group(1) not in ban_filetype:
                result.update({root+'\\'+file_name:search_file(root+'\\'+file_name,re_list,id_tf,encoding)})
    return result

#f_info[匹配内容，正则表达式，匹配物品]
def write_file(file_path,file_tree,id_tf,encoding):
    global count,count_id
    try:
        f = open(file_path, 'r', encoding=encoding)
    except FileNotFoundError:
        print(file_path+'处文件不存在（可能是在更新中被删除)')
        return
    #change_f是需要改变并写入文件的文本
    change_f=f.readlines()
    f_info=file_tree[file_path]
    #增加一次迭代，防止迭代溢出
    f_info.append([None,None,None])
    id=None
    text_list=[]
    for i in range(len(f_info)):
        #匹配了一个新物品的id，开始写入上一物品
        if (id!=f_info[i][2] and id!=None):
            count_id += 1
            text_iter=iter(text_list)
            text,r_e=next(text_iter)
            switch=False
            for line in range(len(change_f)):
                old_file_line=list(change_f[line])
                if re.match('.*', change_f[line]).group() == id:
                    switch=True
                #按id写入
                elif change_f[line][0]=='/' and id_tf=='True':
                    switch=False
                #找到了写入的位置，开始按顺序写入正则表达式对应内容
                if switch:
                    match=re.search(r_e,change_f[line])
                    if match!=None:
                        old_file_line=old_file_line[:match.span()[0]]+list(text)+old_file_line[match.span()[1]:]
                        count+=1
                        #不按id写入，按上一文本写入，写入完后就终止
                        if id_tf=='False':
                            switch=False
                        try:
                            text, r_e = next(text_iter)
                        except StopIteration:
                            break
                change_f[line]=''.join(old_file_line)
            text_list=[]
        id = f_info[i][2]
        text_list.append((f_info[i][0], f_info[i][1]))
    f.close()
    fw = open(file_path, 'w', encoding='UTF-8')
    for line in change_f:
        fw.write(line)
    fw.close()

def read_folder(folder_path,filetree_name,file_name,re_list,id_tf,encoding='UTF-8',ban_filetype=None):
    if ban_filetype == None:
        ban_filetype=[]
    file_tree = search_folder(folder_path,re_list,id_tf,encoding,ban_filetype)
    with open(filetree_name, 'w', newline='', encoding='UTF-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['文件路径', '正则表达式'])
        for file in file_tree.keys():
            for line in file_tree[file]:
                writer.writerow([file, line[1], line[2]])
    with open(file_name, 'w', newline='', encoding='UTF-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['索引', '文本内容', '翻译内容'])
        index = iter(range(100000000))
        for file in file_tree.keys():
            for line in file_tree[file]:
                writer.writerow([next(index), line[0], ''])

def write_tree(file_name,filetree_name,id_tf,encoding='UTF-8'):
    with open(filetree_name, 'r', newline='', encoding='UTF-8') as csvfile:
        tree_reader = csv.reader(csvfile)
        with open(file_name, 'r', newline='', encoding='UTF-8') as text:
            text_reader = csv.reader(text)
            new_file_tree = {}
            # i的结构((文件路径，正则表达式，物品id)，(索引，文本内容）)
            for i in zip(tree_reader, text_reader):
                if i[0][0] == '文件路径':
                    continue
                if len(i[1]) == 2:
                    new_text = i[1][1]
                elif i[1][2] == '':
                    new_text = i[1][1]
                else:
                    new_text = i[1][2]
                if i[0][0] in new_file_tree:
                    new_file_tree[i[0][0]].append([new_text, i[0][1], i[0][2]])
                else:
                    new_file_tree[i[0][0]] = [[new_text, i[0][1], i[0][2]]]

    for file_path in new_file_tree.keys():
        write_file(file_path, new_file_tree,id_tf,encoding)

#储存结构{绝对路径：【【文本内容，正则表达式】，【。。。】，，。。。。】，绝对路径：【。。。】}
if __name__=='__main__':
    enter='None'
    while enter!='q':
        enter=str(input('输入r读出文件，输入w写入文件，输入q退出:'))
        print('操作中')
        if enter=='r':
            for info in file_info:
                count = 0
                if info.get('ban_filetype')==None:
                    read_folder(info['folder_path'],info['filetree_name'],info['file_name'],info['re_list'],info['id'],info['encoding'])
                else:
                    read_folder(info['folder_path'],info['filetree_name'],info['file_name'],info['re_list'],info['id'],info['encoding'],info['ban_filetype'])
                print(info['file_name'] + '读取出' + str(count) + '个词条')
        elif enter=='w':
            for info in file_info:
                count = 0
                count_id = 0
                write_tree(info['file_name'],info['filetree_name'],info['id'],info['encoding'])
                print(info['file_name']+'已写入'+str(count)+'个词条 '+str(count_id)+'个id')