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
from views import HtmlView, TreeView

PRJ_NAME = u'Lake Tai'
DEFAULT_INDEX = u'index.rst'
DEFAULT_CONF = u'conf.py'


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.prj_path = None
        self.filename = None

        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.treeview = TreeView()
        self.htmlview = HtmlView()
        self.setCentralWidget(splitter)
        splitter.addWidget(self.treeview)
        splitter.addWidget(self.htmlview)

        self.setWindowTitle(PRJ_NAME)
        self.init_act()
        self.init_menu()
        self.init_toolbar()
        self.init_statusbar()
        self.show()
        # self.showMaximized()

    def init_act(self):
        # all pic from /usr/share/icons/Mint-X/actions/32

        self.openPrjAct = QtGui.QAction(
            QtGui.QIcon("images/open.png"),
            "&Open Project",
            self,
            shortcut="Ctrl+O",
            statusTip="Open Project",
            triggered=self.open_prj
        )

        self.quitAct = QtGui.QAction(
            QtGui.QIcon('images/exit.png'),
            "&Close",
            self,
            shortcut=QtGui.QKeySequence.Close,
            statusTip=u"Quit",
            triggered=self.quit
        )

        self.editAct = QtGui.QAction(
            QtGui.QIcon('images/edit.png'),
            "&Edit",
            self,
            shortcut="Ctrl+e",
            statusTip=u"Edit",
            triggered=self.edit
        )

        self.buildHtmlAct = QtGui.QAction(
            QtGui.QIcon('images/make.png'),
            "&Build Html",
            self,
            shortcut="Ctrl+b",
            statusTip=u"Build Html",
            triggered=self.build_html
        )

        self.cleanHtmlAct = QtGui.QAction(
            QtGui.QIcon('images/clean.png'),
            "&Clean Html",
            self,
            shortcut="Ctrl+c",
            statusTip=u"Clean Html",
            triggered=self.clean_html
        )

    def init_menu(self):
        self.fileMenu = self.menuBar().addMenu("&Project")
        self.fileMenu.addAction(self.openPrjAct)
        self.fileMenu.addAction(self.buildHtmlAct)
        self.fileMenu.addAction(self.cleanHtmlAct)
        self.menuBar().addSeparator()
        self.fileMenu.addAction(self.editAct)
        self.menuBar().addSeparator()
        self.fileMenu.addAction(self.quitAct)

    def init_toolbar(self):
        self.prjToolBar = self.addToolBar("prj")
        self.prjToolBar.addAction(self.openPrjAct)
        self.prjToolBar.addAction(self.buildHtmlAct)
        self.prjToolBar.addAction(self.cleanHtmlAct)
        self.prjToolBar.addAction(self.editAct)

        self.proToolBar = self.addToolBar("pro")
        self.proToolBar.addAction(self.quitAct)

    def init_statusbar(self):
        self.statusBar().showMessage("Ready")

    def edit(self):
        os.chdir(self.prj_path)
        proc = subprocess.Popen(
            ["gvim", self.filename],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        print "edit1"
        proc.wait()
        print "edit2"
        self.build_html()

    def clean_html(self):
        os.chdir(self.prj_path)
        proc = subprocess.Popen(
            ["make", "clean"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        proc.wait()

    def build_html(self):
        os.chdir(self.prj_path)
        proc = subprocess.Popen(
            ["make", "html"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        print "bt1"
        proc.wait()
        print "bt2"
        print self.htmlname
        self.htmlview.load_html(self.htmlname)

    def open_prj(self, prj_path=None):

        # for test
        prj_path = '/home/dormouse/project/blog'

        if not prj_path:
            dlg = OpenDlg()
            prj_path = dlg.getExistingDirectory(self)

        if prj_path:
            confname = os.path.join(prj_path, DEFAULT_CONF)
            if os.path.exists(confname):
                try:
                    sys.path.insert(0, prj_path)
                    import conf
                except Exception, e:
                    print e
                    return

                self.setWindowTitle(PRJ_NAME + u' -- ' + conf.project)
                self.prj_path = prj_path
                self.build_path = os.path.join(prj_path, u'_build/html')
                self.handle_file_changed()
            else:
                reply = QtGui.QMessageBox.information(
                    self,
                    u"Warning!",
                    u"Can not find conf.py!"
                )
                if reply == QtGui.QMessageBox.Ok:
                    return
                else:
                    return

    def handle_file_changed(self, filename=None):
        if not filename:
            filename = os.path.join(self.prj_path, DEFAULT_INDEX)
        htmlname = filename.replace(self.prj_path, self.build_path)
        htmlname = htmlname.replace('.rst', '.html')
        self.treeview.load_dir(self.prj_path)
        self.htmlview.load_html(htmlname)
        self.filename = filename
        self.htmlname = htmlname

    def quit(self):
        self.close()
