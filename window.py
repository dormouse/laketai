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

PRJ_NAME = u'Lake Tai'
DEFAULT_INDEX = u'index.rst'


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.prj_path = None

        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.treeview = TreeView()
        self.editor = Editor()
        self.htmlview = HtmlView()
        self.setCentralWidget(splitter)
        splitter.addWidget(self.treeview)
        splitter.addWidget(self.editor)
        splitter.addWidget(self.htmlview)

        self.setWindowTitle(PRJ_NAME)
        self.initAct()
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
        if not prj_path:
            dlg = OpenDlg()
            prj_path = dlg.getExistingDirectory(self)

        if prj_path:
            try:
                sys.path.insert(0, prj_path)
                import conf
            except:
                return

            self.setWindowTitle(PRJ_NAME + u' -- ' + conf.project)
            self.prj_path = prj_path
            self.handleFileChanged()

    def handleFileChanged(self, filename=None):
        if not filename:
            filename = DEFAULT_INDEX
        full_filename = os.path.join(self.prj_path, filename)
        html_filename = u'_build/html/%s.html' %\
            os.path.splitext(filename)[0]
        full_html_filename = os.path.join(self.prj_path, html_filename)
        print full_html_filename

        self.treeview.load_dir(self.prj_path)
        self.editor.openFile(full_filename)
        self.htmlview.load_html(full_html_filename)

    def quit(self):
        self.close()
