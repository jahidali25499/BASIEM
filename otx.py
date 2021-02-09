from OTXv2 import OTXv2 
from pandas import DataFrame
from sql_database import SQL_Database


class OTX:
	
	# OTX API key needed in order to function
	def __init__(self, otx_key):
		self.otx = OTXv2(str(otx_key))

	# Function to search the otx through single IOC (Indicator of Compromise) e.g. IP Addresss, File Hash, Domain  
	def otx_search(self, indicator):

		pulses = self.otx.search_pulses(str(indicator))
		pulse_id = None
		name = None 
		description = None

		for i in range(len(pulses["results"])):
			
			# More fields can be selected - refer to otx_fields.txt 
			pulse_id = pulses["results"][i]["id"]
			name = pulses["results"][i]["name"]
			description = pulses["results"][i]["description"]
			
			if pulse_id != None:
				yield "Pulse ID: " + pulse_id + "\n" + "Name: " + name + "\n" + "Description: " + description + "\n"
		
		
	# Gather all pulses you have subscribed to and convert to json format
	def otx_all(self):

		all_pulses = self.otx.getall()
		
		# Data is inconveniently presented in pandas dataframe format - must be converted to json 
		df = DataFrame(all_pulses)

		json_format = df.to_json(orient="records")
		json_var = json.loads(json_format)

		for i in json_var:
			print(json.dumps(i, indent=4))
			print("\n\n\n")



# This API key is no longer valid!
search = OTX("880c7334ad91a33971f56b1b3ad974738fd3d02a2ead6fd963d046afcbdb67f3")
all_pulses = search.otx_all()


