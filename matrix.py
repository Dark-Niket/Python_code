##rotation by 90 degres
m= [[1,2,3],
    [4,5,6],
    [7,8,9]] ##sample matrix
def rotation():
    global m
 
    p=[]
    o=[]
    for i in range (len(m)):
        l=[]
        for j in m:
            l.append(j[i])
        p.append(l[::-1])


    

    print(p)
rotation()