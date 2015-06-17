#!/bin/env python
# -*- coding: utf8 -*-

# These are only needed for Python v2 but are harmless for Python v3.
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
from PyQt4 import QtGui


class OpenDlg(QtGui.QFileDialog):
    def __init__(self, parent=None):
        super(OpenDlg, self).__init__()
        self.setFileMode(self.Directory)
        self.setOption(self.ShowDirsOnly, True)
        self.setWindowTitle("Select Project Path")
