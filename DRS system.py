'''
Author: Kunal
date: 24/09/2021
purpose: learning
'''
import tkinter
import time
import threading
from functools import partial
import cv2
import imutils
import PIL.Image, PIL.ImageTk
SET_WIDTH = 650
SET_HEIGHT = 368
stream = cv2.VideoCapture("lol.MP4")
flag = True
def play(speed):
    global flag
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)
    grabbed, frame = stream.read()
    if not grabbed:
        exit()
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    if flag:
        canvas.create_text(134,26, fill="black", font="Times 26 bold", text="Decision Pending")
    flag = not flag
def pending(decision):
    # 1. display decision pending
    frame = cv2.cvtColor(cv2.imread("decision_pending.jpg"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)
    # 2. Wait for 2 second
    time.sleep(2)
    # 3.display out/not out image
    if decision == "out":
        decision_image = "OUT.jpg"
    else:
        decision_image = "NOT_OUT.jpg"
    frame = cv2.cvtColor(cv2.imread(decision_image), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)

    pass
def out():
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon=1
    thread.start()
    print("Player is out")
def not_out():
    thread = threading.Thread(target=pending, args=("not out",))
    thread.daemon = 1
    thread.start()
    print("Player is not out")

# Tkinter gui starts here
window = tkinter.Tk()
window.title("KAGXXX'S Decision Review System")
cv_img = cv2.cvtColor(cv2.imread("in_progress.jpg"), cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0,0, anchor=tkinter.NW, image=photo)
canvas.pack()

#Buttons to control playback
btn = tkinter.Button(window, text="<< Backward(fast)", width=50, command=partial(play, -25))
btn.pack()

btn = tkinter.Button(window, text="<< Backward(slow)", width=50, command=partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text="Forward(fast) >>", width=50, command=partial(play, 25))
btn.pack()

btn = tkinter.Button(window, text="Forward(fast) >>", width=50, command=partial(play, 2))
btn.pack()

btn = tkinter.Button(window, text="out", width=50, command=out)
btn.pack()

btn = tkinter.Button(window, text="not out", width=50, command=not_out)
btn.pack()

window.mainloop()