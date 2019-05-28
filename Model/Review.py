import csv
import glob
import os


class Review:

    def loadCSV(self,path=""):
        if path == "":
            pass #Select a path here

        file_pattern = os.path.join(dir, '*.csv')
        file_list = glob.glob(file_pattern)

        rows = []

        for file in file_list:
            with open(file) as csvfile:
                readCSV = csv.reader(csvfile, delimiter=',')
                for row in readCSV:
                    rows += row[1]

        return rows

    def saveCSV(selfs,dataframe,path=""):
        if path == "":
            pass #Select a path here

        
