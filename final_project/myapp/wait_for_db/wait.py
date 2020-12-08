import pymysql
from time import sleep
from sys import stderr

ok = False
for i in range(10):
	try:
		conn = pymysql.connect(host='myapp_db', port=8081, user='test_qa', password='qa_test', db='myapp_db')
		conn.ping(reconnect=False)
		conn.close()
		ok = True
		break
	except:
		sleep(2)

if not ok:
	print('DB wait timeout', file=sys.stderr)
	exit(1)