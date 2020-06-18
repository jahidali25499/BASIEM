import json
from sql_database import SQL_Database
import time
from apscheduler.schedulers.background import BackgroundScheduler


class Alerts:

    def __init__(self):

        self.sql = SQL_Database()
        self.cursor = self.sql.mydb.cursor()
        
        # store all alerts here before sending them off to database at once
        self.alerts_list = []

    # Store all rules inside this single function 
    def alerts_rules(self, packet):
        self.re_init_device(packet)
        self.password_fail_reinit(packet)
        self.foreign_device(packet)

        
    # Insert all alerts from alerts list into database
    def insert_into_database(self):

        print("Inserting Alerts")
        start = time.time()

        sql_command = '''INSERT INTO alerts (id_network_traffic, alert) VALUES (%s,%s) '''
        values = self.alerts_list
        
        # Using 'executemany' addresses the speed issues and inserts data far more quickly
        self.cursor.executemany(sql_command, values)
        self.sql.mydb.commit()
        
        end = time.time()
        result = end - start

        print("Finished Inserting Alerts at %.2f secs" %(result))

        
    # Link alerts generated here to the full traffic in 'network_traffic' by matching the epoch time 
    def find_network_id(self, epoch):

        sql_command = '''SELECT id FROM network_traffic WHERE JSON_CONTAINS(`frame all`, '{}')'''.format(epoch)
        self.cursor.execute(sql_command)

        result = self.cursor.fetchall()
        return result


    # Rule to detect the 're-init' command in a packet
    def re_init_device(self, packet):

        try:
            # Detected in the application layer
            re_init_service = packet["_source"]["layers"]["bacapp"]["bacapp.confirmed_service"]
            apdu_type = packet["_source"]["layers"]["bacapp"]["bacapp.type"]
            
            # Detect re-init packet sent from source device not ack from target device to avoid duplicate entries
            if (re_init_service != None) and (int(re_init_service) == 20):
               
                # If detected gather extra information such as IP Address, time etc.
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
                    
                    # Add to alerts list
                    self.alerts_list.append(tuple([network_id, json_event]))
                    
        except KeyError:  
            pass


    # Rule to detect failed password entered for 're-init' command
    def password_fail_reinit(self, packet):
        
        try:
            error_code = packet["_source"]["layers"]["bacapp"]["bacapp.error_code"]
            
            # Password failure would have error code 26
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
            
            # Detected in 'bvlc' layer which has the function code 5 in hexadecimal (hence 16 in int)
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

    # Convenient way of deleting table if HeidiSQL is being a bother
    def delete_sql(self):
        print("Deleting")
        sql_command = '''TRUNCATE network_traffic;'''
        self.cursor.execute(sql_command)

