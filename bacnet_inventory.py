import bacpypes.object 
import sys 
import inspect 
import BAC0
from BAC0.core.io.IOExceptions import NoResponseFromController, UnknownPropertyError
from bacpypes.errors import InvalidTag, InvalidParameterDatatype
import json
from sql_database import SQL_Database



class Bacnet_Inventory():

	def __init__(self):

		self.bacnet = BAC0.lite()
		self.devices = self.bacnet.whois()

		self.sql = SQL_Database()
		self.cursor = self.sql.mydb.cursor()

		self.module_cls = []
		self.all_obj = dict()

		modules = sys.modules["bacpypes.object"]

		for name, obj in inspect.getmembers(modules):
			if inspect.isclass(obj):
				self.module_cls.append(obj)

		for cs in self.module_cls:
			try:
				self.all_obj[cs.objectType] = cs

			except AttributeError:
				pass 


	def get_bacnet_properties(self):

		for dev in self.devices:
			objects = self.bacnet.read("{} device {} objectList".format(dev[0], dev[1]))
			device_name = self.bacnet.read("{} device {} objectName".format(dev[0], dev[1]))

			json_prop_list = []

			for obj in objects:
				prop_list = dict()

				print("{}:{}".format(obj[0], obj[1]))
				properties = self.all_obj[obj[0]].properties

				for prop in properties:
					try:
						response = self.bacnet.read("{} {} {} {}".format(dev[0], obj[0], obj[1], prop.identifier))
						prop_list[prop.identifier] = response

					except (NoResponseFromController, InvalidTag, InvalidParameterDatatype, UnknownPropertyError):
						pass

				json_prop = json.dumps(prop_list)
				json_prop_list.append(json_prop)
			
			self.insert_prop_sql(device_name, json_prop_list)



	def insert_prop_sql(self, device_name, json_prop_list):

		prop_sql_command = "INSERT INTO {} (object, properties) VALUES (%s,%s)".format(device_name)
		values = json_prop_list

		self.cursor.executemany(prop_sql_command, values)
		self.mydb.commit()

		print(self.cursor.rowcount, "Records Inserted")

	

bac = Bacnet_Inventory()
bac.get_bacnet_properties()



