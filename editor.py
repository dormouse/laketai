#!/bin/env python
# -*- coding: utf8 -*-

# These are only needed for Python v2 but are harmless for Python v3.
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
from PyQt4 import QtGui, QtCore


class Editor(QtGui.QTextEdit):
    def __init__(self, parent=None):
        super(Editor, self).__init__(parent)

    def openFile(self, path=None):
        with open(path) as f:
            text = f.read()
            self.setText(text)

    def open_File(self, path=None):
        inFile = QtCore.QFile(path)
        if inFile.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            text = inFile.readAll()

            try:
                # Python v3.
                text = str(text, encoding='ascii')
            except TypeError:
                # Python v2.
                # text = str(text)
                pass

            self.setPlainText(text)
