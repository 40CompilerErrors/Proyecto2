import csv
import glob
import os

from PyQt5.QtWidgets import QFileDialog


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

    def saveCSV(self,dataframe,path=""):
        if path == "":
            path = QFileDialog.getExistingDirectory()

        dataframe.to_csv(os.path.join(path,"results.csv"))

        
