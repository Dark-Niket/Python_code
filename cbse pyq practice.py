def remove_element():
    l = [2,3,4,55,6667,0]
    m = 0

    if m in l:
        l.remove(m)
        print("Found and removed!!")
    else:
        print("Element not found")

    print(l)  

# remove_element()



def add_context():
    d={"Anita":78,"Diode":89,"Fob":45}
    for i in d :
        print (i)
# add_context()



def p_txt():
    with open ("Prog.txt" ,'w') as f:
        p="Python Python Python is \nPython jum \nPython miket \nPythonnije Python"
        f.write(p)

def p_read():
    with open("Prog.txt") as f:
        q = f.readlines()

        for i in q:
            words = i.split()
            c = words.count("Python")
            print(i.strip(), c)
# p_txt()
# p_read()
def read_story():
    with open("STORIES.TXT") as f:
        lines = f.readlines()

        vowels = "AEIOUaeiou"

        for line in lines:
            if line != "": 
                if line[0] not in vowels:
                    print(line.strip())



# read_story()

def push():
    L = [("Laptop", 90000), ("Mobile", 30000), ("Pen", 50), ("Headphones", 1500)]
    s=[]
    for i in L:
        if i[1]>50:
            s.append(i)
    print(s)
# push()
def popi():
    L = [("Laptop", 90000), ("Mobile", 30000), ("Pen", 50), ("Headphones", 1500)]
    while len(L)>0:
        p=L.pop()
        print(p)
    print("Stack Empty")
# popi()
s="NIKETBASUSUDIPBASUMOTUISHIDCJHWSD"
k=s.split("I"
)      
print(k)
    