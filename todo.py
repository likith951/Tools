import tkinter as tk
from functools import partial
from tkinter import font
from datetime import datetime



window = tk.Tk()
Tasks=[]
TimeStamps=[]
pos=[]
btncolors=[]
##
def writeData():
    file=open("todo.txt", "r")
    lines=file.readlines()
    for line in lines:
        temp=line.split("\0")
        p=int(temp[0])
        text=temp[1]
        time=temp[2]
        color = temp[3].strip() if len(temp) > 3 and temp[3].strip() else "#3498db"
        newtask(frames,btns,text,time,p,color)
    file.close()

def editText(checkbox):
    otext=checkbox.cget("text")
    print("triggred")
    checkbox.config(text=text.get())
    Tasks[Tasks.index(otext)]=text.get()
def getout(frame,checkbox,timestamp,TaskFrame):
    Tasks.remove(checkbox.cget("text"))
    TimeStamps.remove(timestamp.cget("text"))
    pos.remove(str(frames.index(frame)))
    TaskFrame.destroy()


def changeColor(btn,checkbox):
    btncolors[Tasks.index(checkbox.cget("text"))]="red"
    btn.config(bg="red")
def checked(cb):
    f = font.Font(font=cb.cget("font"))
    temp=f.actual("overstrike")
    if temp==0:
        f.configure(overstrike=1)
    else:
        f.configure(overstrike=0)

    cb.configure(font=f)

def edit(menu,btn):
    x=btn.winfo_rootx()
    y=btn.winfo_rooty()
    menu.tk_popup(x,y)

def get_time():
    i=btns.index(get_button(btns))
    if i==0:
        return str(datetime.now().strftime("%H:%M"))
    else:
        return str(datetime.now().strftime("%b %d"))

def get_button(btns):
    for btn in btns:
        if btn['relief'] == tk.FLAT:
            return btn
def newtask(frames,btns,text,Time=None,i=None,color="#3498db"):
    ##Genarilizing for writing:
    if hasattr(text,'get'):
        Text=text.get()
        time=get_time()
        btn = get_button(btns)
        frame = frames[btns.index(btn)]
        text.delete("0",tk.END)
    else:
        Text=text
        time=Time
        btn=btns[i]
        frame=frames[i]
    ###AddingCheckBoxes:
    TaskFrame=tk.Frame(frame,bg="#888888")
    checkBox = tk.Checkbutton(TaskFrame, text=Text,justify=tk.LEFT,bg="#888888",font=("Segoe UI", 10))
    timeStamp = tk.Label(TaskFrame, text=time,justify=tk.LEFT,bg="#888888",font=("Consolas", 9))
    editbtn=tk.Button(TaskFrame,justify=tk.RIGHT,bg=color)##
    checkBox.pack(side=tk.LEFT, fill=tk.BOTH,anchor=tk.N)
    timeStamp.pack(side=tk.LEFT, fill=tk.BOTH,anchor=tk.N)
    editbtn.pack(side=tk.RIGHT, fill=tk.BOTH,anchor=tk.N)
    editMenu=tk.Menu(TaskFrame,tearoff=0)
    editMenu.add_command(label="Edit Text",command=partial(editText,checkBox))
    editMenu.add_command(label="Change Color",command=partial(changeColor,editbtn,checkBox))
    editMenu.add_command(label="Delete",command=partial(getout,frame,checkBox,timeStamp,TaskFrame))
    TaskFrame.pack(side=tk.TOP, fill=tk.BOTH,anchor=tk.N)
    editbtn.config(command=partial(edit,editMenu,editbtn))
    checkBox.config(command=partial(checked, checkBox))
    ##storing data for writing
    Tasks.append(checkBox.cget("text"))
    TimeStamps.append(timeStamp.cget("text"))
    btncolors.append(editbtn.cget("bg"))
    pos.append(str(frames.index(frame)))
def tabMange(btns,frames,i):
    for j in range(len(btns)):
        btns[j].config(relief=tk.RAISED,bg="#007acc")
        frames[j].pack_forget()
        if j==i:
            btns[j].config(relief=tk.FLAT,bg="#00c853")
            frames[j].pack()
window.title("To-dos")
window.geometry("300x500")
window.configure(bg="#1e1e1e")
bar= tk.Frame(window, bg="#38383A",height=40)
bar.pack(side="bottom", fill="x")
text=tk.Entry(bar,bg="#2d2d2d",fg="#e0e0e0")
text.pack(side="left", fill="x", padx=1, pady=3,expand=True)


##adding tabs
tab_bar=tk.Frame(window, bg="white",height=40)
tab_bar.pack(side="top", fill="x")
##daily Tasks
dayButton=tk.Button(tab_bar,text="Daily",bg="#00c853",fg="white",font=("Arial", 11, "bold"))
dayButton.pack(side="left",expand=True,fill="both")
dayFrame=tk.Frame(window, bg="#38383A")
dayFrame.pack(side="top", fill="both",expand=True)
dayButton.config(command=partial(tabMange,dayButton,dayFrame))

##Weekly Task
weekButton=tk.Button(tab_bar,text="Weekly",bg="#007acc",fg="white",font=("Arial", 11, "bold"))
weekButton.pack(side="left",expand=True,fill="both")
weekFrame=tk.Frame(window, bg="#38383A")
weekFrame.pack(side="top", fill="both",expand=True)
weekButton.config(command=partial(tabMange,weekButton,weekFrame))
#Montly Tasks
monthButton=tk.Button(tab_bar,text="Monthy",bg="#007acc",fg="white",font=("Arial", 11, "bold"))
monthButton.pack(side="right",expand=True,fill="both")
monthFrame=tk.Frame(window, bg="#38383A")
monthFrame.pack(side="top", fill="both",expand=True)
#######
frames=[dayFrame,weekFrame,monthFrame]
btns=[dayButton,weekButton,monthButton]
#######
for btn in btns:
    btn.config(command=partial(tabMange,btns,frames,btns.index(btn)))
    frames[btns.index(btn)].pack_forget()
dayFrame.pack()
dayButton.config(relief=tk.FLAT)
addtask=tk.Button(bar,text="Add Task",bg="#1C1C1D",fg="#FFFFFF",command=partial(newtask,frames,btns,text),font=("Arial", 10))
addtask.pack(side="right", fill="x", padx=1, pady=3)

##KEY BINDS
window.bind("<Return>",lambda event: newtask( frames, btns, text))

##TriggeringCheckBoxFunc
writeData()
window.mainloop()

###Writing
file=open("todo.txt", "w")

for i in range(0,len(TimeStamps)):
    file.write(pos[i]+"\0"+Tasks[i]+"\0"+TimeStamps[i]+"\0"+btncolors[i]+"\n")
file.close()