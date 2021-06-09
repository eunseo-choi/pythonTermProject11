import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback

TOKEN = '1769442996:AAEq79sUkh8bYiqpIi43dFpQt2-hNDgVVMI'
MAX_MSG_LENGTH = 300
baseurl = 'http://openapi.kepco.co.kr/service/EvInfoServiceV2/getEvSearchList?serviceKey=jRweCh29qySuZx84N5yFQERd8KjyNruM9jn9ivkI%2FFq95OLzmPizeIpj9uEZnd5CnJxzsZjZJZ6r2Msl7TVvmg%3D%3D&pageNo=1&numOfRows=500&addr=%EC%84%9C%EC%9A%B8'
bot = telepot.Bot(TOKEN)

def getData():
    res_list = []
    url = baseurl
    #print(url)
    res_body = urlopen(url).read()
    #print(res_body)
    soup = BeautifulSoup(res_body, 'html.parser')

    for items in soup.findAll('item'):
        item = re.sub('<.*?>', '/', str(items))
        parsed = item.split('/')
        try:
            if parsed[10] == '1':
                row = '충전소 명 : '+parsed[16]+' | 주소 : '+parsed[2]+' | 충전기 타입 : '+parsed[8]+'(충전가능)'
            elif parsed[10] == '2':
                row = '충전소 명 : '+parsed[16]+' | 주소 : '+parsed[2]+' | 충전기 타입 : '+parsed[8]+'(충전중)'
            elif parsed[10] == '3':
                row = '충전소 명 : '+parsed[16]+' | 주소 : '+parsed[2]+' | 충전기 타입 : '+parsed[8]+'(고장/점검)'
            elif parsed[10] == '4':
                row = '충전소 명 : '+parsed[16]+' | 주소 : '+parsed[2]+' | 충전기 타입 : '+parsed[8]+'(통신장애)'
            elif parsed[10] == '5':
                row = '충전소 명 : '+parsed[16]+' | 주소 : '+parsed[2]+' | 충전기 타입 : '+parsed[8]+'(통신미연결)'
        except IndexError:
            row = item.replace('|', ',')
        if row:
            res_list.append(row.strip())
    return res_list

def run(date_param):
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS logs( user TEXT, log TEXT, PRIMARY KEY(user, log) )')
    conn.commit()

    user_cursor = sqlite3.connect('users.db').cursor()
    user_cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    user_cursor.execute('SELECT * from users')

    for data in user_cursor.fetchall():
        user, param = data[0], data[1]
        print(user, date_param, param)
        res_list = getData()
        msg = ''
        for r in res_list:
            try:
                cursor.execute('INSERT INTO logs (user,log) VALUES ("%s", "%s")'%(user,r))
            except sqlite3.IntegrityError:
                # 이미 해당 데이터가 있다는 것을 의미합니다.
                pass
            else:
                print( str(datetime.now()).split('.')[0], r )
                if len(r+msg)+1>MAX_MSG_LENGTH:
                    sendMessage( user, msg )
                    msg = r+'\n'
                else:
                    msg += r+'\n'
        if msg:
            sendMessage( user, msg )
    conn.commit()

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

if __name__=='__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')

    print( '[',today,']received token :', TOKEN )

    pprint( bot.getMe() )

    run(current_month)