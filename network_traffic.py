import json
from secret import Secret
from sql_database import SQL_Database
from alerts_siem import Alerts
import time 



class Network_Traffic:

    def __init__(self, input_file):
	
        self.sql = SQL_Database()
        self.cursor = self.sql.mydb.cursor()

        with open(str(input_file)) as file:
            self.json_file = json.load(file)

        self.traffic_list = []
        self.alerts = Alerts()
        

    def mstp_read(self):

        mstp_name = None
        for i in range(len(self.json_file)):

            for values in self.json_file[i]["_source"]["layers"]:
                mstp_name = values

            try:
                self.json_file[i]["_source"]["layers"]["llc"]

            except KeyError:
                mstp_name = None

        return mstp_name



    def insert_into_database(self):
		
        sql_command = '''INSERT INTO network_traffic (`L2 src address`, `L2 dst address`, `L3 src address`, `L3 dst address`, `L4 src port`, `L4 dst port`, `bacnet dnet`,
							`bacnet hopc`, `frame all`, `eth all`, `ip all`,
							`udp all`, `bvlc all`, `bacnet all`, `bacapp all`,
							`llc all`, `mstp all`)
							VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''


        self.cursor.executemany(sql_command, self.traffic_list)
        self.sql.mydb.commit()
        

    def insert_traffic(self):

        start = time.time()
        print("Getting Traffic Now!")

        l2_source_address = None
        l2_dest_address = None
        l3_source_address = None
        l3_dest_address = None
        l4_dest_port = None
        bacnet_dnet = None
        bacnet_hopc = None
        frame_all = None
        eth_all = None
        ip_all = None
        udp_all = None
        bvlc_all = None
        bacnet_all = None
        bacapp_all = None
        llc_all = None
        mstp_all = None


        for i in self.json_file:
            
            try: 
                    eth_all = json.dumps(i["_source"]["layers"]["eth"])
                    l2_source_address = i["_source"]["layers"]["eth"]["eth.src"]
                    l2_dest_address = i["_source"]["layers"]["eth"]["eth.dst"]

            except KeyError:
                    pass

            try: 
                    ip_all = json.dumps(i["_source"]["layers"]["ip"])
                    l3_source_address = i["_source"]["layers"]["ip"]["ip.src"]
                    l3_dest_address = i["_source"]["layers"]["ip"]["ip.dst"]

            except KeyError:
                    pass

            try:
                    udp_all = json.dumps(i["_source"]["layers"]["udp"])
                    l4_source_port = i["_source"]["layers"]["udp"]["udp.srcport"]
                    l4_dest_port = i["_source"]["layers"]["udp"]["udp.dstport"]

            except KeyError:
                    pass

            try:
                    bacnet_dnet = i["_source"]["layers"]["bacnet"]["bacnet.dnet"]
                    bacnet_hopc = i["_source"]["layers"]["bacnet"]["bacnet.hopc"]

            except KeyError:
                    pass 

            try:
                    frame_all = json.dumps(i["_source"]["layers"]["frame"])

            except KeyError:
                    pass 

            try:		
                    bvlc_all = json.dumps(i["_source"]["layers"]["bvlc"])

            except KeyError:
                    pass 

            try:
                    bacnet_all = json.dumps(i["_source"]["layers"]["bacnet"])

            except KeyError:
                    pass		

            try:
                    bacapp_all = json.dumps(i["_source"]["layers"]["bacapp"])

            except KeyError:
                    pass

            try:    		    
                    llc_all = json.dumps(i["_source"]["layers"]["llc"])
                    mstp_all = json.dumps(i["_source"]["layers"][self.mstp_read()])

            except KeyError:
                    pass


            values = tuple([l2_source_address, l2_dest_address, l3_source_address, l3_dest_address, l4_source_port, l4_dest_port, bacnet_dnet, bacnet_hopc,
            frame_all, eth_all, ip_all, udp_all, bvlc_all, bacnet_all, bacapp_all, llc_all, mstp_all])

            self.traffic_list.append(values)

        self.insert_into_database()

        end = time.time()
        result = end - start
        print("Finished in %.2f secs" %(result))


    def insert_alerts(self):

        for packet in self.json_file:
            self.alerts.alerts_rules(packet)

        self.alerts.insert_into_database()
            

if __name__ == "__main__":		
	network = Network_Traffic("example_traffic/re-init.json")
	network.insert_traffic()
	network.insert_alerts()
    
