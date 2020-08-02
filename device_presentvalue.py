
from bacnet_database import Bacnet_Database
import time 


bacnet = Bacnet_Database()

while True:

	bacnet.get_presentvalue()
	time.sleep(2)


