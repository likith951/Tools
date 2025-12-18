import tkinter as tk
from functools import partial
from tkinter import font
from datetime import datetime

window = tk.Tk()
Tasks=[]
TimeStamps=[]
pos=[]
btncolors=[]
c_vars=[]
PRIORITY = {
    "red": 0,
    "yellow": 1,
    "blue": 2
}


def repack(Scolor, TaskFrame, checkbox):
    if hasattr(Scolor, "get"):
        Scolor = Scolor.get()
    else:
        Scolor = Scolor
    parent = TaskFrame.master


    tasks_in_frame = parent.winfo_children()

    idx = Tasks.index(checkbox.cget("text"))
    btncolors[idx] = Scolor

    def priority(task_frame):
        btn = task_frame.winfo_children()[-1]
        return PRIORITY.get(btn.cget("bg"))

    tasks_in_frame.sort(key=priority)

    # repack in sorted order
    for task in tasks_in_frame:
        task.pack_forget()
        task.pack(side=tk.TOP, fill=tk.BOTH, anchor=tk.N)

def apply(checkbox,textarea,Taskbtn,Scolor,editwin,taskframe,event=None):
    otext=checkbox.cget("text")
    checkbox.config(text=textarea.get("1.0",tk.END).strip())
    Tasks[Tasks.index(otext)] = textarea.get("1.0",tk.END).strip()
    btncolors[Tasks.index(checkbox.cget("text"))] = Scolor.get()
    Taskbtn.config(bg=Scolor.get())
    repack(Scolor,taskframe,checkbox)
    editwin.destroy()
def writeData():
    file=open("todo.txt", "r")
    lines=file.readlines()
    for line in lines:
        temp=line.split("\0")
        p=int(temp[0])
        text=temp[1]
        time=temp[2]
        color = temp[3].strip()
        checked_state = int(temp[4].strip())
        newtask(frames,btns,text,time,p,color,checked_state)
    file.close()

def getout(editwin,frame,checkbox,timestamp,TaskFrame):
    Tasks.remove(checkbox.cget("text"))
    TimeStamps.remove(timestamp.cget("text"))
    pos.remove(str(frames.index(frame)))
    TaskFrame.destroy()
    editwin.destroy()


def checked(cb):
    f = font.Font(font=cb.cget("font"))
    #idx = Tasks.index(cb.cget("text"))
    if f.actual("overstrike") == 0:
        f.configure(overstrike=1)
        #c_vars[idx]=1
    else:
        f.configure(overstrike=0)
        #c_vars[idx]=0
    cb.configure(font=f)


def edit(Taskbtn,frame,checkBox,timeStamp,TaskFrame,btn):
    editwin=tk.Toplevel(window)
    editwin.title("Edit")
    editwin.geometry("300x200")
    editwin.resizable(0,0)
    bottomframe = tk.Frame(editwin, height=40)
    bottomframe.pack(side="bottom", fill="x", expand=1)
    applybtn = tk.Button(bottomframe, text="Apply")
    applybtn.pack(side=tk.LEFT,expand=1,padx=5,pady=5,fill="both")
    colors=["red","yellow","blue"]
    color=tk.StringVar()
    color.set(btncolors[Tasks.index(checkBox.cget("text"))])
    colorpicker=tk.OptionMenu(bottomframe,color, *colors)
    colorpicker.pack(side=tk.LEFT,expand=1,padx=5,pady=5)
    discardbtn = tk.Button(bottomframe, text="Discard")
    discardbtn.pack(side=tk.LEFT,expand=1,padx=5,pady=5,fill="both")
    deletebtn = tk.Button(bottomframe, text="Delete")
    deletebtn.pack(side=tk.LEFT,expand=1,padx=5,pady=5,fill="both")
    mainFrame=tk.Frame(editwin)
    mainFrame.pack(side="top",expand=1)
    textarea=tk.Text(mainFrame)
    textarea.pack(fill=tk.BOTH)
    taskText=checkBox.cget("text")
    textarea.insert(tk.INSERT,taskText)
    focusFrame=tk.Frame(editwin)
    focusFrame.pack(side="top",expand=1)
    #config func
    applybtn.configure(command=partial(apply, checkBox,textarea,Taskbtn,color,editwin,TaskFrame,btn))
    discardbtn.config(command=editwin.destroy)
    deletebtn.config(command=partial(getout, editwin,frame,checkBox,timeStamp,TaskFrame))
    #focusFrame=tk.Frame(editwin)
    editwin.grab_set()  # Makes the modal window "modal"
    window.wait_window(editwin)


def get_time():
    i=btns.index(get_button(btns))
    if i==0:
        return str(datetime.now().strftime("%I:%M%p"))
    else:
        return str(datetime.now().strftime("%b %d"))

def get_button(btns):
    for btn in btns:
        if btn['relief'] == tk.FLAT:
            return btn
def newtask(frames,btns,text,Time=None,i=None,color="blue",checked_state=0):
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
    if Text=="":
        return
    ###AddingCheckBoxes:
    c_var = tk.IntVar(value=checked_state)
    TaskFrame=tk.Frame(frame,bg="#888888")
    checkBox = tk.Checkbutton(TaskFrame, text=Text,variable=c_var,onvalue=1,offvalue=0,justify=tk.LEFT,bg="#888888",font=("Segoe UI", 10))
    timeStamp = tk.Label(TaskFrame, text=time,justify=tk.LEFT,bg="#888888",font=("Consolas", 9))
    editbtn=tk.Button(TaskFrame,justify=tk.RIGHT,bg=color)
    checkBox.pack(side=tk.LEFT, fill=tk.BOTH,anchor=tk.N)
    timeStamp.pack(side=tk.LEFT, fill=tk.BOTH,anchor=tk.N)
    editbtn.pack(side=tk.RIGHT, fill=tk.BOTH,anchor=tk.N)
    TaskFrame.pack(side=tk.TOP, fill=tk.BOTH,anchor=tk.N)
    editbtn.config(command=partial(edit,editbtn,frame,checkBox,timeStamp,TaskFrame,editbtn))
    checkBox.config(command=partial(checked, checkBox))
    ##storing data for writing
    Tasks.append(checkBox.cget("text"))
    TimeStamps.append(timeStamp.cget("text"))
    btncolors.append(editbtn.cget("bg"))
    pos.append(str(frames.index(frame)))
    c_vars.append(c_var)
    if checked_state==1:
        checked(checkBox)
    repack(color,TaskFrame,checkBox)
def tabMange(btns,frames,i):
    for j in range(len(btns)):
        btns[j].config(relief=tk.RAISED,bg="#007acc")
        frames[j].pack_forget()
        if j==i:
            btns[j].config(relief=tk.FLAT,bg="#00c853")
            frames[j].pack()

#########Window
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
c_vals=c_vars
for i in range(0,len(TimeStamps)):
    file.write(pos[i]+"\0"+Tasks[i]+"\0"+TimeStamps[i]+"\0"+btncolors[i]+"\0"+str(c_vals[i].get())+"\n")
file.close()