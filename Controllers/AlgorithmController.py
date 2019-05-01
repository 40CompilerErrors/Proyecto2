# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 09:43:04 2019

@author: javie
"""

class AlgorithmController:

    
    def __init__(self, view, algorithm_name, TWB):
        self.view = view
        self.webcontroller = TWB
        
    def randomforest(self):
        self.webcontroller.n_estimators = int(self.view.dialog_estimators_RF.text())
        self.webcontroller.random_state = int(self.view.dialog_random_RF.text())
        self.view.close()
        
    def naivebayes(self):
        print(self.view.dialog_NB.text())
        self.view.close()