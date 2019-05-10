# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 09:43:04 2019

@author: javie
"""

from numpy import random

class AlgorithmController:

    
    def __init__(self, view, algorithm_name, TWB):
        self.view = view
        self.webcontroller = TWB
        self.errors = False
        
    def randomforest(self):
        self.errorestimators = False
        self.errorrandom = False
        self.errordepth = False
        
        if(self.view.dialog_estimators_RF.text().isdigit()):
            self.webcontroller.n_estimators = int(self.view.dialog_estimators_RF.text())
            self.errorestimators = False
        else:
            self.view.label_errors.setText("Fallos en el número de arboles")
            self.errorestimators = True
            
        if(self.view.dialog_random_RF.text().isdigit()):
            self.webcontroller.random_state = int(self.view.dialog_random_RF.text())   
            self.errorrandom = False
        else:
            self.view.label_errors.setText("Fallos en el random state")
            self.errorrandom = True
                  
        
        if(self.view.dialog_depth_RF.text() == "None" or self.view.dialog_depth_RF.text().isdigit()):
            if(self.view.dialog_depth_RF.text().isdigit()):
                self.webcontroller.max_depth = int(self.view.dialog_depth_RF.text())
            '''else:
                self.webcontroller.max_depth = self.view.dialog_depth_RF.text()'''
            self.errordepth = False
        else:
            self.view.label_errors.setText("Fallos en la profundidad máxima")
            self.errordepth = True
            
        self.webcontroller.verbose = int(self.view.dialog_verbose_RF.text())
        
        self.webcontroller.oob_score = bool(self.view.dialog_oob_RF.text())
        
        if(self.errorestimators == True or self.errordepth == True or self.errorrandom == True):
            self.errors = True
        else:
            self.errors = False
        
        if self.errors == False:
            self.view.close()
        else:
            self.view.label_errors.setVisible(True)
            
                
        
    def naivebayes(self):
        self.webcontroller.var_smoothing = float(self.view.dialog_NB.text())
        self.view.close()
        
    def svm(self):
        self.webcontroller.random_state = int(self.view.dialog_random_SVM.text())
        self.webcontroller.verbose = int(self.view.dialog_verbose_SVM.text())
        self.webcontroller.shrinking = bool(self.view.dialog_shrinking_SVM.text())
        self.webcontroller.max_iter = int(self.view.dialog_max_iter_SVM.text())        
        self.view.close()