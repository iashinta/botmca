import requests
import json
import pymysql
import time

connection = pymysql.connect(host='localhost', user='root', password='', db='fleep', cursorclass=pymysql.cursors.DictCursor)
cursor =connection.cursor()

r = requests.post("https://fleep.io/api/account/login",
                  headers = {"Content-Type": "application/json"},
                  data = json.dumps({"email": "kruinsmine@gmail.com", "password": "123123ds"}))

ticket=r.json()["ticket"]
token=r.cookies["token_id"]

def getConversation():
    r = requests.post("https://fleep.io/api/conversation/list",
        headers = {"Content-Type": "application/json"},
        cookies = {"token_id": token},
        data = json.dumps({"ticket": ticket}))
    conversations=r.json()['conversations']

    for conversation in conversations:
        getMessages(conversation['conversation_id'])


def getMessages(conversation_id):
    url="https://fleep.io/api/conversation/sync/"+conversation_id
    r = requests.post(url,
        headers = {"Content-Type": "application/json"},
        cookies = {"token_id": token},
        data = json.dumps({"ticket": ticket}))
    messages=r.json()['stream']

    for message in messages:
        try:
            msg=message['message'][8:-10]
            sql_select="SELECT * FROM inbox where message_id='%s'"%message['message_id']
            cursor.execute(sql_select)
            
            item=cursor.fetchone()
            if item is None and message['account_id'] != "ea7ed7f4-532f-45aa-806e-6527b6b67f32":
                sql_insert="INSERT INTO inbox VALUES(null,'%s','%s','%s','%s',0)"%(conversation_id,msg,message['message_id'],message['account_id'])
                print(sql_insert)
                cursor.execute(sql_insert)
                connection.commit()
            connection.rollback()
        except:
            print("...")

while True:
    getConversation()
    connection.rollback()
    time.sleep(1)