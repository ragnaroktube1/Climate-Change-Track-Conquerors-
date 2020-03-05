import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog,QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5.uic import loadUi
window_name = "window"
interframe_wait_ms = 1

import plotly.express as px
px.set_mapbox_access_token("pk.eyJ1Ijoic3VtdWtoMTIzIiwiYSI6ImNrN2RyZHgxbzBjbzczZHFrOTk2MzQxNTUifQ.Ip-uM7Lv_UOz6CGEUG_Njg")
import pandas as pd
df=pd.read_csv("datahack.csv")
fig = px.scatter_mapbox(df, lat="lat", lon="lan",color="data1", size="data2",
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=12)
import firebase_admin
from firebase_admin import credentials,db
import time
cred = credentials.Certificate("hackbout.json")
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://hackbout-ed3ed.firebaseio.com/'
})

root=db.reference()

class life(QDialog):
    def __init__(self):
        super(life,self).__init__()
        loadUi("showbutton.ui",self)
        self.setWindowTitle("Traffic")
        self.pushButton.clicked.connect(self.onpush)
    @pyqtSlot()
    def onpush(self):
        data=root.child("live").get()
        print(data)
        if data is not None:
            for i in range(1,len(data)):
                new=data[i].split(",")
                df.append({"lat":new[0],"lan":new[1],"data1":new[2],"data2":new[3],"time":new[4]},ignore_index=True)
        fig.show()
                
app=QApplication(sys.argv)
widget=life()
widget.show()
sys.exit(app.exec_())