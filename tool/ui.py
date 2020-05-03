import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import *
import sys
import numpy as numpy
import subprocess
import uiBackEnd.script as scriptToRun
import uiBackEnd.singleRepo as singleRepo
import uiBackEnd.singleUser as singleUser

def fetchSingleRepo(entries, vars, v, root):
    selection = v.get()
    if selection != "2":
        mess = "Wrong Button Pressed/Selected"
        tk.messagebox.showwarning('Error',mess)
        return
    
    entry = entries[0]
    username = entry[2].get()

    entry = entries[1]
    password = entry[2].get()

    privateInc = vars[0].get()
    print(privateInc)
    if privateInc == 0:
        privateInc = 1
    else:
        privateInc = 0

    b4['state'] = 'disabled'
    singleRepo.singleRepoAnalysis(username,password,privateInc)

def fetchSingleUser(entries, vars, v, root):
    selection = v.get()
    if selection != "3":
        mess = "Wrong Button Pressed/Selected"
        tk.messagebox.showwarning('Error',mess)
        return
    
    entry = entries[0]
    username = entry[2].get()

    entry = entries[1]
    password = entry[2].get()

    privateInc = vars[0].get()
    print(privateInc)
    if privateInc == 0:
        privateInc = 1
    else:
        privateInc = 0

    b5['state'] = 'disabled'
    singleUser.singleUserAnalysis(username,password,privateInc)

def fetch(entries, vars, v, root):

    selection = v.get()
    print(selection)
    if selection != "1":
        mess = "Wrong Button Pressed/Selected"
        tk.messagebox.showwarning('Error',mess)
        return

    entry = entries[0]
    toshow = 1
    field = entry[1]
    text  = entry[2].get()
    topic = text
    print('%s    %s: "%s"' % (toshow, field, text))
    print(" ")
    


    entry = entries[1]
    toshow = vars[0].get()
    field = entry[1]
    text  = entry[2].get()
    try:
        temp = int(text)
    except ValueError:
        mess = "The number of stars can only be a positive integer"
        tk.messagebox.showwarning('Processing Over',mess)
        return
    temp = int(text)
    if temp < 0:
        mess = "The number of stars can only be a positive integer"
        tk.messagebox.showwarning('Processing Over',mess)
        return
    stars = text
    if toshow == 0:
        stars = -1
    print('%s    %s: "%s"' % (toshow, field, text))
    print(" ")

    entry = entries[2]
    toshow = vars[1].get()
    field = entry[1]
    text  = entry[2].get()
    try:
        temp = int(text)
    except ValueError:
        mess = "The number of forks can only be a positive integer"
        tk.messagebox.showwarning('Processing Over',mess)
        return
    temp = int(text)
    if temp < 0:
        mess = "The number of forks can only be a positive integer"
        tk.messagebox.showwarning('Processing Over',mess)
        return
    forks = text
    if toshow == 0:
        forks = -1
    print('%s    %s: "%s"' % (toshow, field, text))
    print(" ")

    entry = entries[3]
    toshow = vars[2].get()
    field = entry[1]
    text  = entry[2].get()
    try:
        temp = int(text)
    except ValueError:
        mess = "The number of contributors can only be a positive integer"
        tk.messagebox.showwarning('Processing Over',mess)
        return
    temp = int(text)
    if temp < 0:
        mess = "The number of contributors can only be a positive integer"
        tk.messagebox.showwarning('Processing Over',mess)
        return
    cont = text
    if toshow == 0:
        cont = -1
    print('%s    %s: "%s"' % (toshow, field, text))
    print(" ")

    entry = entries[4]
    toshow = vars[3].get()
    field = entry[1]
    text  = entry[2].get()
    try:
        temp = int(text)
    except ValueError:
        mess = "The number of releases can only be a positive integer"
        tk.messagebox.showwarning('Processing Over',mess)
        return
    temp = int(text)
    if temp < 0:
        mess = "The number of releases can only be a positive integer"
        tk.messagebox.showwarning('Processing Over',mess)
        return
    rel = text
    if toshow == 0:
        rel = -1
    print('%s    %s: "%s"' % (toshow, field, text))
    
    print(" ")
    print("Starting the Script")
    b1["state"] = "disabled"
    # b2["state"] = "disabled"
    # x = input()
    root.destroy
    scriptToRun.code(topic,stars,forks,cont,rel)

def showHelp():
    subprocess.Popen("BTP-Paper.pdf",shell=True)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("400x450")

    v = tk.StringVar(root,"0")
    row = tk.Frame(root)
    row.pack(side=tk.TOP,anchor='w',padx=30)
    Radiobutton(row,text="Big Data",variable=v,value="1").pack(side=tk.LEFT)
    # root.bind("<Return>", (lambda event, e=ents, v=vars: fetch(e,v,root)))   

    entries = []
    vars = []

    varStars = tk.IntVar()
    varFork = tk.IntVar()
    varCont = tk.IntVar()
    varRel = tk.IntVar()

    # first row to be topic editor
    row = tk.Frame(root, width = 400)
    row.pack(side=tk.TOP,anchor='w',padx=60)
    lab = tk.Label(row,text="Topic")
    lab.pack(side=tk.LEFT)
    ent = tk.Entry(row)
    ent.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)
    entries.append((1,"Topic",ent))

    #  second row to be number of stars
    row = tk.Frame(root, width = 400)
    row.pack(side=tk.TOP,anchor='w',padx=60)
    tk.Checkbutton(row,text="Number of Stars: ",variable=varStars).pack(side=tk.LEFT)
    ent = tk.Entry(row)
    ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
    entries.append((varStars.get(),"Stars",ent))

    #  third row to be number of forks
    row = tk.Frame(root, width = 400)
    row.pack(side=tk.TOP,anchor='w',padx=60)
    tk.Checkbutton(row,text="Number of Forks: ",variable=varFork).pack(side=tk.LEFT)
    ent = tk.Entry(row)
    ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
    entries.append((varFork.get(),"Forks",ent))

    #  fourth row to be number of contributors
    row = tk.Frame(root, width = 400)
    row.pack(side=tk.TOP,anchor='w',padx=60)
    tk.Checkbutton(row,text="Number of Contributors: ",variable=varCont).pack(side=tk.LEFT)
    ent = tk.Entry(row)
    ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
    entries.append((varCont.get(),"Cont",ent))

    #  fifth row to be number of stars
    row = tk.Frame(root, width = 400)
    row.pack(side=tk.TOP,anchor='w',padx=60)
    tk.Checkbutton(row,text="Number of Releases: ",variable=varRel).pack(side=tk.LEFT)
    ent = tk.Entry(row)
    ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
    entries.append((varRel.get(),"Release",ent))

    vars.append(varStars)
    vars.append(varFork)
    vars.append(varCont)
    vars.append(varRel)

    row = tk.Frame(root, width = 400)
    row.pack(side=tk.TOP,anchor='w',padx=80)
    b1 = tk.Button(row, text='Start',
                  command=(lambda e=entries, va=vars, v=v: fetch(e,va,v,root)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    # b2 = tk.Button(row, text='Quit', command=root.destroy)
    # b2.pack(side=tk.LEFT, padx=5, pady=5)
    # b3 = tk.Button(row, text='Help',
    #               command=(showHelp))
    # b3.pack(side=tk.LEFT, padx=5, pady=5)


    # -------------------------------------------------------------------------------------------------------------------

    entriesForRepo = []
    varsForRepo = []

    row = tk.Frame(root)
    row.pack(side=tk.TOP,anchor='w',padx=30)
    Radiobutton(row,text="Single Repository",variable=v,value="2").pack(side=tk.LEFT)

    row = tk.Frame(root, width = 400)
    row.pack(side=tk.TOP,anchor='w',padx=60)
    lab = tk.Label(row,text="Username ")
    lab.pack(side=tk.LEFT)
    ent = tk.Entry(row)
    ent.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)
    entriesForRepo.append((1,"Username",ent))
    
    row = tk.Frame(root, width = 400)
    row.pack(side=tk.TOP,anchor='w',padx=60)
    lab = tk.Label(row,text="Access Code ")
    lab.pack(side=tk.LEFT)
    ent = tk.Entry(row)
    ent.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)
    entriesForRepo.append((1,"Password",ent))

    varIncPriv = tk.IntVar()
    row = tk.Frame(root, width = 400)
    row.pack(side=tk.TOP,anchor='w',padx=60)
    tk.Checkbutton(row,text="Include Private Repos",variable=varIncPriv).pack(side=tk.LEFT)
    varsForRepo.append(varIncPriv)

    row = tk.Frame(root, width = 400)
    row.pack(side=tk.TOP,anchor='w',padx=80)
    b4 = tk.Button(row, text='Start',
                  command=(lambda e=entriesForRepo, va=varsForRepo, v=v: fetchSingleRepo(e,va,v,root)))
    b4.pack(side=tk.LEFT, padx=5, pady=5)

    # ----------------------------------------------------------------------------------------

    entriesForUser = []
    varsForUser = []

    row = tk.Frame(root)
    row.pack(side=tk.TOP,anchor='w',padx=30)
    Radiobutton(row,text="Single User",variable=v,value="3").pack(side=tk.LEFT)

    row = tk.Frame(root, width = 400)
    row.pack(side=tk.TOP,anchor='w',padx=60)
    lab = tk.Label(row,text="Username ")
    lab.pack(side=tk.LEFT)
    ent = tk.Entry(row)
    ent.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)
    entriesForUser.append((1,"Username",ent))
    
    row = tk.Frame(root, width = 400)
    row.pack(side=tk.TOP,anchor='w',padx=60)
    lab = tk.Label(row,text="Access Code ")
    lab.pack(side=tk.LEFT)
    ent = tk.Entry(row)
    ent.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)
    entriesForUser.append((1,"Password",ent))

    varIncPriv = tk.IntVar()
    row = tk.Frame(root, width = 400)
    row.pack(side=tk.TOP,anchor='w',padx=60)
    tk.Checkbutton(row,text="Include Private Repos",variable=varIncPriv).pack(side=tk.LEFT)
    varsForUser.append(varIncPriv)

    row = tk.Frame(root, width = 400)
    row.pack(side=tk.TOP,anchor='w',padx=80)
    b5 = tk.Button(row, text='Start',
                  command=(lambda e=entriesForUser, va=varsForUser, v=v: fetchSingleUser(e,va,v,root)))
    b5.pack(side=tk.LEFT, padx=5, pady=5)

    root.mainloop()