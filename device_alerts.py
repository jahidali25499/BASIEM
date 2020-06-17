import json
from sql_database import SQL_Database
import operator


# SELECT id FROM Properties WHERE devicename = '<device_name>' AND object_name = '<object_name:object_number>' AND <property> <expression> <value>

# This script can be used to generate alerts based on personalized rules created in the device_rules.json file 
# Rules currently detect whether certain values are higher, lower or equal to a certain value or string 
# TO-DO - edit to include '>=" and "<=" symbols for values


class Device_Alerts:

	def __init__(self, input_file):

		self.sql = SQL_Database()
		self.cursor = self.sql.mydb.cursor()

		with open(str(input_file)) as file:
			self.json_file = json.load(file)

			
	# Used in later function to convert numbers as strings to just numbers
	def is_number(self, number):

		try:
			float(number)
			return True

		except ValueError:
			return False
		

	def device_alerts_bacnet(self):
		
		# Convert symbols which do the same job
		ineq_dict = {
				"<": operator.lt, 
				">": operator.gt, 
				"=": operator.eq
				}
		
		# Extract fields from 'device_rules.json' file 
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
			
			# Gather all values from chosen property within the search value and unit specified
			chosen_property = '''SELECT * FROM Properties WHERE devicename = '{}' AND objectname = '{}:{}' 
			AND time_stamp >= DATE_SUB(NOW(), INTERVAL {} {})'''.format(device_name, object_name, object_number, search_value, search_unit)

			send_cmd = self.cursor.execute(chosen_property)
			results = self.cursor.fetchall()
			
			# Compare to the values specified in the 'device_rules.json' file and trigger alert
			for entry in results:
				
				# Change all numbers to floats or leave as strings
				if self.is_number(entry[4]):
					if ineq_dict[expression](float(entry[4]), value):
						print(alert, entry[0])

				else:
					if ineq_dict[expression](entry[4], value):
						print(alert, entry[0])
						


device = Device_Alerts("device_rules.json")
device.device_alerts_bacnet()
