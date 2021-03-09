import os
import logging
import processing
import webbrowser
from functools import partial
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import QSettings, QPoint, Qt, pyqtSignal, QVariant, QUrl
from PyQt5.QtGui import QCursor, QPixmap, QColor
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
    QgsCoordinateTransform
)

class OpenInBrowser:

    basePath=None
    def __init__(self, iface):
        self.iface=iface
        self.getBasePath()
        self.canvas = iface.mapCanvas()
        self.pointTool = QgsMapToolEmitPoint(self.canvas)
        self.pointTool.canvasClicked.connect(self.display_point)
        self.canvas.setMapTool(self.pointTool)
        self.display_point(self.pointTool)

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
            webbrowser.open(url)
        except AttributeError:
            pass


    def getBasePath(self):
        project = QgsProject.instance()
        self.basePath=QgsExpressionContextUtils.projectScope(project).variable('BrowserPath')
        