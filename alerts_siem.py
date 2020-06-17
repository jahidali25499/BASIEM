import json
from sql_database import SQL_Database
import time
from apscheduler.schedulers.background import BackgroundScheduler


class Alerts:

    def __init__(self):

        self.sql = SQL_Database()
        self.cursor = self.sql.mydb.cursor()

        self.alerts_list = []


    def alerts_rules(self, packet):
        self.re_init_device(packet)
        self.password_fail_reinit(packet)
        self.foreign_device(packet)


        

    def insert_into_database(self):

        print("Inserting Alerts")
        start = time.time()

        sql_command = '''INSERT INTO alerts (id_network_traffic, alert) VALUES (%s,%s) '''
        values = self.alerts_list
        self.cursor.executemany(sql_command, values)
        self.sql.mydb.commit()
        
        end = time.time()
        result = end - start

        print("Finished Inserting Alerts at %.2f secs" %(result))


    def find_network_id(self, epoch):

        sql_command = '''SELECT id FROM network_traffic WHERE JSON_CONTAINS(`frame all`, '{}')'''.format(epoch)
        self.cursor.execute(sql_command)

        result = self.cursor.fetchall()
        return result



    def re_init_device(self, packet):

        try:
            re_init_service = packet["_source"]["layers"]["bacapp"]["bacapp.confirmed_service"]
            apdu_type = packet["_source"]["layers"]["bacapp"]["bacapp.type"]

            if (re_init_service != None) and (int(re_init_service) == 20):

                if int(apdu_type) == 0:
                    source_ip = packet["_source"]["layers"]["ip"]["ip.src"]
                    dest_ip = packet["_source"]["layers"]["ip"]["ip.dst"]
                    time = packet["_source"]["layers"]["frame"]["frame.time"]          
                    alert = "Re-Initialisation Command Detected"
                    
                    # Epoch will be used to link alerts to its full network traffic
                    epoch_time = packet["_source"]["layers"]["frame"]["frame.time_epoch"]
                    json_epoch = json.dumps({"frame.time_epoch": epoch_time})
                    network_id = self.find_network_id(json_epoch)[0][0]
                
                    json_event = json.dumps({"alert": alert, "time": time, "source_ip": str(source_ip), "dest_ip": str(dest_ip)})

                    self.alerts_list.append(tuple([network_id, json_event]))
                    
        except KeyError:  
            pass



    def password_fail_reinit(self, packet):

        try:
            error_code = packet["_source"]["layers"]["bacapp"]["bacapp.error_code"]

            if int(error_code) == 26:
                    source_ip = packet["_source"]["layers"]["ip"]["ip.src"]
                    dest_ip = packet["_source"]["layers"]["ip"]["ip.dst"]
                    time = packet["_source"]["layers"]["frame"]["frame.time"]    
                    alert = "Re-Initialisation Password Failure"

                    epoch_time = packet["_source"]["layers"]["frame"]["frame.time_epoch"]
                    json_epoch = json.dumps({"frame.time_epoch": epoch_time})
                    network_id = self.find_network_id(json_epoch)[0][0]

                    json_event = json.dumps({"alert": alert, "time": time, "source_ip": str(source_ip), "dest_ip": str(dest_ip)})

                    self.alerts_list.append(tuple([network_id, json_event]))

        except KeyError:
            pass



    def foreign_device(self, packet):

        try:
            bvlc_function = packet["_source"]["layers"]["bvlc"]["bvlc.function"]

            if int(bvlc_function, 16) == 5:

                    source_ip = packet["_source"]["layers"]["ip"]["ip.src"]
                    dest_ip = packet["_source"]["layers"]["ip"]["ip.dst"]
                    time = packet["_source"]["layers"]["frame"]["frame.time"]
                    alert = "Foreign Device Registration Detected"
                    
                    epoch_time = packet["_source"]["layers"]["frame"]["frame.time_epoch"]
                    json_epoch = json.dumps({"frame.time_epoch": epoch_time})
                    network_id = self.find_network_id(json_epoch)[0][0]
                    
                    json_event = json.dumps({"alert": alert, "time": time, "source_ip": str(source_ip), "dest_ip": str(dest_ip)})

                    self.alerts_list.append(tuple([network_id, json_event]))


        except KeyError:
            pass



    def test_sql(self):
        print("Deleting")
        sql_command = '''TRUNCATE network_traffic;'''
        self.cursor.execute(sql_command)



        

                




   
