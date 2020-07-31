from pathlib import Path
import os
import sys
import json
from datetime import datetime

current_path = Path(os.getcwd())
parent_path = current_path.parent
sys.path.append(str(parent_path))

from bacnet_database import Bacnet_Database
from sql_database import SQL_Database

bacnet = Bacnet_Database()
bacnet.run_full_scan()


sql = SQL_Database()
cursor = sql.mydb.cursor()

unauth_devices_list = []

def unauth_device(dev_name, dev_id):

	search_sql = "SELECT device_name, device_id FROM trusted_devices WHERE device_name = '{}' AND device_id = '{}';".format(dev_name, dev_id)
	cursor.execute(search_sql)
	cursor.fetchall()

	if cursor.rowcount == 0:
		rule_alert = "Unauthorised BACnet Device"
		time = str(datetime.now())
		json_alert = json.dumps({"Alert": rule_alert, "Time": time, "Device Name": dev_name, "Device ID": dev_id})

		unauth_devices_list.append(tuple([json_alert,]))


def insert_to_database():

	print("Inserting Unauth Alerts")

	sql_command = "INSERT INTO alerts (alert) VALUES (%s)"
	values = unauth_devices_list
	cursor.executemany(sql_command, values)
	sql.mydb.commit()


current_devices = "SELECT devicename, deviceid FROM inventory_2"
cursor.execute(current_devices)
result = cursor.fetchall()

for dev in result:

	unauth_device(dev[0], dev[1])


insert_to_database()



