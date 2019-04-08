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
                                                  password="root",
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

    def getModels(self):
        models = []
        for object in self.bucket.objects.all():
            models.append((object.key,object.get()))
        return models

    def uploadModel(self,filename, data):
        self.__uploadModelToS3(filename,data)




    def getUser(self,username):
        query = """SELECT password_hash, isAdmin FROM users WHERE username = ?"""
        clean_user = self.__sanitizeInput(username)
        self.cursor.execute(query,(clean_user,))
        result = self.cursor.fetchone()
        if result is not None:
            return result[0], result[1]
        else:
            print("No users with a matching username found")
            return 0, 0

    def registerUser(self, username, password):
        query = """INSERT INTO users (username, password_hash, isAdmin) VALUES (?, ?, 0)"""
        username = self.__sanitizeInput(username)
        hashed_password = hashlib.sha512(password.encode('utf8')).hexdigest()
        self.cursor.execute(query,(username,hashed_password))


    def __uploadModelToS3(self, filename, data):
        self.s3.upload_file('./Resources/Models/' + str(filename),BUCKET_NAME,filename)

    # def __retrieveModelsFromS3(self, url):
    #     #retrieve data from URL
    #     #Return data
    #     pass

    def __sanitizeInput(self,input):
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
    pass