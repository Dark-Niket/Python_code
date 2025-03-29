m=int(input("Enter the no of terms for the tribonacci series:"))
a = 0 
b = 1
c = 1 
d = 0
print(f'{a},\n{b},\n{c}')
for i in range(m-1):
    d = a+b+c
    print(f'{d},')
    a = b
    b = c
    c = d 

