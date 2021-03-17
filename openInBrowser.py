import os
import logging
import processing
import webbrowser
from functools import partial
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import QSettings, QPoint, Qt, pyqtSignal, QVariant, QUrl
from PyQt5.QtGui import QCursor, QPixmap, QColor
from PyQt5 import Qt, QtCore, QtWidgets, QtGui, QtWebKit, QtWebKitWidgets, QtXml, QtNetwork, uic
from qgis.gui import QgsVertexMarker, QgsRubberBand, QgsMapToolEmitPoint
from qgis.gui import QgsMapToolEmitPoint
from PyQt5.QtWebKitWidgets import QWebView
from qgis.core import (
    QgsProject,
    QgsDataSourceUri,
    QgsVectorLayer,
    QgsVectorFileWriter,
    QgsField,
    QgsPointXY,
    QgsFeature,
    QgsGeometry,
    QgsDistanceArea,
    QgsPalLayerSettings,
    QgsDistanceArea,
    QgsPolygon,
    QgsConstWkbPtr,
    QgsSnappingConfig,
    QgsCoordinateReferenceSystem,
    QgsWkbTypes,
    QgsLayerTreeGroup,
    QgsLayerTreeLayer,
    QgsFeatureRequest,
    QgsExpressionContextUtils,
    QgsCoordinateTransform,
    QgsApplication
)

class OpenInBrowser:

    basePath=None
    def __init__(self, iface):
        self.project = QgsProject.instance()
        self.iface=iface
        self.pluginPath = os.path.dirname(__file__)
        self.canvas = iface.mapCanvas()
        self.pointTool = QgsMapToolEmitPoint(self.canvas)
        self.pointTool.canvasClicked.connect(self.display_point)
        self.canvas.setMapTool(self.pointTool)
        self.display_point(self.pointTool)
        self.ui_browserPath = uic.loadUi(os.path.join(self.pluginPath,'gui/browserPath.ui'))                
        self.ui_browserPath.btn_ok.clicked.connect(self.setBrowserPath)
        self.getBasePath()
        QgsApplication.messageLog().messageReceived.connect(self.write_log_message)
        self.widget = uic.loadUi(os.path.join(self.pluginPath,'gui', 'browserView.ui'))
        
        self.apdockwidget=QtWidgets.QDockWidget("browserView" , self.iface.mainWindow() )
        self.apdockwidget.setObjectName("browserView")
        self.apdockwidget.setWidget(self.widget)
        self.iface.addDockWidget( QtCore.Qt.LeftDockWidgetArea, self.apdockwidget)
        self.apdockwidget.update()


    

    def write_log_message(message, tag, level):
        with open('C:/Users/Boden_Aaron/Documents/qgis.log', 'a') as logfile:
            logfile.write('{tag}({level}): {message}'.format(tag=tag, level=level, message=message))

    
    def display_point(self, pointTool):       
        try:                       
            geom = QgsGeometry.fromPointXY(QgsPointXY(pointTool.x(),pointTool.y()))
            sourceCrs = QgsCoordinateReferenceSystem(QgsProject.instance().crs().authid())
            destCrs = QgsCoordinateReferenceSystem(4326)
            tr = QgsCoordinateTransform(sourceCrs, destCrs, QgsProject.instance())

            geom.transform(tr)
            point = geom.asPoint() # QgsPointXY

            print(QgsPointXY(pointTool.x(),pointTool.y()))
            lat = str(point.y())
            lon = str(point.x())
            print(lat,lon,self.basePath)
            url = self.basePath+"?v_lat="+lat+"&v_lng="+lon
            print(url)
            #webbrowser.open(url)
            qstr = self.QString(url)
            qurl = QUrl()
            qurl.setUrl(qstr)
            print(qurl)
            #self.widget.SV.load(QUrl(url))
            #self.widget.SV.load(QUrl(url))
            #self.widget.SV.load(QUrl('https://demo3-small-82766907-4a67-4536-9bad-daf6bafdfef8.s3.eu-central-1.amazonaws.com/index.html'))
            #self.widget.SV.load(QUrl('https://goo.gl/maps/hdzvfMGgRSaF7p8r9'))
            self.widget.SV.load(QUrl(self.basePath))
            
            #self.apdockwidget.update()
        except AttributeError as a:
            print(a)            

    def QString(self, x):
        return x

    def getBasePath(self):        
        
        self.basePath=QgsExpressionContextUtils.projectScope(self.project).variable('BrowserPath')
        if self.basePath == None:
            self.ui_browserPath.show()

    def setBrowserPath(self):
        QgsExpressionContextUtils.setProjectVariable(self.project,'BrowserPath',self.ui_browserPath.txt_browserPath.text())
        self.ui_browserPath.close()
        self.getBasePath()