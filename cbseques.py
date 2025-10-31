## 24ia
# print(d['Raj'])
# ## 24 ib
# len(d1)
# ## 24 ii a
# d1.update(d)
# ## 24 ii b 
# d1.pop('amit')
# ## 25
# B
## 26 
def sum(n):
    s=0
    for i in range(1,n+1):
        s=s+i
    return s
# print(sum(10))
## 29 a
def elections():
    with open ("Election.txt",'a+') as f:
        d=f.readlines()
        for i in d:
            for j in range (len(i)):
                if i[j] == 'vote':
                    print(i)
# elections()
## 29 b
def reports():
    with open ("Election.txt",'r') as f:
        d=f.read()
        for i in d:
            if i[0] and i[-1] in 'AEIOUaeiou':
                print(i,end=' ')
# reports()
## 30 a
def push(stk,clr):
    stk.extend(clr)
    print(stk)
def pop_clr(stk):
    try:
        print(stk.pop())
    except:
        print("Underflow")
def is_empty(stk):
    if len(stk)==0:
        return True
    else:
        return False
stk=[2,3,4,5]
clr=[9,8]
push(stk,clr)
pop_clr(stk)

## 30 b
# def push_trail(N,mystack):
#     for i in range(len(N)):
#         if i >= 5:
#             mystack.append(i) 
# def pop_one
## 31a
# i=G,e,n,X
# c=0,1,2,3
# str=gGnngGn
## 33
import csv
def read_data():
    with open('p_rec.csv', mode='r', newline='') as file:
        q = csv.reader(file)
        p = list(q)
        print("cancer patients")
        print(p[0]) ## header 
        for i in range(1,len(p)):
            if p[i][1] == "Cancer":
                print(p[i])
def count_rec():
    with open('p_rec.csv', mode='r', newline='') as file:
        q = csv.reader(file)
        p = list(q)
    print (f"the no of records in file,{len(p)-1}")
## 36
import pickle
def create():
    with open('data.pkl', mode='wb') as file:
            
        ans ='y'
        data = []
        while ans == 'y':
            pnr = input("Enter your pnr: ")
            pname = input("Enter your pname: ")
            brdstn = input("Enter your brdstn: ")
            dest=input("Enter ur destn:")
            fare=int(input("Enter ur fare:"))
            data.append([pnr,pname,brdstn,dest,fare])
            ans = input("Do you want to add another record? (y/n): ").lower()
            if ans != 'y':
                print("Exiting...")
        pickle.dump(data, file)
        print("Data written to data.pkl")