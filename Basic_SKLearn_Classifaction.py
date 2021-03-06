#This code is under the beer licence
#This code only works for numerial and one boolean values
#Ues boolean for the decession callculation
#Need to add folder location to csv folder on line 22,23,27
#testColumn name needed on 44,45,46

import glob, os
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

#================================
pd.set_option('display.max_colwidth', -1) # displays content from given folder
#================================
#function to rename given files
def rename(dir, pathAndFilename, pattern, titlePatteren):
    os.remane(pathAndFilename, os.path.join(dir, titlePatteren)) # methdoe to do the rename

# search for csv files in working folder
path = os.path.expanduser("/Folder_name/Sub_Foldername/*.csv") #pass folder name here

#iterate and remane them one by one with the number of the iteration
for i, fname in enumerate(glob.glob(path)): # change file name to add numbee
    rename(os.path.expanduser('~/Folder_name/Sub_Foldername/'), fname, r'*.csv', r'test{}.csv'.format(i))# change file name without changing extention e.g ".csv"

#Change spearator for CSV file
#this is setup to use 4 files, comment out or add more if required
df1 = pd.read_csv('~/Folder_name/Sub_Foldername/file_01.csv', sep=";")
df2 = pd.read_csv('~/Folder_name/Sub_Foldername/file_02.csv', sep=";")

#Choose the files you want to use
#remove df# or add df# if required
frames = [df1, df2]

#concatente multiple data csv files
data = pd.concat(frames)

#================================
#Seperate the data needed for the AI to learn
#
data['TestColumn'] = [0 if x == 'True' else 1 for x in data['TestColumn']]
X = data.drop('TestColumn',1)
y = data.TestColumn
#=========================================================================
#This is the magic part where we let the program hide data from itself
#=========================================================================
#Train and Test splitting data
#X_train = data set we are going to use to train Classifier with
#X_test = information we don't let he program see, so it can test itself
#y_train = the training data giving the answers we want
#y_test = data we test to see if program gives us the right answer
#Test split, part of SKlearn lib
#test size is the % of data to test
#Random state is just a random seed number, just grabs random numbers in the data set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state= 42)

#Applying a stander scaler to optimise the results, imported with sklearn lib above
#fit transform is to fit the data better
sc = StandardScaler()
X_train = sc.fit_transform(X_train)#this reducs bias in columns that have high numbers or low numbers (changes most data in the X_training data to a value between 0 - 1)
X_test  = sc.transform(X_test)# we want to keep the train and test data the same
X_train[:10]#print out the 1st 10 data on the training data, this is just default

#==============================
#Random Forest Classifier
#Look mammy I'm programming AI, (Classifier with is a fancy way to say organise the data)
#used for medium size data set
#==============================
#Object label = Classifier (how many trees do you want)
rfc = RandomForestClassifier(n_estimators=200)
rfc.fit(X_train, y_train)# just does a simple fit of the data we seperated out for training
pred_rfc = rfc.predict(X_test)# predect the test values
#How the Forest Classifier preforms
print("Random Forest")
print(classification_report(y_test, pred_rfc)) # how the test data compares to the predected values
print(confusion_matrix(y_test, pred_rfc))# this give us a matrix on the mislabels between good  and bad

#=================================
##SVM Classifier
#Support Vector Model
#Libary is pretty much the same as other libs
#=================================
clf = svm.SVC()#calling the function
clf.fit(X_train, y_train)# just does a simple fit of the data we seperated out for training
pred_clf = clf.predict(X_test)# predect the test values
#How the CLF model preformes
print("SVM Classification")
print(classification_report(y_test, pred_clf))# how the test data compares to the predected values
print(confusion_matrix(y_test, pred_clf))# this give us a matrix on the mislabels between good  and bad

#=================================
##Neural Network
#hidden layers is the nodes in the NN
#Good for text based code or big data sets, picture processing
#==================================
#object = Classifier(how many nodes in each layer, max many iterations
mlpc = MLPClassifier(hidden_layer_sizes=(11,11,11),max_iter=500)
mlpc.fit(X_train, y_train)
pred_mlpc = mlpc.predict(X_test)
#How the NN model preformes
print("Neural Network")
print(classification_report(y_test, pred_mlpc))# how the test data compares to the predected values
print(confusion_matrix(y_test, pred_mlpc))# this give us a matrix on the mislabels between good  and bad

#Score the AI
from sklearn.metrics import accuracy_score #Test scrore
bn = accuracy_score(y_test, pred_rfc) #Labelling code for printing
dm = accuracy_score(y_test, pred_clf) #Labelling code for printing
cm = accuracy_score(y_test, pred_mlpc) #Labelling code for printing
print(bn, ' is the Forest score')
print(dm, ' is the SVM Classification score')
print(cm, ' is the Neural Network score')
