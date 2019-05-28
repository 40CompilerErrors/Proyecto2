import os

from Utilities.DB_Driver import DB_Driver as DB


class Model:

    def saveModel(self):
        pass


    def downloadModels(self):

        db =  DB.DB_Driver()

        for obj in self.bucket.objects.all():
            key = str(obj.key)
            print("Downloading " + key)
            # parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
            resources_path = os.path.join(os.getcwd(), 'Resources/Models')
            s3_path = os.path.join(resources_path,key)

            self.s3.meta.client.download_file(DB.BUCKET_NAME,key,s3_path)

        db.closeConnection()

    def uploadToS3(self, filename):
        db =  DB.DB_Driver()
        db.bucket.upload_file(('./Resources/Models/' + str(filename)), Key=filename)
        db.closeConnection()

