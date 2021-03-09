# -*- coding: utf-8 -*-

__author__ = 'Aaron Boden Eictronic GmbH'
__date__ = 'March 2021'
__copyright__ = '(C) 2021 Aaron Boden Eictronic GmbH'

import os
import webbrowser

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .openInBrowser import OpenInBrowser
        

class Hyperlinkgenerator:
    def __init__(self, iface):
        self.iface = iface
        self.pluginPath = os.path.dirname(__file__)                       
        

    def initGui(self):               
    
        self.mainMenu = QMenu(self.iface.mainWindow())
        self.mainMenu.setObjectName('HyperlinkGenerator')
        self.mainMenu.setTitle('HyperlinkGenerator')
        
        self.menuBar = self.iface.mainWindow().menuBar()
        self.menuBar.insertMenu(self.iface.firstRightStandardMenu().menuAction(), self.mainMenu)
        self.toolbar = self.iface.addToolBar('HyperlinkGenerator')
        
        self.openInBrowser = QAction('Im Browser öffnen', self.iface.mainWindow())
        self.openInBrowser.setIcon(QIcon(os.path.join(self.pluginPath, 'icons', 'openInBrowser.png')))
        self.mainMenu.addAction(self.openInBrowser)
        self.toolbar.addAction(self.openInBrowser)
        self.openInBrowser.triggered.connect(self.startOpenInBrowser)           
        
    def startOpenInBrowser(self):
        self.gui = OpenInBrowser(self.iface)
        
    def unload(self):                
        self.mainMenu.deleteLater()
        