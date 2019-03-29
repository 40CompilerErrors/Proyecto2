import mysql.connector



class DB_Driver:

    def __init__(self):
        # Setup s3 driver
        self.connection = mysql.connector.connect(host="",
                                                  database="",
                                                  user="",
                                                  password="")

        if self.connection.is_connected():
            db_Info = self.connection.get_server_info()
            print("Connected to MySQL database... MySQL Server version on ", db_Info)
            cursor = self.connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You are connected to - ", record)
        else:
            raise AssertionError('Connection to the DB could not be established')

    def getModels(self):
        # fetch all from database
        # Retrieve the data from the URL
        # Return them as an array of tuples
        pass

    def uploadModel(self):
        #upload to S3
        #Get the URL and
        #Upload it to DB with a given name
        pass

    def uploadModel(self):
        # upload to S3
        # Get the URL and
        # Upload it to DB with a given name
        pass

    def getUser(self,username):
        #get the username and the password hash
        pass


    def closeConnection(self):
        #close the connection
        pass

    def __uploadToS3(self, data):
        #upload to S3
        #Return the resulting URL
        pass

    def __retrieveFromS3(self, url):
        #retrieve data from URL
        #Return data
        pass
