# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 09:35:36 2019

@author: javie
"""

from PyQt5.QtWidgets import QApplication, QDialog
from Controllers import AlgorithmController as AC
from PyQt5.uic import loadUi

class AlgorithmDialog(QDialog):
    def __init__(self, algorithm_name):
        super(AlgorithmDialog, self).__init__()
        
        self.controller = AC.AlgorithmController(self, algorithm_name)
        
        if(algorithm_name=='Random Forest'):
            print('Pelo de Gon')
        elif(algorithm_name=='Naive Bayes'):
            loadUi('./Resources/UI/DialogNaiveBayes.ui', self)
    
            self.setWindowTitle('Editor de algoritmo Naive Bayes')
        self.buttonActions(algorithm_name)
        
    def buttonActions(self, algorithm_name):
        if(algorithm_name=='Random Forest'):
            print('Ultra Instinct')
        elif(algorithm_name=='Naive Bayes'):
            self.buttonBox_NB.accepted.connect(self.controller.editar)
            self.buttonBox_NB.rejected.connect(self.reject)
        