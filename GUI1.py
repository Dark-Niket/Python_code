import tkinter as tk
def unique_words():
    s1=en.get()
    s2=en2.get()
    s3=s1.split()
    s4=s2.split()
    l=[]
    for i in s3:
        continue
    for j in s4:
        continue
    if i !=j:
        l.append(i)
        l.append(j)
    label.config(text=f'Unique words {l}')
root=tk.Tk()
root.title("Unique words in two sentences")
tk.Label(root, text="Unique words in two sentences:").pack(pady=5)
en = tk.Entry(root)
en.pack(pady=5, padx=10)
en2= tk.Entry(root)
en2.pack(pady=5, padx=10)

tk.Button(root, text="find unique words", command=unique_words).pack(pady=5)
label = tk.Label(root, text="")
label.pack(pady=5)

root.mainloop()















s1="this apple is sweet"
s2 = "this apple is sour"
s3=s1.split()
s4=s2.split()
print(s3, s4)
l=[]
for i in s3:
    print("s1",i)
for j in s4:
    print("s2",j)
if i !=j:
    print(i,j)
    l.append(i)
    l.append(j)
print(l)
        # if i!=j:
#             print(i,j)
#             l.append(i)
#             l.append(j)
# print(l)
        
