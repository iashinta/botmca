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

def sendMessage():
    cursor.execute("SELECT * FROM outbox where status=0")
    outboxes=cursor.fetchall()

    for outbox in outboxes:
        conversation_id=outbox['conversation_id']
        r = requests.post("https://fleep.io/api/message/send/"+conversation_id,
            headers = {"Content-Type": "application/json"},
            cookies = {"token_id": token},
            data = json.dumps({"message": outbox['message'], "ticket": ticket}))

        sql_update="UPDATE outbox set status=1 where id=%s"%(outbox['id'])
        cursor.execute(sql_update)
        connection.commit()
    connection.rollback()

while True:
    sendMessage()
    print("Send Messages...")
    time.sleep(1)