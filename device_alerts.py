import json
from sql_database import SQL_Database
import operator


# SELECT id FROM Properties WHERE devicename = '<device_name>' AND object_name = '<object_name:object_number>' AND <property> <expression> <value>

class Device_Alerts:

	def __init__(self, input_file):

		self.sql = SQL_Database()
		self.cursor = self.sql.mydb.cursor()

		with open(str(input_file)) as file:
			self.json_file = json.load(file)


	def is_number(self, number):

		try:
			float(number)
			return True

		except ValueError:
			return False
		

	def device_alerts_bacnet(self):

		ineq_dict = {
				"<": operator.lt, 
				">": operator.gt, 
				"=": operator.eq
				}

		for i in self.json_file:

			device_name = i["device_name"]
			object_name = i["object_name"]
			object_number = i["object_number"]
			object_property = i["property"]
			expression = i["expression"]
			value = i["value"]
			search_value = i["search_value"]
			search_unit = i["search_unit"]
			alert = i["alert"]

			chosen_property = '''SELECT * FROM Properties WHERE devicename = '{}' AND objectname = '{}:{}' 
			AND time_stamp >= DATE_SUB(NOW(), INTERVAL {} {})'''.format(device_name, object_name, object_number, search_value, search_unit)

			send_cmd = self.cursor.execute(chosen_property)
			results = self.cursor.fetchall()

			for entry in results:

				if self.is_number(entry[4]):
					if ineq_dict[expression](float(entry[4]), value):
						print(alert, entry[0])

				else:
					if ineq_dict[expression](entry[4], value):
						print(alert, entry[0])
						


device = Device_Alerts("device_rules.json")
device.device_alerts_bacnet()
