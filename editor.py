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

