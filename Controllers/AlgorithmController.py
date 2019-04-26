# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 09:43:04 2019

@author: javie
"""

class AlgorithmController:
    def __init__(self, view, algorithm_name):
        self.view = view
        
    def editar(self):
        print(self.view.dialog_NB.text())
        self.view.close()