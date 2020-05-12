import numpy as np

mylist = []
with open('army.txt', "r") as fp:
    for i in fp.readlines():
        tmp = i.split(',')
        mylist.append((int(tmp[0]), int(tmp[1]), tmp[2].strip(), tmp[3].strip()))
        print((int(tmp[0]), int(tmp[1]), tmp[2].strip(), tmp[3].strip()))
