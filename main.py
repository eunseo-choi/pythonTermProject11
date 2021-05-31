from tkinter import *
from tkinter import font
from tkinter import scrolledtext
from tkinter import ttk
import tkinter.messagebox
from http.client import HTTPSConnection
from http.server import BaseHTTPRequestHandler, HTTPServer

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

    def InitCharging(self):
        self.style = ttk.Style()
        self.style.configure('new.TFrame', background='#7AC5CD')
        self.frame1 = ttk.Frame(window,style='new.TFrame')
        self.notebook.add(self.frame1, text="전기차 충전소")

        self.Label1 = Entry(self.frame1)
        self.Label1.pack()
        self.Label1.place(x=10, y=30, width=200, height=30)
        self.SearchButton1 = Button(self.frame1, text="검색",command=self.SearchCharging)
        self.SearchButton1.pack()
        self.SearchButton1.place(x=210, y=30, width=40, height=30)
        self.mailimage = PhotoImage(file="gmail.png")
        self.MailButton1 = Button(self.frame1, image=self.mailimage,command=self.sendMain())
        self.MailButton1.pack()
        self.MailButton1.place(x=300, y=20, )

        self.RenderTextScrollbar = Scrollbar(self.frame1)
        self.RenderTextScrollbar.pack()
        self.RenderTextScrollbar.place(x=480, y=70,width=200, height=200)
        self.RenderText = Listbox(self.frame1, yscrollcommand = self.RenderTextScrollbar.set)
        self.RenderText.pack()
        self.RenderText.place(x=10, y=70,width=470, height=200)


    def SearchCharging(self):
        import http.client
        from xml.dom.minidom import parse, parseString
        conn = http.client.HTTPConnection("openapi.kepco.co.kr")
        conn.request("GET", "/service/EvInfoServiceV2/getEvSearchList?serviceKey=jRweCh29qySuZx84N5yFQERd8KjyNruM9jn9ivkI%2FFq95OLzmPizeIpj9uEZnd5CnJxzsZjZJZ6r2Msl7TVvmg%3D%3D&pageNo=1&numOfRows=500&addr=%EC%84%9C%EC%9A%B8")
        req = conn.getresponse()

        ChdataList = []
        ChdataList.clear()
        index = 0

        if req.status == 200:
            CharStationDoc = req.read().decode("utf-8")
            if CharStationDoc == None:
                print("ERROR")
            else:
                parseData = parseString(CharStationDoc)
                all = parseData.childNodes
                body = all[0].childNodes
                items = body[1].childNodes
                item = items[0].childNodes

                for i in item:
                    if i.nodeName == "item":
                        subitems = i.childNodes
                        if self.Label1.get() in subitems[0].firstChild.nodeValue:
                            pass
                        else:
                            continue
                        if subitems[1].firstChild.nodeValue == '1':
                            print(subitems[0].firstChild.nodeValue)
                            if subitems[4].firstChild.nodeValue == '1':
                                ChdataList.append((subitems[0].firstChild.nodeValue, "완속", "충전가능"))
                            if subitems[4].firstChild.nodeValue == '2':
                                ChdataList.append((subitems[0].firstChild.nodeValue, "완속", "충전중"))
                            if subitems[4].firstChild.nodeValue == '3':
                                ChdataList.append((subitems[0].firstChild.nodeValue, "완속", "고장/점검"))
                            if subitems[4].firstChild.nodeValue == '4':
                                ChdataList.append((subitems[0].firstChild.nodeValue, "완속", "통신장애"))
                            if subitems[4].firstChild.nodeValue == '5':
                                ChdataList.append((subitems[0].firstChild.nodeValue, "완속", "통신미연결"))
                        if subitems[1].firstChild.nodeValue == '2':
                            if subitems[4].firstChild.nodeValue == '1':
                                ChdataList.append((subitems[0].firstChild.nodeValue, "고속", "충전가능"))
                            if subitems[4].firstChild.nodeValue == '2':
                                ChdataList.append((subitems[0].firstChild.nodeValue, "고속", "충전중"))
                            if subitems[4].firstChild.nodeValue == '3':
                                ChdataList.append((subitems[0].firstChild.nodeValue, "고속", "고장/점검"))
                            if subitems[4].firstChild.nodeValue == '4':
                                ChdataList.append((subitems[0].firstChild.nodeValue, "고속", "통신장애"))
                            if subitems[4].firstChild.nodeValue == '5':
                                ChdataList.append((subitems[0].firstChild.nodeValue, "고속", "통신미연결"))

                    index += 1

                for i in range(len(ChdataList)):
                    printstring = "[" + str((i + 1)) + "] 주소 : " + str(ChdataList[i][0]) + "\n충전기 타입 : " + str(ChdataList[i][1]) + "\n충전기 상태 : " + str(ChdataList[i][2]) + "\n"
                    self.RenderText.insert(i,printstring)


    def InitGasStation(self):
        self.frame2 = Frame(window)
        self.notebook.add(self.frame2, text="주유소")

        self.Label2 = Entry(self.frame2)
        self.Label2.pack()
        self.Label2.place(x=10, y=30, width=200, height=30)
        self.SearchButton2 = Button(self.frame2, text="검색", command=self.SearchGasStation)
        self.SearchButton2.pack()
        self.SearchButton2.place(x=210, y=30, width=40, height=30)

        self.RenderTextScrollbar2 = Scrollbar(self.frame2)
        self.RenderTextScrollbar2.pack()
        self.RenderTextScrollbar2.place(x=480, y=70)
        self.RenderText2 = Text(self.frame2)
        self.RenderText2.pack()
        self.RenderText2.place(x=10, y=70)

    def SearchGasStation(self):
        #http://openapi.seoul.go.kr:8088/675a77514c6173683733696b55556c/xml/LOCALDATA_092808/1/1000/
        import http.client
        from xml.dom.minidom import parse, parseString
        conn = http.client.HTTPConnection("openapi.seoul.go.kr:8088")
        conn.request("GET", "/675a77514c6173683733696b55556c/xml/LOCALDATA_092808/1/1000/")
        req = conn.getresponse()

        GasdataList = []
        GasdataList.clear()

        if req.status == 200:
            GasStationDoc = req.read().decode("utf-8")
            if GasStationDoc == None:
                print("ERROR")
            else:
                parseData = parseString(GasStationDoc)
                all = parseData.childNodes
                row = all[0].childNodes

                for i in row:
                    if i.nodeName == "row":
                        subitems = i.childNodes
                        if subitems[31].firstChild is not None:
                            if self.Label2.get() in subitems[31].firstChild.nodeValue:
                                pass
                            else:
                                continue
                        if subitems[31].firstChild is not None:
                            if subitems[37].firstChild is not None:
                                if subitems[25].firstChild is not None:
                                    tel = str(subitems[25].firstChild.nodeValue)
                                    pass
                                    if len(tel)<9:
                                        tel = "02-"+tel
                                        pass
                                    GasdataList.append((subitems[37].firstChild.nodeValue,subitems[31].firstChild.nodeValue,tel))
                                else:
                                    GasdataList.append((subitems[37].firstChild.nodeValue,subitems[31].firstChild.nodeValue,"-"))

                for i in range(len(GasdataList)):
                    self.RenderText2.insert(INSERT,"[")
                    self.RenderText2.insert(INSERT, i+1)
                    self.RenderText2.insert(INSERT, "]")
                    self.RenderText2.insert(INSERT, " 시설명 : ")
                    self.RenderText2.insert(INSERT, GasdataList[i][0])
                    self.RenderText2.insert(INSERT, "\n")
                    self.RenderText2.insert(INSERT, "주소 : ")
                    self.RenderText2.insert(INSERT,GasdataList[i][1])
                    self.RenderText2.insert(INSERT, "\n")
                    self.RenderText2.insert(INSERT, "전화 번호 : ")
                    self.RenderText2.insert(INSERT, GasdataList[i][2])
                    self.RenderText2.insert(INSERT, "\n")

    def InitNanumCar(self):
        self.frame3 = Frame(window)
        self.notebook.add(self.frame3, text="나눔카")

        self.Label3 = Entry(self.frame3)
        self.Label3.pack()
        self.Label3.place(x=10, y=30, width=200, height=30)
        self.SearchButton3 = Button(self.frame3, text="검색", command=self.SearchNanumCar)
        self.SearchButton3.pack()
        self.SearchButton3.place(x=210, y=30, width=40, height=30)

        self.RenderTextScrollbar3 = Scrollbar(self.frame3)
        self.RenderTextScrollbar3.pack()
        self.RenderTextScrollbar3.place(x=480, y=70)
        self.RenderText3 = Text(self.frame3)
        self.RenderText3.pack()
        self.RenderText3.place(x=10, y=70)

    def SearchNanumCar(self):
        #http://openapi.seoul.go.kr:8088/675a77514c6173683733696b55556c/xml/NanumcarSpotList/1/1000/
        import http.client
        from xml.dom.minidom import parse, parseString
        conn = http.client.HTTPConnection("openapi.seoul.go.kr:8088")
        conn.request("GET", "/675a77514c6173683733696b55556c/xml/NanumcarSpotList/1/1000/")
        req = conn.getresponse()

        NanumdataList = []
        NanumdataList.clear()

        if req.status == 200:
            NanumDoc = req.read().decode("utf-8")
            if NanumDoc == None:
                print("ERROR")
            else:
                parseData = parseString(NanumDoc)
                all = parseData.childNodes
                row = all[0].childNodes

                for i in row:
                    if i.nodeName == "row":
                        subitems = i.childNodes
                        if subitems[9].firstChild is not None:
                            if self.Label3.get() in subitems[9].firstChild.nodeValue:
                                pass
                            else:
                                continue
                        if subitems[9].firstChild is not None:
                            if subitems[11].firstChild is not None:
                                if subitems[7].firstChild is not None:
                                    if subitems[7].firstChild.nodeValue == 'GA':
                                        NanumdataList.append((subitems[11].firstChild.nodeValue,subitems[9].firstChild.nodeValue,"가솔린차"))
                                    if subitems[7].firstChild.nodeValue == 'EV':
                                        NanumdataList.append((subitems[11].firstChild.nodeValue,subitems[9].firstChild.nodeValue,"전기차"))
                                    if subitems[7].firstChild.nodeValue == 'TO':
                                        NanumdataList.append((subitems[11].firstChild.nodeValue,subitems[9].firstChild.nodeValue,"혼합차량"))

                for i in range(len(NanumdataList)):
                    self.RenderText3.insert(INSERT,"[")
                    self.RenderText3.insert(INSERT, i+1)
                    self.RenderText3.insert(INSERT, "]")
                    self.RenderText3.insert(INSERT, " 거점명 : ")
                    self.RenderText3.insert(INSERT, NanumdataList[i][0])
                    self.RenderText3.insert(INSERT, "\n")
                    self.RenderText3.insert(INSERT, "주소 : ")
                    self.RenderText3.insert(INSERT,NanumdataList[i][1])
                    self.RenderText3.insert(INSERT, "\n")
                    self.RenderText3.insert(INSERT, "전기차 여부 : ")
                    self.RenderText3.insert(INSERT, NanumdataList[i][2])
                    self.RenderText3.insert(INSERT, "\n")

    def sendMain(self):
        import mimetypes
        import mysmtplib
        from email.mime.base import MIMEBase
        from email.mime.text import MIMEText
        host = "smtp.gmail.com"  # Gmail SMTP 서버 주소.
        port = "587"
        html = "self.RenderText"
        senderAddr = "dmstj080500@gmail.com"  # 보내는 사람 email 주소.
        recipientAddr = "dmstj200085@naver.com"

        msg = MIMEBase("multipart", "alternative")
        msg['Subject'] = "Test email in Python 3.0"
        msg['From'] = senderAddr
        msg['To'] = recipientAddr

        HtmlPart = MIMEText(html, 'html', _charset='UTF-8')
        msg.attach(HtmlPart)

        s = mysmtplib.MySMTP(host, port)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login("dmstj080500@gmail.com", "dmstj12zz")
        s.sendmail(senderAddr, [recipientAddr], msg.as_string())
        s.close()

        print("Mail sending complete!!!")


MainGUI()