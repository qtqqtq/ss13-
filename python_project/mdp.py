
class matrix_mdp:
    def __init__(self,size):
        self.size=size
        self.matrix_list=[[0]*size for i in range(size)]
    def nearxy(self,x,y):
        correct_x=x+1
        correct_y=y+1
        #如果x,y超出范围，将临近的点转移到左面或上面
        if x==self.size:
            correct_x=0
        if y==self.size:
            correct_y=0
        return [(x-1,y),(x,y-1),(correct_x,y),(x,correct_y)]
    def value_function(self):
if __name__=='__main__':
    mm=matrix_mdp(5)
    print(mm.matrix_list)
    print(mm.nearxy(5,5))