#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Justin
#
# Created:     17-10-2015
# Copyright:   (c) Justin 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from Tkinter import*
import tkMessageBox
import Tkinter
from tkFileDialog import askdirectory
from tkFileDialog import askopenfilename
from os import listdir
from os.path import isfile, join
import photo_editor
import thread
import os

pathGUIInputDir = None
pathGUIOutputDir = None
pathGUIBackground1 = None
pathGUIBackground2 = None
windowGUITopLayer = None
alive = True
fileQueue = list()

def on_closing():
    global alive
    global windowGUITopLayer
    thread.exit_thread
    alive = False
    windowGUITopLayer.destroy()


def background1_select():
    global pathGUIBackground1
    pathGUIBackground1 = askopenfilename()

def background2_select():
    global pathGUIBackground2
    pathGUIBackground2 = askopenfilename()


def input_select():
    global pathGUIInputDir
    pathGUIInputDir = askdirectory()
    print(pathGUIInputDir)
def output_select():
    global pathGUIOutputDir
    pathGUIOutputDir = askdirectory()
    print(pathGUIOutputDir)
    if not os.path.exists(pathGUIOutputDir + "/Bad"):
        print("there")
        os.makedirs(pathGUIOutputDir + "/Bad")
    if not os.path.exists(pathGUIOutputDir + "/Good"):
        os.makedirs(pathGUIOutputDir + "/Good")
    if not os.path.exists(pathGUIOutputDir + "/CSV"):
        os.makedirs(pathGUIOutputDir + "/CSV")
def search_files():
    global alive
    while (alive):
        onlyfiles = [ f for f in listdir(pathGUIInputDir) if isfile(join(pathGUIInputDir,f)) ]
        for f in onlyfiles:
            # extention = os.path.splitext(f)[1]
            if f not in fileQueue: #and extention is ".bmp":
                fileQueue.append(f)

def start_proccess():
    global fileQueue
    global pathGUIInputDir
    global pathGUIOutputDir
    if(pathGUIInputDir is not None and pathGUIOutputDir is not None):
        print("hi")
        onlyfiles = [ f for f in listdir(pathGUIInputDir) if isfile(join(pathGUIInputDir,f)) ]
        for f in onlyfiles:
            extention = os.path.splitext(f)[1]
            print extention
            if f not in fileQueue and extention == ".bmp":
                fileQueue.append(f)
        photo_editor.execute(fileQueue, pathGUIInputDir, pathGUIOutputDir)



def main():
    global pathGUIInputDir
    global pathGUIOutputDir
    global windowGUITopLayer

    windowGUITopLayer = Tkinter.Tk()
    windowGUITopLayer.protocol("WM_DELETE_WINDOW", on_closing)
    menuButtonGUISettings = Menubutton( windowGUITopLayer, text = "Settings", relief=RAISED)
    menuButtonGUISettings.grid()
    menuButtonGUISettings.menu = Menu (menuButtonGUISettings, tearoff = 0)
    menuButtonGUISettings["menu"] = menuButtonGUISettings.menu

    menuButtonGUISettings.menu.add_command (label = "Input Location",
                                         command = input_select)

    menuButtonGUISettings.menu.add_command (label = "Output Location",
                                         command = output_select)

    menuButtonGUISettings.menu.add_command (label = "background1",
                                         command = background1_select)

    menuButtonGUISettings.menu.add_command (label = "background2",
                                         command = background2_select)
    menuButtonGUISettings.pack()

    buttonGUIStart = Tkinter.Button(windowGUITopLayer, text = "Start",
                                    command = start_proccess).pack()

    windowGUITopLayer.mainloop()

    pass

if __name__ == '__main__':
    main()
