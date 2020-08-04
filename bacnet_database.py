import mysql.connector
import BAC0
from BAC0.core.io.IOExceptions import UnknownPropertyError, NoResponseFromController
from datetime import datetime
from bacpypes.basetypes import PropertyIdentifier
from bacpypes.primitivedata import Date, Time 
from bacpypes.errors import InvalidTag, InvalidParameterDatatype
import re 
import json 
import sys 
from config import Config



class Bacnet_Database:

	def __init__(self):

		self.bacnet = BAC0.lite()
		# Send 'who-is' command to find devices on network 
		self.devices = self.bacnet.whois()

		#if len(self.devices) == 0:
		#	print("No BACnet Devices Found :(")
		#	sys.exit()


		# Credentials for database stored in the config.py module 
		credentials = Config()

		self.mydb = mysql.connector.connect(
			host = credentials.host,
			user = credentials.user,
			passwd = credentials.passwd,
			database = credentials.database,
			)

		self.cursor = self.mydb.cursor(buffered=True)


	# Add devices to the inventory_2 table
	def get_inventory(self):

		print("Now Getting Inventory")
		for dev in self.devices:
                        
			last_seen = str(datetime.now())
			device_name = self.bacnet.read("{} device {} objectName".format(dev[0], dev[1]))
			ip_address = str(dev[0])
			device_id = dev[1]

			sql_command = "INSERT INTO inventory_2 (devicename, deviceid, ip_addr, lastseen) VALUES (%s,%s,%s,%s)"
			values = (device_name, device_id, ip_address, last_seen)

			self.cursor.execute(sql_command, values)
			self.mydb.commit()

			print(self.cursor.rowcount, "Record inserted")

	

	# Create individual tables for BACnet devices
	def create_tables(self):
		
		print("Creating Tables")

		for dev in self.devices:
			device_name = self.bacnet.read("{} device {} objectName".format(dev[0], dev[1]))
			sql_command = sql_command = 'CREATE TABLE {} (object MEDIUMTEXT, properties JSON)'.format(str(device_name))
			self.cursor.execute(sql_command)
			print("Table Created")


	# Insert objects and properties into individual BACnet devices tables	
	def insert_prop_sql(self, device_name, obj_prop_list):

		prop_sql_command = "INSERT INTO {} (object, properties) VALUES (%s,%s)".format(device_name)
		values = obj_prop_list
		self.cursor.executemany(prop_sql_command, values)
		self.mydb.commit()

		print(self.cursor.rowcount, "Records inserted")


	def insert_singleprop_sql(self, device_name, object_name, json_obj):

		prop_sql_command = "INSERT INTO {} (object, properties) VALUES (%s,%s)".format(device_name)
		values = (object_name, json_obj)
		self.cursor.execute(prop_sql_command, values)
		self.mydb.commit()

		print(self.cursor.rowcount, "Records inserted")




	# Attempt to convert bacpypes 'datetime' objects to date and time - Hit or Miss Works half the time 
	# Should remove but cba having to untangle spahgetti code
	def convert_to_datetime(self, value):
		datetime = None
		try: 
			if re.search(r"[a-z]\)", str(Date(value))):
				datetime = Date(value)			
			else:
				datetime = Time(value)
		
		except (TypeError, ValueError):
			datetime = value

		return datetime

				
			
	def get_properties(self):

		# Exclude certian properties as these will constantly change the hash values 
		exclusion_list = ["localTime", "localDate"]

		print("Getting Properties")
         
		for dev in self.devices:
			
			objects = self.bacnet.read("{} device {} objectList".format(dev[0], dev[1]))
			device_name = self.bacnet.read("{} device {} objectName".format(dev[0], dev[1]))
			print("device_name: {}".format(device_name))

			objname_jsonobj = []

			for obj in objects:
				prop_list = dict()
				object_name = "{}:{}".format(obj[0], obj[1])

				try:
					properties = self.bacnet.readMultiple("{} {} {} all".format(dev[0], obj[0], obj[1]), prop_id_required=True)


					
					# Exclude them first before doing other stuff
					for ex in exclusion_list:

						for prop in properties:

							try:
								if prop[1] == ex:
									properties.remove(prop)
							except IndexError:
								pass	
					
					for prop in properties:

						try:
							if isinstance(prop[0], tuple):
								prop_list[prop[1]] = str(self.convert_to_datetime(prop[0]))

							else:
								if isinstance(prop[0], (int, float)):
									prop_list[prop[1]] = prop[0]

								else:
									prop_list[prop[1]] = str(prop[0])

						except IndexError:
							prop_list = dict()
				
				# Sometimes generates loads of errors - Dont really know why
				except (InvalidTag, InvalidParameterDatatype, TypeError):
					pass 
				
				# Indicates 'multiple read' has failed and therefore will attempt to use 'single read' with specified properties
				if len(prop_list) == 0:
					self.single_read(device_name, dev[0], obj[0], obj[1])
				
				# Otherwise insert them into the table in JSON
				else:
					json_obj = json.dumps(prop_list)

					objname_jsonobj.append(tuple([object_name, json_obj]))
			
			self.insert_prop_sql(device_name, objname_jsonobj)

			self.close_database()
					

		

	# Use as Last Resort! - Will flood network with error messages
	def enumerate_all_properties(self, device_name, device_address, obj, obj_number):
                
		prop_sql_list = dict()
		object_name = "{}:{}".format(obj, obj_number)

		properties = PropertyIdentifier()
		for i in properties.enumerations:
			try:
				prop = self.bacnet.read("{} {} {} {}".format(str(device_address), str(obj), obj_number, i))

				if isinstance(prop, (int, float)):
					prop_sql_list[i] = prop
				else:
					prop_sql_list[i] = str(prop)

			except (UnknownPropertyError, NoResponseFromController, InvalidTag, InvalidParameterDatatype):
				pass
		
		json_obj = json.dumps(prop_sql_list)
		self.insert_prop_sql(device_name, object_name, json_obj)





	# Will attempts single read attempts if multiple read fails 
	# Will use the file 'properties.json' to enumerate and find any properties
	def single_read(self, device_name, device_address, obj, obj_number):

		prop_sql_list = dict()
		object_name = "{}:{}".format(obj, obj_number)

		with open("properties.json") as file:
			json_data = json.load(file)

		for i in json_data["BacnetObjectDescription"]:
			if i["typeId"] == obj:

				try:
					for prop in i["propsId"]:
						add_prop  = self.bacnet.read("{} {} {} {}".format(str(device_address), str(obj), obj_number, prop))

						if isinstance(add_prop, (int,float)):
							prop_sql_list[prop] = add_prop
						else:
							prop_sql_list[prop] = str(add_prop)

				except (InvalidTag, NoResponseFromController, InvalidParameterDatatype):
					pass


		if len(prop_sql_list) == 0:
			# self.enumerate_all_properties(device_name, device_address, obj, obj_number)
			pass
	
		else:
			json_obj = json.dumps(prop_sql_list)
			self.insert_singleprop_sql(device_name, object_name, json_obj)




	# Clear entries for table 'inventory_2'
	def clear_inventory(self):

		print("Clearing Inventory")
	
		sql_command = "TRUNCATE inventory_2"
		self.cursor.execute(sql_command)

		print("inventory table cleared")




	def clear_tables(self):

		print("Clearing Tables")

		current_devices_sql = "SELECT devicename FROM inventory_2"
		self.cursor.execute(current_devices_sql)

		current_devices = self.cursor.fetchall()

		for device in current_devices:
			self.cursor.execute("DROP TABLE IF EXISTS {}".format(device[0]))
			print("Device Deleted")




	# Insert values into the 'Properties' table
	def insert_presentvalue_sql(self, device_obj_list):
		#cursor_5 = self.mydb.cursor(buffered=True)

		prop_sql_command = "INSERT INTO Properties (devicename, objectname, time_stamp, present_value, status_flags, event_state, out_of_service) VALUES (%s,%s,%s,%s,%s,%s,%s)"
		values = device_obj_list
		self.cursor.executemany(prop_sql_command, values)
		self.mydb.commit()

		print(self.cursor.rowcount, "Properties Record Inserted")




	# Retrieve values to store into 'Properties' table
	def get_presentvalue(self):
	
		for dev in self.devices:
			device_name = self.bacnet.read("{} device {} objectName".format(dev[0], dev[1]))
			objects = self.bacnet.read("{} device {} objectList".format(dev[0], dev[1]))

			device_obj_list = []

			for obj in objects:
				object_name = "{}:{}".format(obj[0], obj[1])
				time_stamp = str(datetime.now())
				present_value = None
				status_flags = None
				event_state = None
				out_of_service = None 

				try:
					present_value = self.bacnet.read("{} {} {} presentValue".format(dev[0], obj[0], obj[1]))

					# Try to convert to number rather than string if possible
					if isinstance(present_value, (int, float)):
						present_value = present_value
					else:
						present_value = str(present_value)

					status_flags = self.bacnet.read("{} {} {} statusFlags".format(dev[0], obj[0], obj[1]))
					event_state = self.bacnet.read("{} {} {} eventState".format(dev[0], obj[0], obj[1]))
					out_of_service = self.bacnet.read("{} {} {} outOfService".format(dev[0], obj[0], obj[1]))

					# Convert to True or False strings rather than numbers
					if out_of_service == 0:
						out_of_service = "False"
					if out_of_service == 1:
						out_of_service == "True"

				except (NoResponseFromController, InvalidTag, UnknownPropertyError):
					pass 

				# Ignore device object as it does not contain present value property and throws errors
				if obj[0] == 'device':
					pass

				else:
					device_obj_list.append(tuple([device_name, object_name, time_stamp, present_value, str(status_flags), event_state, out_of_service]))
	
			self.insert_presentvalue_sql(device_obj_list)


	# Store Values into the 'events' table 
	def store_event_sql(self, device_id, time_stamp, event):

		prop_sql_command = "INSERT INTO events (device_id, time_stamp, event) VALUES (%s,%s,%s)"
		values = (device_id, time_stamp, event)
		self.cursor.execute(prop_sql_command, values)
		self.mydb.commit()

		print(self.cursor.rowcount, "Event Record Inserted")




	# Generate Events and store into JSON format
	def create_events(self):

		for dev in self.devices:
			device_name = self.bacnet.read("{} device {} objectName".format(dev[0], dev[1]))
			device_id = dev[1]
			objects = self.bacnet.read("{} device {} objectList".format(dev[0], dev[1]))

			for obj in objects:
				object_name = "{}:{}".format(obj[0], obj[1])
				time_stamp = str(datetime.now())
				present_value = None
				
				try:
					present_value = self.bacnet.read("{} {} {} presentValue".format(dev[0], obj[0], obj[1]))

					if isinstance(present_value, (int, float)):
						present_value = present_value
					else:
						present_value = str(present_value)

					
					create_event = {'time': time_stamp, 'device_name': device_name, 'object_name': object_name, 'present_value': present_value}
					json_event = json.dumps(create_event)

					# Ignore device object as does not contain present value property
					if obj[0] == "device":
						pass
					else:
						self.store_event_sql(device_id, time_stamp, json_event)
					
				except (NoResponseFromController, InvalidTag, UnknownPropertyError):
						pass 


	#Closes Connections
	def close_database(self):
		self.mydb.close()

	# Runs the main functions
	def run_scan(self):
		self.clear_tables()
		self.clear_inventory()
		self.get_inventory()
		self.create_tables()
		self.get_properties()


