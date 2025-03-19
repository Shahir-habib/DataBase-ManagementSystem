"""1. Develop an application as follows. 
User will enter two numbers. Provide button to add or to find the difference. Depending 
on the option result will be shown in result box. Add a suitable title to the screen. 
Whenever the form is loaded, also display current date in the title bar."""

from tkinter import *
import time
import os
def add():
    a=int(e1.get())
    b=int(e2.get())
    c=a+b
    e3.insert(0,c)
    f=open("calculator.txt","a")
    f.write("Addition of %d and %d is %d\n"%(a,b,c))
    f.close()
def sub():
    a=int(e1.get())
    b=int(e2.get())
    c=a-b
    e3.insert(0,c)
    f=open("calculator.txt","a")
    f.write("Subtraction of %d and %d is %d\n"%(a,b,c))
    f.close()
def clear():
    e1.delete(0,END)
    e2.delete(0,END)
    e3.delete(0,END)
def exit():
    root.destroy()
root=Tk()
root.title(f"Calculator {time.strftime('%d/%m/%Y')}")
root.geometry("300x300")
l1=Label(root,text="Enter first number")
l1.pack()
e1=Entry(root)
e1.pack()
l2=Label(root,text="Enter second number")
l2.pack()
e2=Entry(root)
e2.pack()
b1=Button(root,text="Add",command=add)
b1.pack()
b2=Button(root,text="Subtract",command=sub)
b2.pack()
l3=Label(root,text="Result")
l3.pack()
e3=Entry(root)
e3.pack()
b3=Button(root,text="Clear",command=clear)
b3.pack()
b4=Button(root,text="Exit",command=exit)
b4.pack()
root.mainloop()
#output: calculator window will open and you can perform addition and subtraction of two numbers and the result will be displayed in the window and stored in a file calculator.txt
#input: enter two numbers and click on add or subtract button   and click on clear to clear the window and click on exit to close the window