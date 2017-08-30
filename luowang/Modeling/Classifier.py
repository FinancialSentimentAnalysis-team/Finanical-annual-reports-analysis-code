from __future__ import division
import numpy as np
#import xgboost as xgb
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn import naive_bayes
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from GCForest import gcForest


### logistic regression classifier############################## 
def test_LogisticRegression(*data):
    X_train, X_test, y_train, y_test=data
    try:
        cls=LogisticRegression(C=1)
        cls.fit(X_train, y_train)
        cls.predict(X_test)
        return cls.predict(X_test)
    except Exception:
        return [0]*len(X_test)
### test following paramters:
#C=np.logspace(-2, 4, num=100)
###
      
        
### decision tree classifier############################## 
def test_DecisionTreeClassifier(*data):
    
    X_train, X_test, y_train, y_test=data
    try:
        cls=DecisionTreeClassifier()
        cls.fit(X_train, y_train)
        return cls.predict(X_test)
    except Exception:
        return [0]*len(X_test)
    ###
    '''
   criterions=['gini', 'entropy']
   splitter=['best', 'random']
   max_depth=np.arrange(1, maxdepth)
   ''' 
   ###
        

 #### svm classifier##############################  
def test_SVC_rbf(*data):
    X_train, X_test, y_train, y_test=data
    cls=svm.SVC(kernel='rbf', gamma=10)
    cls.fit(X_train, y_train)
    return cls.predict(X_test)
### test paramters: gamma  for svm.SVC
'''
gamma=range(1, 20)

'''
###

def test_SVR_rbf(*data):
    X_train, X_test, y_train, y_test=data
    cls=svm.SVR(kernel='rbf', gamma=10)
    cls.fit(X_train, y_train)
    return cls.predict(X_test)
###
'''test following paramters:
gamma=range(1,20)
''' 
###

##########random forest classifier##############################    
def test_RandomForestClassifier(*data):
    X_train, X_test, y_train, y_test=data
    clf = RandomForestClassifier(n_estimators=11)
    clf.fit(X_train, y_train)
    return clf.predict(X_test)


############# gcforest classifier############################## 
def test_GcForest(*data):
    X_train, X_test, y_train, y_test=data
    gcf=gcForest()
    gcf.fit(X_train, y_train)
    return gcf.predict(X_test)


def test_XGBoost(*data):
    X_train, X_test, y_train, y_test=data
    xg_train=xgb.DMatrix(X_train, label=y_train)
    xg_test=xgb.DMatrix(X_test, label=y_test)
    
    ### setup parameters for xgboost
    param={}
    
    ## use softmax multi-class classification
    param['objective']='multi:softmax'
    
    ### scale weight of positive example
    param['eta']=0.1
    param['max_depth']=6
    param['silent']=1
    param['nthread']=4
    param['num_class']=6

    watchlist =[(xg_train, 'train'),(xg_test, 'test')]
    num_round=5
    bst=xgb.train(param, xg_train, num_round, watchlist)
    
    # get prediction
    pred=bst.predict(xg_test)
    error_rate=np.sum(pred != y_test)/y_test.shape[0]
    print ('Test error using softmax = {}'.format(error_rate))
    
    ### do the same thing again, but output probabilities
    param['objective']='multi:softprob'
    bst=xgb.train(param, xg_train, num_round, watchlist)

    ### get prediction, this is in ID array, need reshape to (ndata, nclass)
    pred_prob=bst.predict(xg_test).reshape(y_test.shape[0],6)
    pred_label=np.argmax(pred_prob, axis=1)
    error_rate=np.sum(pred!=y_test)/y_test.shape[0]
    print ('Test error using softprob = {}'. format(error_rate))
    return pred
    
