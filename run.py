#!/bin/env python3
# -*- coding: utf8 -*-

import os
import sys
import logging

import markups
from PyQt5.QtCore import (Qt, QPoint, QSettings, QSize, QUrl)
from PyQt5.QtGui import (QIcon, QKeySequence)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (QAction, QApplication, QDockWidget,
                             QFileDialog, QFileSystemModel,
                             QMainWindow, QMessageBox,
                             QTextEdit, QTreeView)
from docutils.core import publish_parts

PRJ_NAME = u'Lake Tai'
DEFAULT_INDEX = u'index.rst'
DEFAULT_CONF = u'conf.py'

class TextEdit(QTextEdit):
    def __init__(self, parent = None):
        super(TextEdit, self).__init__(parent)
        self.textChanged.connect(self.onTextChanged)
        self.markup = markups.ReStructuredTextMarkup()

    def openFile(self, path=None):
        with open(path, 'r') as f:
            text = f.read()
            self.setText(text)


    def onTextChanged(self):
        self.updateHtml()
        self.setFocus()

    def updateHtml(self):
        text = self.toPlainText()
        extra_settings = {'initial_header_level': 4,
                          'doctitle_xform': 0,
                          'syntax_highlight': 'short',
                          'stylesheet - path': 'html4css1.css',
                          'embed-stylesheet': 'no'
                          }
        try:
            html = publish_parts(text, writer_name='html', settings_overrides=extra_settings)['whole']
            self.parent().logger.debug(html)

            self.parent().previewView.setHtml(html)
            self.parent().showErrorMsg("mark up parse ok!")
        except:
            # todo
            # 显示更详细的出错信息
            self.parent().showErrorMsg("mark up parse error!")


class HtmlView(QWebEngineView):
    def __init__(self, parent=None):
        super(HtmlView, self).__init__(parent)


class TreeView(QTreeView):
    def __init__(self, parent=None):
        super(TreeView, self).__init__(parent)
        self.dir_path = None
        self.setMaximumWidth(180)

    def load_dir(self, dir_path):
        if dir_path == self.dir_path:
            return

        self.dir_path = dir_path

        model = QFileSystemModel()
        model.setRootPath(dir_path)
        self.setModel(model)

        index_root = model.index(model.rootPath())
        self.setRootIndex(index_root)

        # hide unwanted info
        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)
        self.setHeaderHidden(True)

    def selectionChanged(self, selected, deselected):
        super(TreeView, self).selectionChanged(selected, deselected)
        indexes = selected.indexes()
        if indexes:
            new_filename = self.model().data(indexes[0])
            main_win = self.parent().parent()
            main_win.handleFileChanged(new_filename)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.logger = logging.getLogger(__name__)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        self.readSettings()
        self.textEdit = TextEdit(self)
        self.setCentralWidget(self.textEdit)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.createDockWindows()

        self.setWindowTitle("Lake Tai")

    def createActions(self):
        self.openProjectAction = QAction(
            QIcon("images/open.png"), "&Open Project", self,
            shortcut="Ctrl+O",
            statusTip="Open Project",
            triggered=self.openProject
        )
        self.preferencesAction = QAction(
            "Preferences...",
            self,
            menuRole = QAction.PreferencesRole
        )

        self.quitAction = QAction(
            QIcon('images/quit.png'), "&Close", self,
            shortcut=QKeySequence.Close,
            statusTip="Quit",
            triggered=self.quit,
            menuRole=QAction.QuitRole #  More like OSX native app
        )

        self.recentProjectActions = []
        settings = self.getSettingsObj()
        recentProjectsMax = settings.value("recentProjectsMax")
        for i in range(recentProjectsMax):
            self.recentProjectActions.append(QAction(self, visible=False, triggered=self.openRecentProject))

    def createToolBars(self):
        self.file_toolbar = self.addToolBar("file")
        self.file_toolbar.addAction(self.openProjectAction)
        self.file_toolbar.addAction(self.quitAction)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createMenus(self):
        # file menu
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.preferencesAction)
        self.fileMenu.addAction(self.quitAction)
        self.fileMenu.addAction(self.openProjectAction)
        # file menu -> recent projects menu
        self.recentPorjectsMenu = self.fileMenu.addMenu("recent projects")
        for action in self.recentProjectActions:
            self.recentPorjectsMenu.addAction(action)
        self.updateRecentProjectActions()

        # view menu
        self.viewMenu = self.menuBar().addMenu("&View")

    def updateRecentProjectActions(self):
        settings = self.getSettingsObj()
        projects = settings.value('recentProjects', [])
        for action in self.recentProjectActions:
            action.setVisible(False)
        for project, action in zip(projects, self.recentProjectActions):
            action.setText(project)
            action.setData(project)
            action.setVisible(True)

    def createDockWindows(self):
        # dock for project files
        dock = QDockWidget("Project", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.projectTreeView= TreeView(dock)
        dock.setWidget(self.projectTreeView)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())

        # dock for html preview
        dock = QDockWidget("Preview", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.previewView= HtmlView(dock)
        dock.setWidget(self.previewView)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())

    def getSettingsObj(self):
        settings = QSettings("Dormouse", "LakeTai")
        return settings

    def readSettings(self):
        settings = self.getSettingsObj()
        # main window
        self.move(settings.value("mainwin/pos", QPoint(200, 200)))
        self.resize(settings.value("mainwin/size", QSize(400, 400)))


    def writeSettings(self):
        settings = self.getSettingsObj()
        # main window
        settings.setValue("mainwin/pos", self.pos())
        settings.setValue("mainwin/size", self.size())

    def openRecentProject(self):
        action = self.sender()
        if action:
            self.openProject(action.data())

    def showErrorMsg(self, msg):
        self.statusBar().showMessage(msg)

    def addRecentProject(self, project):
        settings = self.getSettingsObj()
        projects = settings.value("recentProjects", [])
        projectsMax = settings.value("recentProjectsMax", 5)

        if project in projects:
            # do nothing
            return
        if len(projects) < projectsMax:
            projects.append(project)
        if len(projects) == projectsMax:
            newProjects = projects[1:]
            newProjects.append(project)
        settings.setValue("recentProjects", newProjects)
        self.updateRecentProjectActions()



    def openProject(self, prjPath=None):
        default_path = '/Users/dormouse/test'
        if not prjPath:
            options = QFileDialog.Options()
            options |= QFileDialog.ShowDirsOnly
            prjPath= QFileDialog.getExistingDirectory(
                self,
                "QFileDialog.getOpenFileNames()",
                default_path,
                options=options
            )
        if prjPath:
            full_conf_filename = os.path.join(prjPath, DEFAULT_CONF)
            if os.path.exists(full_conf_filename):
                try:
                    sys.path.insert(0, prjPath)
                    # import conf
                except Exception as e:
                    pass
                    # QErrorMessage().showMessage(e)


                # self.setWindowTitle(PRJ_NAME + u' -- ' + conf.project)
                self.prj_path = prjPath
                self.addRecentProject(prjPath)
                self.handleFileChanged()
            else:
                reply = QMessageBox.information(
                    self,
                    u"Warning!",
                    u"Can not find conf.py!"
                )
                if reply == QMessageBox.Ok:
                    return
                else:
                    return

    def handleFileChanged(self, filename=None):
        if not filename:
            filename = DEFAULT_INDEX
        full_filename = os.path.join(self.prj_path, filename)
        html_filename = u'_build/html/%s.html' %\
            os.path.splitext(filename)[0]
        full_html_filename = os.path.join(self.prj_path, html_filename)

        self.projectTreeView.load_dir(self.prj_path)
        self.textEdit.openFile(full_filename)

    def quit(self):
        self.close()


    def closeEvent(self, event):
        reply = QMessageBox.question(self,
                                     'Message',
                                     'Are you sure to quit?',
                                     QMessageBox.Yes,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.writeSettings()
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
