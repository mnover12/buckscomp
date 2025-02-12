# packages
from copy import deepcopy

import numpy as np
from fontTools.subset.svg import xpath
from numpy.ma.core import subtract
import pandas as pd
from fontTools.misc.cython import returns
import matplotlib.pyplot as plt
import seaborn as sns
import os

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

# files
mainDir = r"C:\Users\mvnov\Hackathon"
ticketSheet = mainDir+r"\Data\Prompt2\Prompt2Tickets.csv"
retailSheet = mainDir+r"\Data\Prompt2\Prompt2Retail.csv"
foodSheet = mainDir+r"\Data\Prompt2\Prompt2F&B.csv"
customerSheet = mainDir+r"\Data\Prompt2\Prompt2Demographics.csv"

# variables
ticketData = pd.read_csv(ticketSheet)
retailData = pd.read_csv(retailSheet)
foodData = pd.read_csv(foodSheet)
consumerData = pd.read_csv(customerSheet)

# classes
class Node:
    def __init__(self, data, id):
        self.Id = deepcopy(id)
        self.data = deepcopy(data)
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def InsertBegin(self, data, id): # put it at the start
        new_node = Node(data, id)
        new_node.next = self.head
        self.head = new_node

    def GetIndexFromId(self, Id): # get index number from ID number
        if self.head is None:
            return 0

        current_node = self.head
        previd = current_node.Id
        indx = 0
        while (current_node is not None) and (previd < Id):
            current_node = current_node.next
            previd = current_node.Id
            indx += 1

        print(indx)
        return indx

    def AddData(self, data):
        print("adding data")

    def insertAtIndex(self, data, index, id):
        if index == 0:
            self.InsertBegin(data, id)
            return

        position = 0
        current_node = self.head
        while (current_node is not None) and (position + 1 != index):
            position += 1
            current_node = current_node.next

        print(current_node)
        print(current_node.next)
        if (current_node is not None) and (current_node.next is None):
            new_node = Node(data, id)
            new_node.next = current_node.next
            current_node.next = new_node
        else:
            print("adding onto existing nupa")
            z = current_node.data
            z = pd.concat([z, pd.Series([data])], ignore_index=True)
            self.data = z

    def updateNode(self, val, index):
        current_node = self.head
        position = 0
        while current_node is not None and position != index:
            position += 1
            current_node = current_node.next

        if current_node is not None:
            current_node.data = val

    def sizeOfLL(self):
        size = 0
        current_node = self.head
        while current_node:
            size += 1
            current_node = current_node.next
        return size

    def printLL(self):
        current_node = self.head
        while current_node:
            current_node = current_node.next

def llLoad(data, x, y, varfil, on):
    packet = pd.DataFrame(list(zip(data.iloc[:, x], data.iloc[:, y])), columns=[data.columns[x], data.columns[y]])

    if on:
        try:
            X_train, X_test, Y_train, Y_test = train_test_split(packet[data.columns[x]].values.reshape(-1, 1), packet[data.columns[y]].values, test_size=0.2)
            scaler = StandardScaler()
            X_train = scaler.fit_transform(X_train)
            X_test = scaler.transform(X_test)

            # the actual model
            knn = KNeighborsClassifier(n_neighbors=5)
            knn.fit(X_train, Y_train)
            y_pred_knn = knn.predict(X_test)

            varfil.write(str(ticketData.columns[col]) + " vs. " + str(ticketData.columns[cross]) + " knn results:\n")
            varfil.write("\nAccuracy for " + str(ticketData.columns[col]) + " vs. " + str(ticketData.columns[cross]) + ": " + str(accuracy_score(Y_test, y_pred_knn)))
            varfil.write("\nClassification Report for " + str(ticketData.columns[col]) + " vs." + str(ticketData.columns[cross]) + ":\n" + str(classification_report(Y_test, y_pred_knn)))

        except:
            varfil.write(str(ticketData.columns[col]) + " vs. " + str(ticketData.columns[cross]) + " knn results:\n")
            varfil.write("Error in Generating.")

    return packet

def Graphing(packet, colum, cross):
    # graph the data
    gra = sns.jointplot(data=packet, kind='scatter', x=colum, y=cross, s=8,marker='x', color='blue', alpha=0.6)
    gra.fig.suptitle(colum + " vs. " + cross, size=16)
    gra.fig.subplots_adjust(top=0.95)
    gra.fig.set_size_inches(12, 10)

    return gra

# code
UserDataBase = LinkedList()
sns.set_theme(style = "darkgrid")
currentsheet = ticketData

for col in range(0, len(currentsheet.columns.tolist())):
    if (col == 0):
        for userindex in range(0, len(currentsheet.iloc[:, 0])):
            databasedata = currentsheet.loc[userindex, :]
            z = currentsheet.iloc[:, 0][userindex]
            #print("Currently Adding:"+ str(z)+" | index: "+ str(UserDataBase.GetIndexFromId(z))+ "\n")
            UserDataBase.insertAtIndex(databasedata, UserDataBase.GetIndexFromId(z), z)
            #UserDataBase.printLL()

    #for cross in range(0, len(currentsheet.columns.tolist())):
     #   if cross != col:

            # create folder for info
      #      filename = currentsheet.columns[col] + "_" + currentsheet.columns[cross]
       #     fold = os.mkdir(mainDir + "\\Graphs\\" + filename)
        #    with (open(mainDir + "\\Graphs\\" + filename + "\\ClusterData.txt", "w") as file):

                # data manipulation, clustering, and graphing
         #       packet = llLoad(currentsheet, col, cross, file, True)
          #      gra = Graphing(packet, currentsheet.columns[col], currentsheet.columns[cross])

                # save/show results
           #     gra.savefig(mainDir + "\\Graphs\\" + filename + "\\PicGraph.png", dpi=400)
