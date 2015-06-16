#!/bin/env python
# -*- coding: utf8 -*-

# These are only needed for Python v2 but are harmless for Python v3.
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
from PyQt4 import QtCore, QtGui, QtWebKit


class HtmlView(QtWebKit.QWebView):
    def __init__(self, parent=None):
        super(HtmlView, self).__init__(parent)

    def load(self, path):
        """
            Load the specified HTML file.
        """
        self.load(QtCore.QUrl.fromLocalFile(path))


class TreeView(QtGui.QTreeView):
    def __init__(self, parent=None):
        super(TreeView, self).__init__(parent)
