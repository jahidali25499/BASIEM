from Crypto.Hash import SHA256
from sql_database import SQL_Database


class Hash():

    def __init__(self):

        self.sql = SQL_Database()
        self.cursor = self.sql.mydb.cursor()


    def insert_hash_database(self, device_name, hash_hex):

        sql_command = '''INSERT INTO device_configs (device_name, hash) VALUES (%s,%s)'''
        values = (device_name, hash_hex)

        self.cursor.execute(sql_command, values)
        self.sql.mydb.commit()

        print("Hash inserted into database")


    def generate_hash_all(self):

        find_devices = '''SELECT devicename, deviceid FROM inventory_2'''
        self.cursor.execute(find_devices)
        result = self.cursor.fetchall()

        for device in result:

            find_config = '''SELECT properties FROM {} WHERE object = 'device:{}'
                          '''.format(device[0], device[1])

            self.cursor.execute(find_config)
            device_result = self.cursor.fetchall()

            for result in device_result:

                device_config_hash = SHA256.new(str.encode(result[0]))
                device_hash_hex = device_config_hash.hexdigest()
                
                self.insert_hash_database(device[0], device_hash_hex)



    def create_hash_single(self, device_name, device_number):

        find_config = '''SELECT properties FROM {} WHERE object 'device:{}'
                      '''.format(device_name, device_number)

        self.cursor.execute(find_config)
        device_result = self.cursor.fetchall()

        for result in device_result:

            device_config_hash = SHA256.new(str.encode(result[0]))
            device_hash_hex = device_config_hash.hexdigest()

            self.insert_hash_database(device[0], device_hash_hex)



    def verify_hash_all(self):

        find_all_devices = '''SELECT devicename, deviceid FROM inventory_2'''
        self.cursor.execute(find_all_devices)
        result = self.cursor.fetchall()

        for device in result:

            find_config = '''SELECT properties FROM {} WHERE object = 'device:{}' '''.format(device[0], device[1])
            self.cursor.execute(find_config)
            device_result = self.cursor.fetchall()

            for result in device_result:

                device_config_hash = SHA256.new(str.encode(result[0])).hexdigest()

                current_hash_sql = '''SELECT hash FROM device_configs WHERE device_name = '{}' '''.format(device[0])
                self.cursor.execute(current_hash_sql)
                current_hash = self.cursor.fetchall()

                if device_config_hash == current_hash[0][0]:
                    print("Device: {}\nDevice Number: {}\nFile Integrity: {}".format(device[0], device[1], "Passed"))

                else:
                    print("Device: {}\nDevice Number: {}\nFile Integrity: {}".format(device[0], device[1], "Failed"))

    
                
    def verify_hash_single(self, device_name, device_number):

        find_config = '''SELECT properties FROM {} WHERE object = 'device:{}' '''.format(device_name, device_number)
        self.cursor.execute(find_config)
        config_result = self.cursor.fetchall()

        config_hash = SHA256.new(str.encode(config_result[0][0])).hexdigest()

        hash_sql = "SELECT hash FROM device_configs WHERE device_name = '{}'".format(device_name)
        self.cursor.execute(hash_sql)
        current_hash = self.cursor.fetchall()

        if config_hash == current_hash[0][0]:
            print("Device: {}\nDevice Number: {}\nFile Integrity: {}".format(device_name, device_number, "Passed"))
            return True

        else:
            print("Device: {}\nDevice Number: {}\nFile Integrity: {}".format(device_name, device_number, "Failed"))
            return False
                  

    

if __name__ == "__main__":
    hash_database = Hash()
    #hash_database.generate_hash_all()
    hash_database.verify_hash_all()
    #hash_database.verify_hash_single(device_name="myBacnetDevice01", device_number=1234)
    
