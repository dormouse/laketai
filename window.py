#!/bin/env python
# -*- coding: utf8 -*-

# These are only needed for Python v2 but are harmless for Python v3.
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
from PyQt4 import QtGui, QtCore

import os
import subprocess
import sys

# from dialogs import OpenDlg
from editor import Editor
from views import HtmlView, TreeView


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.treeview = TreeView()
        self.editor = Editor()
        self.htmlview = HtmlView()
        self.setCentralWidget(splitter)
        splitter.addWidget(self.treeview)
        splitter.addWidget(self.editor)
        splitter.addWidget(self.htmlview)

        self.setWindowTitle("Lake Tai")
        self.setupMenus()
        self.showMaximized()

    def setupMenus(self):
        pass
