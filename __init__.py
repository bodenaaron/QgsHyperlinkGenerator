# -*- coding: utf-8 -*-

__author__ = 'Aaron Boden Eictronic GmbH'
__date__ = 'March 2021'
__copyright__ = '(C) 2021 Aaron Boden Eictronic GmbH'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

def classFactory(iface):
    from .plugin import Hyperlinkgenerator
    return Hyperlinkgenerator(iface)

