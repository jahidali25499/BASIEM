from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from pathlib import Path
import os
import sys


class RSA_Signature():

    def __init__(self):

        # Add parent directory to import module
        path = Path(os.getcwd())
        parent_path = path.parent
        sys.path.append(parent_path.__str__())       

        # Now import module
        from sql_database import SQL_Database

        self.sql = SQL_Database()
        self.cursor = self.sql.mydb.cursor()


    # Insert signatures to database with neccesary details
    def insert_signature_database(self, device_name, signature_hex):

        sql_command = '''INSERT INTO device_configs (device_name, signature) VALUES (%s,%s)'''
        values = (device_name, signature_hex)

        self.cursor.execute(sql_command, values)
        self.sql.mydb.commit()
        
        print("Signature Inserted to Database")



    def create_key_pair(self, priv_key_name="private_key.pem", publ_key_name="public_key.pem"):

        print("Creating Key Pair")
        
        # Generate private key with 2048 bits
        private_key = RSA.generate(2048)

        # Generate matching public key
        public_key = private_key.publickey()

        # Write private key to file in PEM format
        with open(priv_key_name, "wb") as file_priv_key:
            file_priv_key.write(private_key.export_key("PEM"))

        # Write public key to file in PEM format
        with open(publ_key_name, "wb") as file_publ_key:
            file_publ_key.write(public_key.export_key("PEM"))


    # Create signatures for all devices currently located in database
    def create_signature_all(self, priv_key):

        print("Creating Signatures")

        # Open private key file otherwise raise error
        try:
            with open(priv_key, "r") as priv_key_file:
                private_key = RSA.import_key(priv_key_file.read())

        except FileNotFoundError:
            print("Private Key File Cannot Be Found!")

        
        # Find all devices to create signatures for
        find_devices = '''SELECT devicename, deviceid FROM inventory_2'''

        self.cursor.execute(find_devices)
        result = self.cursor.fetchall()

        for device in result:
            
            find_config = '''SELECT properties FROM {} WHERE object = 'device:{}'

                      '''.format(device[0], device[1])

            self.cursor.execute(find_config)
            device_result = self.cursor.fetchall()

            for result in device_result:

                # create hash from configuration files
                # Hashing function only accepts bytes strings
                device_config_hash = SHA256.new(str.encode(result[0]))
                # Sign the hashed files
                device_signature = pkcs1_15.new(private_key).sign(device_config_hash)

                # convert to hex string as this is much nicer to look at 
                device_signature_hex = device_signature.hex()

                # Insert the signature into the database
                self.insert_signature_database(device[0], device_signature_hex)


    # Use to create a single signature for single device id requested 
    def create_signature_single(self, priv_key, device_name, device_number):

        try:
            with open(priv_key, "r") as priv_key_file:
                private_key = RSA.import_key(priv_key_file.read())

        except FileNotFoundError:
            print("Private Key File Not Found!")

        find_config = '''SELECT properties FROM {} WHERE object = 'device:{}'

                    '''.format(device_name, device_number)

        self.cursor.execute(find_config)
        device_result = self.cursor.fetchall()

        for result in device_result:

            device_config_hash = SHA256.new(str.encode(result[0]))
            device_signature = pkcs1_15.new(private_key).sign(device_config_hash)
            device_signature_hex = device_signature.hex()

            self.insert_signature_database(device_name, device_signature_hex)
            

    # Verify signature using public key and specify device name and number
    def verify_signature(self, publ_key, device_name, device_number):

        try:
            with open(publ_key, "r") as publ_key_file:
                public_key = RSA.import_key(publ_key_file.read())

        except FileNotFoundError:
            print("Public Key File Not Found!")

        # Now retrieve the config again from the ones currently on database to check integrity
        find_config = '''SELECT properties FROM {} WHERE object = 'device:{}'
                    '''.format(device_name, device_number)

        self.cursor.execute(find_config)
        device_result = self.cursor.fetchall()

        sql_signature = '''SELECT signature FROM device_configs WHERE device_name = '{}'
        '''.format(device_name)

        self.cursor.execute(sql_signature)
        signature_hex = self.cursor.fetchall()

        # Convert hex string back to bytes as this is the only way to hash the thing
        for result in signature_hex:
            signature = bytes.fromhex(result[0])

        for dev in device_result:
        
            device_config_hash = SHA256.new(str.encode(dev[0]))

            # verify and return True or False depending whether verification is successful 
            try:
                verify_signature = pkcs1_15.new(public_key).verify(device_config_hash, signature)
                print("Valid Signature!")

                return True

            except (ValueError, TypeError):
                print("Signature Is Not Valid!")

                return False


sig = RSA_Signature()
#sig.create_key_pair()
#sig.create_signature_all(priv_key="private_key.pem")
sig.verify_signature(publ_key="public_key.pem", device_name="myBacnetDevice01", device_number="1234")

