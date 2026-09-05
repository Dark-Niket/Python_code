s=input("Enter a string:")
s1=s.split()
d={}
print(s1)
for i in s1:
    print(i)
    c=0
    for j in i:
        #print(j)
        if j in "AEIOUaeiou":
            c+=1
            print("the vowels",j)
            print ("The no of vowels:",c)
            d[i]=c
print(d)
d1=d.values()
print(d1)
d2=sorted(d1)
print(d2)
