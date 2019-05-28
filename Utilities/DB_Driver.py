import os

import mysql.connector
import boto3
import hashlib

BUCKET_NAME = 'gge-opiniones'
keyFile = open('./Resources/keys.txt', 'r') #Keyfile is in gitignore. Must be added manually
PUBLIC_KEY = keyFile.readline().rstrip()
PRIVATE_KEY = keyFile.readline().rstrip()

class DB_Driver:

    def __init__(self):
        self.session = boto3.Session(
            aws_access_key_id= PUBLIC_KEY,
            aws_secret_access_key= PRIVATE_KEY
        )
        self.s3 = self.session.resource('s3')
        self.bucket = self.s3.Bucket(BUCKET_NAME)

        self.connection = mysql.connector.connect(host="localhost",
                                                  port = "3306",
                                                  database="proyecto2",
                                                  user="root",
                                                  password="",
                                                  use_pure=True)

        if self.connection.is_connected():
            db_Info = self.connection.get_server_info()
            print("Connected to MySQL database... MySQL Server version on ", db_Info)
            cursor = self.connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You are connected to - ", record)
        else:
            raise AssertionError('Connection to the DB could not be established')

        self.cursor = self.connection.cursor(prepared = True)


    def sanitizeInput(self,input):
        sanitized=""
        for character in input:
            if character == "'" or character ==")" or character == ";":
                break
            else:
                sanitized += character
        return sanitized


    def closeConnection(self):
        self.connection.close()

if __name__ == "__main__":
    #tests go here if needed
    db = DB_Driver()
    model = db.getModels()
    for i in model:
        print(i[0])