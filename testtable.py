from PyQt5 import QtGui,QtCore
from PyQt5.QtWidgets import QApplication,  QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
import sys
import csv
import threading
#import subprocess
#subprocess.call("python hackboutview.py",shell=True)
def a():
    import os
    os.system("python hackboutview.py")
t3=threading.Thread(target=a)
t3.start()
import firebase_admin
from firebase_admin import credentials,db
import time
cred = credentials.Certificate("hackbout.json")
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://hackbout-ed3ed.firebaseio.com/'
})
updatedata=0
root=db.reference()
def checkdata():
    global root
    global updatedata
    
    root.set("")
    root.update({"active":1})
    data=root.get()
    prevlen=len(data)
    while True:
        data=root.child("live").get()
        if data is not None:
            if len(data)>prevlen:
                print(data[prevlen:])
                data1=data[prevlen:][-1].split(",")
                prevlen=len(data)
                
                print(data1)
                updatedata=(data1)
        time.sleep(5)

t1 = threading.Thread(target=checkdata)
class Window(QWidget):
    def __init__(self):
        super().__init__()
        
        self.title = "PyQt5 Tables"
        self.top = 100
        self.left = 100
        self.width = 500
        self.height = 400

        self.InitWindow()
        QtCore.QTimer.singleShot(500, self.OnLoad)

    def OnLoad(self):
        global updatedata
        if updatedata!=0:
            self.adddata(updatedata)
            updatedata=0
        print("hi")
        QtCore.QTimer.singleShot(3000, self.OnLoad)
    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        
        self.val=0
        self.creatingTables()

        self.show()
        

    def creatingTables(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(170)
        self.tableWidget.setColumnCount(5)

        dat=csv.reader(open("datahack.csv","r"),delimiter=",")
        data=list(dat)
        print(data,len(data))
        
        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.addWidget(self.tableWidget)
        self.setLayout(self.vBoxLayout)
        for i in range(0,len(data)):
            for j in range(5):
                self.tableWidget.setItem(i,j, QTableWidgetItem(data[i][j]))
        self.val=len(data)
        
    def adddata(self,data):
        self.val+=1
        for j in range(4):
                self.tableWidget.setItem(self.val-1,j, QTableWidgetItem(str(data[j])))
        self.tableWidget.setItem(self.val-1,4, QTableWidgetItem(str(data[-1][-8:])))
        
try:
    App = QApplication(sys.argv)
    window = Window()
    t1.start()
    sys.exit(App.exec())
    t1.stop()
finally:
    root.update({"active":0})