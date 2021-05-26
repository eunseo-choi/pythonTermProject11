from tkinter import *
from tkinter import font
from tkinter import scrolledtext
import tkinter.ttk
import tkinter.messagebox

window = Tk()
window.geometry("500x600")
window.title("파이썬 프로젝트")

class MainGUI:
    def __init__(self):
        self.notebook = tkinter.ttk.Notebook(window, width=500, height=600)
        self.notebook.pack()
        self.InitCharging()
        self.InitGasStation()
        self.InitNanumCar()

        window.mainloop()

    def InitTopText(self):
        TempFont = font.Font(window, size=20, weight='bold', family='Consolas')
        MainText = Label(window, font=TempFont, text="[서울시 전기차/주유소 검색]")
        MainText.pack()
        MainText.place(x=20)

    def InitRenderText(self):
        self.RenderText = scrolledtext.ScrolledText(self.frame1)
        self.RenderText.config(width=480,height=200)
        self.RenderText.configure(state='disabled')

    def InitCharging(self):
        self.frame1 = Frame(window)
        self.notebook.add(self.frame1, text="전기차 충전소")

        self.Label1 = Entry(self.frame1)
        self.Label1.pack()
        self.Label1.place(x=10, y=30, width=200, height=30)
        self.SearchButton1 = Button(self.frame1, text="검색",command=self.SearchCharging)
        self.SearchButton1.pack()
        self.SearchButton1.place(x=210, y=30, width=40, height=30)
        self.listNodes1 = Listbox(self.frame1)
        self.listNodes1.pack()
        self.listNodes1.place(x=10, y=70, width=480, height=200)


    def SearchCharging(self):
        import http.client
        from xml.dom.minidom import parse, parseString
        conn = http.client.HTTPConnection("openapi.kepco.co.kr")
        conn.request("GET", "/service/EvInfoServiceV2/getEvSearchList?serviceKey=jRweCh29qySuZx84N5yFQERd8KjyNruM9jn9ivkI%2FFq95OLzmPizeIpj9uEZnd5CnJxzsZjZJZ6r2Msl7TVvmg%3D%3D&pageNo=1&numOfRows=500&addr=%EC%84%9C%EC%9A%B8")
        req = conn.getresponse()

        ChdataList = []
        ChdataList.clear()

        if req.status == 200:
            CharStationDoc = req.read().decode("utf-8")
            if CharStationDoc == None:
                print("ERROR")
            else:
                parseData = parseString(CharStationDoc)
                GeoInfoCharStation = parseData.childNodes
                row = GeoInfoCharStation[0].childNodes

                for item in row:
                    if item.nodeName == "row":
                        subitems = item.childNodes
                        if subitems[0].firstChild.nodeValue in self.Label1.get():
                            ChdataList.append(subitems[0].firstChild.nodeValue)
                            if subitems[3].firstChild.nodeValue == 1:
                                ChdataList.append("완속")
                                print("완속")
                            elif subitems[3].firstChild.nodeValue == 2:
                                ChdataList.append("급속")
                            elif subitems[9].firstChild.nodeValue == 1:
                                ChdataList.append("충전가능")
                            elif subitems[9].firstChild.nodeValue == 2:
                                ChdataList.append("충전중")
                            elif subitems[9].firstChild.nodeValue == 3:
                                ChdataList.append("고장/점검")
                            elif subitems[9].firstChild.nodeValue == 4:
                                ChdataList.append("통신장애")
                            elif subitems[9].firstChild.nodeValue == 5:
                                ChdataList.append("통신미연결")
                        else:
                            continue

                for i in range(len(ChdataList)):
                    self.RenderText.insert(INSERT,"[")
                    self.RenderText.insert(INSERT, "i+1")
                    self.RenderText.insert(INSERT, "]")
                    self.RenderText.insert(INSERT, "주소 : ")
                    self.RenderText.insert(INSERT, ChdataList[i][0])
                    self.RenderText.insert(INSERT, "충전기 타입 : ")
                    self.RenderText.insert(INSERT,ChdataList[i][1])
                    self.RenderText.insert(INSERT, "충전기 상태 : ")
                    self.RenderText.insert(INSERT, ChdataList[i][2])







    def InitGasStation(self):
        self.frame2 = Frame(window)
        self.notebook.add(self.frame2, text="주유소")

        self.Label2 = Entry(self.frame2)
        self.Label2.pack()
        self.Label2.place(x=10, y=30, width=200, height=30)
        self.SearchButton2 = Button(self.frame2, text="검색")
        self.SearchButton2.pack()
        self.SearchButton2.place(x=210, y=30, width=40, height=30)
        self.listNodes2 = Listbox(self.frame2)
        self.listNodes2.pack()
        self.listNodes2.place(x=10, y=70, width=480, height=200)

    def InitNanumCar(self):
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





MainGUI()