import requests
import json
import pymysql
import time

connection = pymysql.connect(host='localhost', user='root', password='', db='fleep', cursorclass=pymysql.cursors.DictCursor)
cursor =connection.cursor()

while True:
	sql="SELECT * FROM inbox where status=0 LIMIT 10"
	cursor.execute(sql)

	data = cursor.fetchall()
	for row in data: