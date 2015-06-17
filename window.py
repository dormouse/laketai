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

from dialogs import OpenDlg
from editor import Editor
from views import HtmlView, TreeView


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.initAct()

        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.treeview = TreeView()
        self.editor = Editor()
        self.htmlview = HtmlView()
        self.setCentralWidget(splitter)
        splitter.addWidget(self.treeview)
        splitter.addWidget(self.editor)
        splitter.addWidget(self.htmlview)

        self.setWindowTitle("Lake Tai")
        self.initMenu()
        self.initToolbar()
        self.initStatusBar()
        self.showMaximized()

    def initAct(self):
        self.openPrjAct = QtGui.QAction(
            QtGui.QIcon("images/open.png"),
            "&Open Project",
            self,
            shortcut="Ctrl+O",
            statusTip="Open Project",
            triggered=self.openPrj
        )

        self.quitAct = QtGui.QAction(
            QtGui.QIcon('images/quit.png'),
            "&Close",
            self,
            shortcut=QtGui.QKeySequence.Close,
            statusTip=u"Quit",
            triggered=self.quit
        )

    def initMenu(self):
        self.fileMenu = self.menuBar().addMenu("&Project")
        self.fileMenu.addAction(self.openPrjAct)
        self.menuBar().addSeparator()
        self.fileMenu.addAction(self.quitAct)

    def initToolbar(self):
        self.prjToolBar = self.addToolBar("prj")
        self.prjToolBar.addAction(self.openPrjAct)

        self.proToolBar = self.addToolBar("pro")
        self.proToolBar.addAction(self.quitAct)

    def initStatusBar(self):
        self.statusBar().showMessage("Ready")

    def openPrj(self, prj_path=None):
        if prj_path:
            pass
        else:
            dlg = QtGui.QFileDialog()
            dlg.setFileMode(dlg.DirectoryOnly)
            dlg.setOption(dlg.ShowDirsOnly, True)
            prj_path = dlg.getExistingDirectory(
                self,
                'Please select project path',
                '',
            )



    def quit(self):
        self.close()
