#!/bin/env python3
# -*- coding: utf8 -*-

import sys
import markups

from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QSettings, QSignalMapper,
        QSize, QTextStream, QUrl, Qt, QCoreApplication)
QCoreApplication.
from PyQt5.QtWidgets import (QMainWindow, QApplication, QTextEdit,
                             QSplitter, QTreeView, QAction, QFileDialog
                             )
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon, QKeySequence

PRJ_NAME = 'markdown editor'

class Editor(QTextEdit):
    def __init__(self, topwin):
        super(Editor, self).__init__()
        self.topwin = topwin
        self.textChanged.connect(self.on_text_changed)
        self.markup = markups.ReStructuredTextMarkup()
        self.open_file_test()

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
        # todo
        # 出错处理
        try:
            html = self.markup.convert(txt).get_document_body()
            self.topwin.htmlview.setHtml(html)
            self.topwin.show_error_msg("mark up parse ok!")
        except:
            self.topwin.show_error_msg("mark up parse error!")

    def open_file_test(self):
        test_rst = """
12
===========

123

456

first section
-------------

112
"""
        self.setPlainText(test_rst)


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

        model = QtGui.QFileSystemModel()
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

        splitter = QSplitter(Qt.Horizontal)
        # self.treeview = TreeView()
        self.htmlview = HtmlView(self)
        self.editor = Editor(self)
        self.setCentralWidget(splitter)
        # splitter.addWidget(self.treeview)
        splitter.addWidget(self.editor)
        splitter.addWidget(self.htmlview)

        self.setWindowTitle(PRJ_NAME)
        self.init_act()
        self.init_menu()
        self.init_toolbar()
        self.init_statusbar()
        self.read_settings()
        self.show()

    def init_act(self):
        """
        self.openPrjAct = QAction(
            QIcon("images/open.png"),
            "&Open Project",
            self,
            shortcut="Ctrl+O",
            statusTip="Open Project",
            triggered=self.open_prj
        )
        """
        self.act_open_file = QAction(
            QIcon("images/open.png"),
            "&Open File",
            self,
            shortcut="Ctrl+O",
            statusTip="Open File",
            triggered=self.open_file
        )


        self.act_quit = QAction(
            QIcon('images/quit.png'),
            "&Close",
            self,
            shortcut=QKeySequence.Close,
            statusTip=u"Quit",
            triggered=self.quit
        )

    def init_menu(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.act_open_file)
        self.menuBar().addSeparator()
        self.fileMenu.addAction(self.act_quit)

    def init_toolbar(self):
        self.file_toolbar = self.addToolBar("file")
        self.file_toolbar.addAction(self.act_open_file)
        self.file_toolbar.addAction(self.act_quit)

    def init_statusbar(self):
        self.statusBar().showMessage("Ready")

    def show_error_msg(self, msg):
        self.statusBar().showMessage(msg)

    def read_settings(self):
        settings = QSettings("Dormouse", "LakeTai")
        print ("hh:", settings.fileName())

        pos = settings.value("pos", QPoint(200, 200))
        size = settings.value("size", QSize(400, 400))
        self.resize(size)
        self.move(pos)

    def write_settings(self):
        settings = QSettings("Dormouse", "LakeTai")
        settings.setValue("pos", self.pos())
        settings.setValue("size", self.size())

    def open_file(self):
        pre_file_path = '~'
        fname = QFileDialog.getOpenFileName(self, 'Open file', pre_file_path)
        if fname[0]:
            self.editor.open_file(fname[0])

    def open_prj(self, prj_path=None):
        if not prj_path:
            dlg = OpenDlg()
            prj_path = dlg.getExistingDirectory(self)

        if prj_path:
            full_conf_filename = os.path.join(prj_path, DEFAULT_CONF)
            if os.path.exists(full_conf_filename):
                try:
                    sys.path.insert(0, prj_path)
                    import conf
                except Exception as e:
                    QtGui.QErrorMessage().showMessage(e)
                    return

                self.setWindowTitle(PRJ_NAME + u' -- ' + conf.project)
                self.prj_path = prj_path
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
            filename = DEFAULT_INDEX
        full_filename = os.path.join(self.prj_path, filename)
        html_filename = u'_build/html/%s.html' %\
            os.path.splitext(filename)[0]
        full_html_filename = os.path.join(self.prj_path, html_filename)

        self.treeview.load_dir(self.prj_path)
        self.editor.openFile(full_filename)
        self.htmlview.load_html(full_html_filename)

    def quit(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
