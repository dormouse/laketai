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

    def load_html(self, path):
        self.load(QtCore.QUrl.fromLocalFile(path))


class TreeView(QtGui.QTreeView):
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
            new_filename = self.model().filePath(indexes[0])
            main_win = self.parent().parent()
            main_win.handle_file_changed(new_filename)
