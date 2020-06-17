from OTXv2 import OTXv2 
from pandas import DataFrame
from sql_database import SQL_Database


class OTX:

	def __init__(self, otx_key):
		self.otx = OTXv2(str(otx_key))


	def otx_search(self, indicator):

		pulses = self.otx.search_pulses(str(indicator))
		pulse_id = None
		name = None 
		description = None

		for i in range(len(pulses["results"])):

			pulse_id = pulses["results"][i]["id"]
			name = pulses["results"][i]["name"]
			description = pulses["results"][i]["description"]

			if pulse_id != None:

				yield "Pulse ID: " + pulse_id + "\n" + "Name: " + name + "\n" + "Description: " + description + "\n"
				

	def otx_all(self):

		all_pulses = self.otx.getall()

		df = DataFrame(all_pulses)

		json_format = df.to_json(orient="records")
		json_var = json.loads(json_format)

		for i in json_var:
			print(json.dumps(i, indent=4))
			print("\n\n\n")




search = OTX("880c7334ad91a33971f56b1b3ad974738fd3d02a2ead6fd963d046afcbdb67f3")
all_pulses = search.otx_all()

