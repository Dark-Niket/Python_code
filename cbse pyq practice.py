def remove_element():
    l = [2,3,4,55,6667,0]
    m = 0

    if m in l:
        l.remove(m)
        print("Found and removed!!")
    else:
        print("Element not found")

    print(l)  # to see updated list

remove_element()