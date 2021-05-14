from tkinter import *
import tkinter.ttk
class MainGUI:

    def __init__(self):
        window = Tk()
        window.title("파이썬 프로젝트")

        self.notebook = tkinter.ttk.Notebook(window, width=500, height=600)
        self.notebook.pack()

        self.frame1 = Frame(window)
        self.notebook.add(self.frame1, text="전기차 충전소")

        self.Label1 = Entry(self.frame1)
        self.Label1.pack()
        self.Label1.place(x=10, y=30,width=200, height=30)
        self.SearchButton1 = Button(self.frame1, text="검색")
        self.SearchButton1.pack()
        self.SearchButton1.place(x=210, y=30, width=40, height=30)
        self.listNodes1 = Listbox(self.frame1)
        self.listNodes1.pack()
        self.listNodes1.place(x=10,y=70,width=480,height=200)

        self.frame2 = Frame(window)
        self.notebook.add(self.frame2, text="주유소")

        self.Label2 = Entry(self.frame2)
        self.Label2.pack()
        self.Label2.place(x=10, y=30,width=200, height=30)
        self.SearchButton2 = Button(self.frame2, text="검색")
        self.SearchButton2.pack()
        self.SearchButton2.place(x=210, y=30, width=40, height=30)
        self.listNodes2 = Listbox(self.frame2)
        self.listNodes2.pack()
        self.listNodes2.place(x=10,y=70,width=480,height=200)

        self.frame3 = Frame(window)
        self.notebook.add(self.frame3, text="나눔카")

        self.Label3 = Entry(self.frame3)
        self.Label3.pack()
        self.Label3.place(x=10, y=30, width=200, height=30)
        self.SearchButton3 = Button(self.frame3, text="검색")
        self.SearchButton3.pack()
        self.SearchButton3.place(x=210, y=30, width=40, height=30)
        self.listNodes3 = Listbox(self.frame3)
        self.listNodes3.pack()
        self.listNodes3.place(x=10, y=70, width=480, height=200)

        window.mainloop()

MainGUI()