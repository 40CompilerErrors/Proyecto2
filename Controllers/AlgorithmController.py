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
        if(self.view.dialog_depth_RF.text() != "None"):
            self.webcontroller.max_depth = int(self.view.dialog_depth_RF.text())
        self.webcontroller.verbose = int(self.view.dialog_verbose_RF.text())
        self.webcontroller.oob_score = bool(self.view.dialog_oob_RF.text())
        self.view.close()
        
    def naivebayes(self):
        self.webcontroller.var_smoothing = float(self.view.dialog_NB.text())
        self.view.close()