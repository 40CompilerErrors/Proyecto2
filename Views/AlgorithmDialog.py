# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 09:35:36 2019

@author: javie
"""

from PyQt5.QtWidgets import QApplication, QDialog
from Controllers import AlgorithmController as AC
from PyQt5.uic import loadUi

class AlgorithmDialog(QDialog):
    def __init__(self, algorithm_name, webcontroller):
        super(AlgorithmDialog, self).__init__()
        
        self.controller = AC.AlgorithmController(self, algorithm_name, webcontroller)
        
        
        if(algorithm_name=='Random Forest'):
            loadUi('./Resources/UI/DialogRandomForest.ui', self)    
            self.setWindowTitle('Editor de algoritmo Random Forest')
        elif(algorithm_name=='Naive Bayes'):
            loadUi('./Resources/UI/DialogNaiveBayes.ui', self)
            self.setWindowTitle('Editor de algoritmo Naive Bayes')
        elif(algorithm_name=='SVM'):
            loadUi('./Resources/UI/DialogSVM.ui', self)
            self.setWindowTitle('Editor de algoritmo SVM')
        self.label_errors.setVisible(False)
        self.buttonActions(algorithm_name)
        
    def buttonActions(self, algorithm_name):
        if(algorithm_name=='Random Forest'):
            self.buttonBox_RF.accepted.connect(self.controller.randomforest)
            self.buttonBox_RF.rejected.connect(self.reject)
        elif(algorithm_name=='Naive Bayes'):
            self.buttonBox_NB.accepted.connect(self.controller.naivebayes)
            self.buttonBox_NB.rejected.connect(self.reject)
        elif(algorithm_name=='SVM'):
            self.buttonBox_SVM.accepted.connect(self.controller.svm)
            self.buttonBox_SVM.rejected.connect(self.reject)
        