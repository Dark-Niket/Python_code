import tkinter as tk
import ast
def rotation():
    m = ast.literal_eval(en.get())
 
    p=[]

    for i in range (len(m)):
        l=[]
        for j in m:
            l.append(j[i])
        p.append(l[::-1])


    

    label.config(text=f'matrix after rot {p}')
root=tk.Tk()
root.title("Matrix rot")
tk.Label(root, text="Matrix after rot:").pack(pady=5)
en=tk.Entry(root)
en.pack(pady=5, padx=10)
tk.Button(root, text="rotate it", command=rotation).pack(pady=5)
label = tk.Label(root, text="")
label.pack(pady=5)
root.mainloop()