#!/bin/env python3
# -*- coding: utf8 -*-

import os
import sys
import markups

from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QSettings, QSignalMapper,
        QSize, QTextStream, QUrl, Qt, QCoreApplication)
from PyQt5.QtWidgets import (QMainWindow, QApplication, QTextEdit,
                             QSplitter, QTreeView, QAction, QFileDialog,
                             QMessageBox, QErrorMessage, QFileSystemModel
                             )
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon, QKeySequence

PRJ_NAME = u'Lake Tai'
DEFAULT_INDEX = u'index.rst'
DEFAULT_CONF = u'conf.py'

class Editor(QTextEdit):
    def __init__(self, topwin):
        super(Editor, self).__init__()
        self.topwin = topwin
        self.textChanged.connect(self.on_text_changed)
        self.markup = markups.ReStructuredTextMarkup()

    def open_file(self, path=None):
        with open(path, 'r') as f:
            text = f.read()
            self.setText(text)


    def on_text_changed(self):
        self.update_html()
        self.setFocus()

    def update_html(self):
        txt = self.toPlainText()
        print (txt)
        ## test
        aa = markups.ReStructuredTextMarkup()
        try:
            html = self.markup.convert(txt).get_document_body()
            self.topwin.htmlview.setHtml(html)
            self.topwin.show_error_msg("mark up parse ok!")
        except:
            # todo
            # 显示更详细的出错信息
            self.topwin.show_error_msg("mark up parse error!")


class HtmlView(QWebEngineView):
    def __init__(self, parent=None):
        super(HtmlView, self).__init__(parent)

    def load_html(self, path):
        self.load(QUrl.fromLocalFile(path))


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
            main_win.handle_file_changed(new_filename)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.prj_path = None

        self.splitter = QSplitter(Qt.Horizontal)
        self.treeview = TreeView()
        self.htmlview = HtmlView(self)
        self.editor = Editor(self)
        self.setCentralWidget(self.splitter)
        self.splitter.addWidget(self.treeview)
        self.splitter.addWidget(self.editor)
        self.splitter.addWidget(self.htmlview)

        self.setWindowTitle(PRJ_NAME)
        self.init_act()
        self.init_menu()
        self.init_toolbar()
        self.init_statusbar()
        self.read_settings()
        self.show()

    def init_act(self):
        self.act_open_prj = QAction(
            QIcon("images/open.png"), "&Open Project", self,
            shortcut="Ctrl+O",
            statusTip="Open Project",
            triggered=self.open_prj
        )
        self.act_quit = QAction(
            QIcon('images/quit.png'), "&Close", self,
            shortcut=QKeySequence.Close,
            statusTip=u"Quit",
            triggered=self.quit
        )

    def init_menu(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.act_open_prj)
        self.menuBar().addSeparator()
        self.fileMenu.addAction(self.act_quit)

    def init_toolbar(self):
        self.file_toolbar = self.addToolBar("file")
        self.file_toolbar.addAction(self.act_open_prj)
        self.file_toolbar.addAction(self.act_quit)

    def init_statusbar(self):
        self.statusBar().showMessage("Ready")

    def show_error_msg(self, msg):
        self.statusBar().showMessage(msg)

    def read_settings(self):
        settings = QSettings("Dormouse", "LakeTai")
        # main window
        self.move(settings.value("mainwin/pos", QPoint(200, 200)))
        self.resize(settings.value("mainwin/size", QSize(400, 400)))
        # splitter
        self.splitter.setSizes(settings.value("splitter/sizes", [300,500,500]))
        self.splitter.setStretchFactor(0,50)
        self.splitter.setStretchFactor(1,50)

    def write_settings(self):
        settings = QSettings("Dormouse", "LakeTai")
        # main window
        settings.setValue("mainwin/pos", self.pos())
        settings.setValue("mainwin/size", self.size())
        # splitter
        settings.setValue("splitter/sizes", self.splitter.sizes())

    def open_file(self):
        pre_file_path = '~'
        fname = QFileDialog.getOpenFileName(self, 'Open file', pre_file_path)
        if fname[0]:
            self.editor.open_file(fname[0])

    def open_prj(self, prj_path=None):
        default_path = '/Users/dormouse/test'
        if not prj_path:
            options = QFileDialog.Options()
            options |= QFileDialog.ShowDirsOnly
            prj_path= QFileDialog.getExistingDirectory(self,
                                                       "QFileDialog.getOpenFileNames()",
                                                       default_path,
                                                       options=options)
        if prj_path:
            full_conf_filename = os.path.join(prj_path, DEFAULT_CONF)
            if os.path.exists(full_conf_filename):
                try:
                    sys.path.insert(0, prj_path)
                    # import conf
                except Exception as e:
                    pass
                    # QErrorMessage().showMessage(e)


                # self.setWindowTitle(PRJ_NAME + u' -- ' + conf.project)
                self.prj_path = prj_path
                self.handle_file_changed()
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

    def handle_file_changed(self, filename=None):
        if not filename:
            filename = DEFAULT_INDEX
        full_filename = os.path.join(self.prj_path, filename)
        html_filename = u'_build/html/%s.html' %\
            os.path.splitext(filename)[0]
        full_html_filename = os.path.join(self.prj_path, html_filename)

        self.treeview.load_dir(self.prj_path)
        self.editor.open_file(full_filename)
        # self.htmlview.load_html(full_html_filename)

    def quit(self):
        self.close()


    def closeEvent(self, event):
        reply = QMessageBox.question(self,
                                     'Message',
                                     'Are you sure to quit?',
                                     QMessageBox.Yes,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.write_settings()
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
