

import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

window=tk.Tk()
window.title("Attandace system ")
window.config(background="yellow")
X=tk.Label(window,text="Name",font=('Algerian',20),bg='yellow')
X.grid(column=1,row=0)
X1=tk.Entry(window,width=50,bd=5)
X1.grid(column=2,row=0)

Y=tk.Label(window,text="id",font=('Algerian',20),bg='yellow')
Y.grid(column=1,row=1)
Y1=tk.Entry(window,width=50,bd=5)
Y1.grid(column=2,row=1)

Z=tk.Label(window,text="Branch",font=('Algerian',20),bg='yellow')
Z.grid(column=1,row=2)
Z1=tk.Entry(window,width=50,bd=5)
Z1.grid(column=2,row=2)

def exit():
    cv2.destroyAllWindows()

b1=tk.Button(window,text="EXIT",font=("Argerian",16),bg='black',fg='red',command=exit)
b1.grid(column=1,row=4)



def mark():
    path='images'
    images=[]
    classNames=[]
    mylist=os.listdir(path)
    for img in mylist:
        currrent_image=cv2.imread(f'{path}/{img}')
        images.append(currrent_image)
        classNames.append(os.path.splitext(img)[0])

    def findencoding(images):
        encodeList=[]
        for img in images:
            tempimg=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            encode=face_recognition.face_encodings(tempimg)[0]
            print(encode)
            encodeList.append(encode)
        return encodeList

    def attendance(name):
        with open('attendance.csv','r+') as f:
            mydatalist=f.readlines()
            namelist=[]
            for line in mydatalist:
                entry=line.split(',')
                namelist.append(entry[0])
            arr = name.split('$')
            if arr[1] not in namelist:
                now =datetime.now()
                str=now.strftime('%D:%H:%M:%S')
                f.writelines(f'\n{arr[1]},{arr[0],arr[2],str}')


    encodingList= findencoding(images)
    print(len(encodingList))
    cap=cv2.VideoCapture(0)
    timer=int(100)
    while timer>0:
        success,img=cap.read()
        imgs=cv2.resize(img,(0,0),None,0.25,0.25)
        imgs=cv2.cvtColor(imgs,cv2.COLOR_BGR2RGB)

        facescurframe=face_recognition.face_locations(imgs)
        encocodecurrframe=face_recognition.face_encodings(imgs,facescurframe)

        for encodeFace,faceloc in zip(encocodecurrframe,facescurframe):
            matches=face_recognition.compare_faces(encodingList,encodeFace)
            facedis=face_recognition.face_distance(encodingList,encodeFace)
            matchid=np.argmin(facedis)

            if matches[matchid]:
                name=classNames[matchid].upper()
                y1,x2,y2,x1=faceloc
                y1, x2, y2, x1=y1*4,x2*4,y2*4,x1*4;
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-70),(x2,y2+70),(0,255,0),cv2.FILLED)
                arr = name.split('$')
                text = 'name= ' + arr[0] +' id= ' + arr[2]
                cv2.putText(img,text,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                attendance(name)
        timer-=1
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(timer),
                    (200, 250), font,
                    2, (0, 255, 0),
                    2, cv2.LINE_AA)
        cv2.imshow('webcam',img)
        cv2.waitKey(1)

b2=tk.Button(window,text="Mark-attendance",font=("Argerian",16),bg='black',fg='white',command=mark)
b2.grid(column=2,row=4)

def define_dataset():
    if(X1.get()=='' or Y1.get()=='' or Z1.get()==''):
        messagebox.showerror("error","provide information ")
        return
    camera = cv2.VideoCapture(0)
    while (True):
        ret, frame = camera.read()
        cv2.imshow('Capture Image --> press `Q`', frame)
        if (cv2.waitKey(1) & 0xFF == ord('q')):
            cv2.imwrite('F:/pycharm/Face_Recognition_attandace_System/images/' + X1.get() + '$' + Y1.get() + '$' + Z1.get() + '.png',frame)
            camera.release()
            break
    cv2.destroyAllWindows()

b3=tk.Button(window,text="new Register",font=("Argerian",16),bg='black',fg='white',command=define_dataset)
b3.grid(column=3,row=4)



window.geometry("800x500")
window.mainloop()


