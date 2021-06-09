from tkinter import *
from tkinter import font
from tkinter import scrolledtext
from tkinter import ttk
import tkinter as tk
import tkinter.messagebox
from pyproj import Proj,transform


window = Tk()
window.geometry("500x600")
window.title("파이썬 프로젝트")

class MainGUI:
    def __init__(self):
        self.notebook = tkinter.ttk.Notebook(window, width=500, height=610)
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
        self.style.configure("Char.TFrame", background='#b1fc6e')
        self.frame1 = ttk.Frame(window,style="Char.TFrame")
        self.notebook.add(self.frame1, text="전기차 충전소")

        self.Label1 = Entry(self.frame1)
        self.Label1.pack()
        self.Label1.place(x=10, y=30, width=200, height=30)
        self.SearchButton1 = Button(self.frame1, text="검색",command=self.SearchCharging)
        self.SearchButton1.pack()
        self.SearchButton1.place(x=210, y=30, width=40, height=30)

        self.mailimage1 = PhotoImage(file="gmail.png")
        self.MailButton1 = Button(self.frame1, image=self.mailimage1,command=self.sendMain1)
        self.MailButton1.pack()
        self.MailButton1.place(x=300, y=20, width=40, height=40)
        self.mapimage1 = PhotoImage(file="map.png")
        self.MapButton1 = Button(self.frame1, image=self.mapimage1,command=self.mapMain1)
        self.MapButton1.pack()
        self.MapButton1.place(x=350, y=20, width=40, height=40)
        self.favimage1 = PhotoImage(file="star.png")
        self.FavButton1 = Button(self.frame1, image=self.favimage1)
        self.FavButton1.pack()
        self.FavButton1.place(x=400, y=20, width=40, height=40)
        self.Chart = Canvas(self.frame1, width=470, height=250, bg= 'white')
        self.Chart.pack()
        self.Chart.place(x=10, y=300)
        self.DrawChart1()

        self.RenderTextScrollbar = Scrollbar(self.frame1)
        self.RenderTextScrollbar.pack()
        self.RenderTextScrollbar.place(x=460, y=70,width=20, height=200)
        self.RenderText = Text(self.frame1, yscrollcommand = self.RenderTextScrollbar.set)
        self.RenderText.pack()
        self.RenderText.place(x=10, y=70,width=450, height=200)



    def SearchCharging(self):
        import http.client
        from xml.dom.minidom import parse, parseString
        conn = http.client.HTTPConnection("openapi.kepco.co.kr")
        conn.request("GET", "/service/EvInfoServiceV2/getEvSearchList?serviceKey=jRweCh29qySuZx84N5yFQERd8KjyNruM9jn9ivkI%2FFq95OLzmPizeIpj9uEZnd5CnJxzsZjZJZ6r2Msl7TVvmg%3D%3D&pageNo=1&numOfRows=500&addr=%EC%84%9C%EC%9A%B8")
        req = conn.getresponse()

        ChdataList = []
        self.textlist = []
        self.locationxlist = []
        self.locationylist = []
        self.namelist = []
        ChdataList.clear()
        index = 0
        self.RenderText.delete("1.0", "end")

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
                            self.locationxlist.append(subitems[8].firstChild.nodeValue)
                            self.locationylist.append(subitems[9].firstChild.nodeValue)
                            self.namelist.append(subitems[7].firstChild.nodeValue)

                        else:
                            continue
                        if subitems[1].firstChild.nodeValue == '1':
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




                for i in range(len(ChdataList)):
                    self.RenderText.insert(INSERT, "[")
                    self.RenderText.insert(INSERT, i + 1)
                    self.RenderText.insert(INSERT, "]")
                    self.RenderText.insert(INSERT, " 주소 : ")
                    self.RenderText.insert(INSERT, ChdataList[i][0])
                    self.RenderText.insert(INSERT, "\n")
                    self.RenderText.insert(INSERT, " 충전기 타입 : ")
                    self.RenderText.insert(INSERT, ChdataList[i][1])
                    self.RenderText.insert(INSERT, "\n")
                    self.RenderText.insert(INSERT, " 충전기 상태 : ")
                    self.RenderText.insert(INSERT, ChdataList[i][2])
                    self.RenderText.insert(INSERT, "\n")
                    self.RenderText.insert(INSERT, "\n")
                    self.textlist.append(" 주소 : " + ChdataList[i][0] + " 충전기 타입 : " + ChdataList[i][1] + " 충전기 상태 : " + ChdataList[i][2])



    def InitGasStation(self):
        self.style2 = ttk.Style()
        self.style2.configure('Gas.TFrame', background='#6eb4fc')
        self.frame2 = ttk.Frame(window, style='Gas.TFrame')
        self.notebook.add(self.frame2, text="주유소")

        self.Label2 = Entry(self.frame2)
        self.Label2.pack()
        self.Label2.place(x=10, y=30, width=200, height=30)
        self.SearchButton2 = Button(self.frame2, text="검색", command=self.SearchGasStation)
        self.SearchButton2.pack()
        self.SearchButton2.place(x=210, y=30, width=40, height=30)
        self.mailimage2 = PhotoImage(file="gmail.png")
        self.MailButton2 = Button(self.frame2, image=self.mailimage2, command=self.sendMain1)
        self.MailButton2.pack()
        self.MailButton2.place(x=300, y=20, width=40, height=40)
        self.mapimage2 = PhotoImage(file="map.png")
        self.MapButton2 = Button(self.frame2, image=self.mapimage2, command=self.mapMain1)
        self.MapButton2.pack()
        self.MapButton2.place(x=350, y=20, width=40, height=40)
        self.favimage2 = PhotoImage(file="star.png")
        self.FavButton2 = Button(self.frame2, image=self.favimage2)
        self.FavButton2.pack()
        self.FavButton2.place(x=400, y=20, width=40, height=40)
        self.Chart = Canvas(self.frame2, width=470, height=250, bg='white')
        self.Chart.pack()
        self.Chart.place(x=10, y=300)
        self.DrawChart2()

        self.RenderTextScrollbar2 = Scrollbar(self.frame2)
        self.RenderTextScrollbar2.pack()
        self.RenderTextScrollbar2.place(x=460, y=70, width=20, height=200)
        self.RenderText2 = Text(self.frame2, yscrollcommand=self.RenderTextScrollbar2.set)
        self.RenderText2.pack()
        self.RenderText2.place(x=10, y=70, width=450, height=200)


    def SearchGasStation(self):
        #http://openapi.seoul.go.kr:8088/675a77514c6173683733696b55556c/xml/LOCALDATA_092808/1/1000/
        import http.client
        from xml.dom.minidom import parse, parseString
        conn = http.client.HTTPConnection("openapi.seoul.go.kr:8088")
        conn.request("GET", "/675a77514c6173683733696b55556c/xml/LOCALDATA_092808/1/1000/")
        req = conn.getresponse()

        self.textlist = []
        self.locationxlist = []
        self.locationylist = []
        self.namelist = []
        GasdataList = []
        GasdataList.clear()
        self.RenderText2.delete("1.0", "end")

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
                        if subitems[11].firstChild and subitems[31].firstChild is not None:
                            if '영업' in subitems[11].firstChild.nodeValue and self.Label2.get() in subitems[31].firstChild.nodeValue:
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
                                    GasdataList.append((subitems[37].firstChild.nodeValue,subitems[31].firstChild.nodeValue,tel,subitems[11].firstChild.nodeValue))
                                else:
                                    GasdataList.append((subitems[37].firstChild.nodeValue,subitems[31].firstChild.nodeValue,"-",subitems[11].firstChild.nodeValue))

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
                    self.RenderText2.insert(INSERT, "영업 상태 : ")
                    self.RenderText2.insert(INSERT, GasdataList[i][3])
                    self.RenderText2.insert(INSERT, "\n")
                    self.RenderText2.insert(INSERT, "\n")
                    self.textlist.append(
                        " 시설명 : " + GasdataList[i][0] + " 주소 : " + GasdataList[i][1] + " 전화번호 : " + GasdataList[i][2]+ " 영업상태 : " + GasdataList[i][3])

    def InitNanumCar(self):
        self.style3 = ttk.Style()
        self.style3.configure("Nanum.TFrame", background='#c87cf8')
        self.frame3 = ttk.Frame(window, style="Nanum.TFrame")
        self.notebook.add(self.frame3, text="나눔카")

        self.Label3 = Entry(self.frame3)
        self.Label3.pack()
        self.Label3.place(x=10, y=30, width=200, height=30)
        self.SearchButton3 = Button(self.frame3, text="검색", command=self.SearchNanumCar)
        self.SearchButton3.pack()
        self.SearchButton3.place(x=210, y=30, width=40, height=30)
        self.mailimage3 = PhotoImage(file="gmail.png")
        self.MailButton3 = Button(self.frame3, image=self.mailimage3, command=self.sendMain1)
        self.MailButton3.pack()
        self.MailButton3.place(x=300, y=20, width=40, height=40)
        self.mapimage3 = PhotoImage(file="map.png")
        self.MapButton3 = Button(self.frame3, image=self.mapimage3,command=self.mapMain3)
        self.MapButton3.pack()
        self.MapButton3.place(x=350, y=20, width=40, height=40)
        self.favimage3 = PhotoImage(file="star.png")
        self.FavButton3 = Button(self.frame3, image=self.favimage3)
        self.FavButton3.pack()
        self.FavButton3.place(x=400, y=20, width=40, height=40)
        self.Chart = Canvas(self.frame3, width=470, height=250, bg='white')
        self.Chart.pack()
        self.Chart.place(x=10, y=300)
        self.DrawChart3()

        self.RenderTextScrollbar3 = Scrollbar(self.frame3)
        self.RenderTextScrollbar3.pack()
        self.RenderTextScrollbar3.place(x=460, y=70, width=20, height=200)
        self.RenderText3 = Text(self.frame3, yscrollcommand=self.RenderTextScrollbar3.set)
        self.RenderText3.pack()
        self.RenderText3.place(x=10, y=70, width=450, height=200)

    def SearchNanumCar(self):
        #http://openapi.seoul.go.kr:8088/675a77514c6173683733696b55556c/xml/NanumcarSpotList/1/1000/
        import http.client
        from xml.dom.minidom import parse, parseString
        conn = http.client.HTTPConnection("openapi.seoul.go.kr:8088")
        conn.request("GET", "/675a77514c6173683733696b55556c/xml/NanumcarSpotList/1/1000/")
        req = conn.getresponse()

        self.textlist = []
        self.locationxlist = []
        self.locationylist = []
        self.namelist = []
        NanumdataList = []
        NanumdataList.clear()
        self.RenderText3.delete("1.0", "end")

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
                                self.locationxlist.append(subitems[1].firstChild.nodeValue)
                                self.locationylist.append(subitems[3].firstChild.nodeValue)
                                self.namelist.append(subitems[11].firstChild.nodeValue)
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
                    self.RenderText3.insert(INSERT, "\n")
                    self.textlist.append(
                        " 거점명 : " + NanumdataList[i][0] + " 주소 : " + NanumdataList[i][1] + " 전기차 여부 : " + NanumdataList[i][2])

    def sendMain1(self):
        import mimetypes
        import mysmtplib
        from email.mime.base import MIMEBase
        from email.mime.text import MIMEText
        self.host = "smtp.gmail.com"  # Gmail SMTP 서버 주소.
        self.port = "587"
        self.senderAddr = "dmstj080500@gmail.com"  # 보내는 사람 email 주소.
        self.recipientAddr = "dmstj200085@naver.com"

        self.msg = MIMEBase("multipart", "alternative")
        self.msg['Subject'] = "Test email in Python 3.0"
        self.msg['From'] = self.senderAddr
        self.msg['To'] = self.recipientAddr


        self.text = str(self.textlist)
        self.HtmlPart = MIMEText(self.text,'plain')
        self.msg.attach(self.HtmlPart)

        self.s = mysmtplib.MySMTP(self.host, self.port)
        self.s.ehlo()
        self.s.starttls()
        self.s.ehlo()
        self.s.login("dmstj080500@gmail.com", "dmstj12zz")
        self.s.sendmail(self.senderAddr, [self.recipientAddr], self.msg.as_string())
        self.s.close()

    def mapMain1(self):
        import threading
        import sys
        import folium
        from cefpython3 import cefpython as cef
        def showMap(frame):
            sys.excepthook = cef.ExceptHook
            window_info = cef.WindowInfo(frame.winfo_id())
            window_info.SetAsChild(frame.winfo_id(), [0, 0, 800, 600])
            cef.Initialize()
            browser = cef.CreateBrowserSync(window_info, url='file:///map.html')
            cef.MessageLoop()
        window2 = Tk()
        frame = Frame(window2, width=800, height=600)
        frame.pack()

        # 지도 저장
        # 위도 경도 지정
        locationx = self.locationxlist[0]
        locationy = self.locationylist[0]
        m = folium.Map(location=[locationx, locationy], zoom_start=15)
        # 마커 지정
        for i in range(len(self.locationylist)):
            markerx = self.locationxlist[i]
            markery = self.locationylist[i]
            popup = self.namelist[i]
            folium.Marker([markerx, markery], popup=popup).add_to(m)
        # html 파일로 저장
        m.save('map.html')
        thread = threading.Thread(target=showMap, args=(frame,))
        thread.daemon = True
        thread.start()
        window2.mainloop()

    def mapMain3(self):
        import threading
        import sys
        import folium
        from cefpython3 import cefpython as cef
        def showMap(frame):
            sys.excepthook = cef.ExceptHook
            window_info = cef.WindowInfo(frame.winfo_id())
            window_info.SetAsChild(frame.winfo_id(), [0, 0, 800, 600])
            cef.Initialize()
            browser = cef.CreateBrowserSync(window_info, url='file:///map3.html')
            cef.MessageLoop()
        window2 = Tk()
        frame = Frame(window2, width=800, height=600)
        frame.pack()

        # 지도 저장
        # 위도 경도 지정
        locationx = self.locationxlist[0]
        locationy = self.locationylist[0]
        m3 = folium.Map(location=[locationx, locationy], zoom_start=15)
        # 마커 지정
        for i in range(len(self.locationylist)):
            markerx = self.locationxlist[i]
            markery = self.locationylist[i]
            popup = self.namelist[i]
            folium.Marker([markerx, markery], popup=popup).add_to(m3)
        # html 파일로 저장
        m3.save('map3.html')
        thread = threading.Thread(target=showMap, args=(frame,))
        thread.daemon = True
        thread.start()
        window2.mainloop()

    def DrawChart1(self):
        y_stretch = 10
        y_gap = 20
        x_stretch = 11
        x_width = 20
        x_gap = 10
        data = [11, 7, 6, 12, 2, 5, 10, 9, 6, 17,9,6,4,9,14]
        loc = ['송파','강서', '강남', '노원', '관악', '은평', '강동', '양천', '성북', '서초', '구로', '중랑', '동작', '영등포', '마포']

        c_width = 470
        c_height = 250
        for x, y in enumerate(data):
            # calculate reactangle coordinates
            x0 = x * x_stretch + x * x_width + x_gap
            y0 = c_height - (y * y_stretch + y_gap)
            x1 = x * x_stretch + x * x_width + x_width + x_gap
            y1 = c_height - y_gap
            # Here we draw the bar
            self.Chart.create_rectangle(x0, y0, x1, y1, fill="green")
            self.Chart.create_text(x0 + 2, y0, anchor=tk.SW, text=str(y))
        for x, i in enumerate(loc):
            x0 = x * x_stretch + x * x_width + x_gap
            y1 = c_height - y_gap
            self.Chart.create_text(x0+10, y1+20, anchor=tk.S, text=i,)

    def DrawChart2(self):
        y_stretch = 7
        y_gap = 20
        x_stretch = 11
        x_width = 20
        x_gap = 10
        data = [10, 12, 4, 24, 1, 16, 1, 28, 29, 1,5,22,4,5,27]
        loc = ['송파','강서', '강남', '노원', '관악', '은평', '강동', '양천', '성북', '서초', '구로', '중랑', '동작', '영등포', '마포']

        c_width = 470
        c_height = 250
        for x, y in enumerate(data):
            # calculate reactangle coordinates
            x0 = x * x_stretch + x * x_width + x_gap
            y0 = c_height - (y * y_stretch + y_gap)
            x1 = x * x_stretch + x * x_width + x_width + x_gap
            y1 = c_height - y_gap
            # Here we draw the bar
            self.Chart.create_rectangle(x0, y0, x1, y1, fill="blue")
            self.Chart.create_text(x0 + 2, y0, anchor=tk.SW, text=str(y))
        for x, i in enumerate(loc):
            x0 = x * x_stretch + x * x_width + x_gap
            y1 = c_height - y_gap
            self.Chart.create_text(x0+10, y1+20, anchor=tk.S, text=i,)

    def DrawChart3(self):
        y_stretch = 2.5
        y_gap = 20
        x_stretch = 11
        x_width = 20
        x_gap = 10
        data = [54, 58, 72, 39, 51, 44, 49, 38, 27, 56,49,25,39,37,78]
        loc = ['송파','강서', '강남', '노원', '관악', '은평', '강동', '양천', '성북', '서초', '구로', '중랑', '동작', '영등포', '마포']

        c_width = 470
        c_height = 250
        for x, y in enumerate(data):
            # calculate reactangle coordinates
            x0 = x * x_stretch + x * x_width + x_gap
            y0 = c_height - (y * y_stretch + y_gap)
            x1 = x * x_stretch + x * x_width + x_width + x_gap
            y1 = c_height - y_gap
            # Here we draw the bar
            self.Chart.create_rectangle(x0, y0, x1, y1, fill="purple")
            self.Chart.create_text(x0 + 2, y0, anchor=tk.SW, text=str(y))
        for x, i in enumerate(loc):
            x0 = x * x_stretch + x * x_width + x_gap
            y1 = c_height - y_gap
            self.Chart.create_text(x0+10, y1+20, anchor=tk.S, text=i,)

MainGUI()