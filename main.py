# -*- coding: utf-8 -*-
import cv2
import numpy as np
from tkinter import filedialog
import tkinter as tk
from PIL import ImageTk, Image
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from itertools import zip_longest
def nest_list(list1,rows, columns):    
        result=[]               
        start = 0
        end = columns
        for i in range(rows): 
            result.append(list1[start:end])
            start +=columns
            end += columns
        return result
def btcoding(image, height, width, bs):
    lheight, lwidth = int(height/bs), int(width/bs)
    m = bs*bs
    for i in range(0, lheight):
        for j in range(0, lwidth):
            tempImg = image[i*bs:i*bs+bs,j*bs:j*bs+bs]
            mean = cv2.meanStdDev(tempImg)[0]
            std = cv2.meanStdDev(tempImg)[1]
            '''
            展示第一個 block
            '''
            if(i+j==0):
                print(tempImg)
            for x in range(0, bs):
                for y in range(0, bs):
                    if tempImg[x][y] > mean:
                        tempImg[x][y] = 1
                    else:
                        tempImg[x][y] = 0
            sumPos = np.float32(np.sum(tempImg))
            if(sumPos == 0):
                sumPos = 1
            l = mean - (std * np.sqrt(float(sumPos)/abs(m - sumPos)))
            h = mean + (std * np.sqrt(float(m-sumPos)/abs(sumPos)))
            t = 5
            if(abs(l-h)>t):
                for x in range(0, bs):
                    for y in range(0, bs):
                        if tempImg[x][y] == 1:
                            image[i*bs+x][j*bs+y] = h
                        else:
                            image[i*bs+x][j*bs+y] = l
            if(abs(l-h)<t):
                ls =[0,1,0,0,0,1,1,0]
                mt = []
                mtc = []
                for x in range(bs):
                    for y in range(bs):
                        mt.append(tempImg[x][y])
                for z,w in zip(mt,ls):
                    if(z!=w):
                        z = w
                    if(z==w):
                        z = z
                    mtc.append(z)
                mt[0:len(ls)] = mtc
                new = nest_list(mt, 4, 4)
                for x in range(0, bs):
                    for y in range(0, bs):
                        if new[x][y] == 1:
                            image[i*bs+x][j*bs+y] = h
                        else:
                            image[i*bs+x][j*bs+y] = l
    return np.uint8(image)
def cv_imread(filePath):
    cv_img=cv2.imdecode(np.fromfile(filePath,dtype=np.uint8),-1)
    return cv_img
def oas(filename):
    plt.cla()
    global b
    b = tk.Label(root)
    gray = cv2.cvtColor(cv2.resize(cv_imread(filename),(500,250)),cv2.COLOR_BGR2GRAY)
    g = cv2.cvtColor(cv2.resize(cv_imread(filename),(500,250)),cv2.COLOR_BGR2GRAY)
    g2 = cv2.cvtColor(cv2.resize(cv_imread(filename),(500,250)),cv2.COLOR_BGR2GRAY)
    y = np.zeros((256))
    for i in range(0,gray.shape[0]):
        for j in range(0,gray.shape[1]):
            y[gray[i,j]] += 1
    output=btcoding(g2,250,500,4)
    btc=Image.fromarray(output)
    imgtk = ImageTk.PhotoImage(image=btc)
    b = tk.Label(image=imgtk)
    b.pack()
    b.imgtk = imgtk
    b.configure(image = imgtk)
    cvphoto = Image.fromarray(g)
    imgtk = ImageTk.PhotoImage(image=cvphoto)
    media.imgtk = imgtk
    media.configure(image=imgtk)
    plt.bar(np.arange(0,256),y,color="gray",align="center")
    canva.draw()
def opfile():
    b.destroy()
    sfname = filedialog.askopenfilename(title='選擇',filetypes=[('All Files','*'),("jpeg files","*.jpg"),("png files","*.png"),("gif files","*.gif")])
    return sfname
def oand():
    filename = opfile()
    oas(filename)
def main():
    global root
    root = tk.Tk()
    global b
    b = tk.Label(root)
    mediaFrame = tk.Frame(root).pack()
    global media
    media = tk.Label(mediaFrame)
    media.pack()
    fig = plt.figure()
    plot =fig.add_subplot(111)
    global canva
    canva = FigureCanvasTkAgg(fig,root)
    canva.get_tk_widget().pack(side='right')
    b1 = tk.Button(root, text="打開",command = oand).pack()
    root.mainloop()
if __name__=='__main__':
    main()