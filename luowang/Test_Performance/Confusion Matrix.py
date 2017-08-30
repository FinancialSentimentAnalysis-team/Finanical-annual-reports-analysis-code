# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 19:42:59 2017

@author: Administrator
"""
from sklearn.metrics import confusion_matrix

def get_confusion_matrix(y_true, y_pred):
    return confusion_matrix(y_true, y_pred)


                    
if __name__ == '__main__':
    y_true=[1,1,-1,-1,0,-1,0,1]
    y_pred=[1,-1,-1,0,0,1,0,-1]
    temp_matrix=get_confusion_matrix(y_true, y_pred)
                            
                          
