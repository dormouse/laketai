from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from docutils.core import publish_parts

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


TEXT = """
Here is a quick and dirty cheat sheet for some common stuff you want
to do in sphinx and ReST.

.. _formatting-text:

文本格式化
===============

=====  ====================     ============
名称   代码                     示例
=====  ====================     ============
斜体   ``*斜体*``               *斜体*
粗休   ``**粗体**``             **粗体**
原文   \`\`**原文**\`\`         ``**原文**``
=====  ====================     ============

源代码
======

末尾使用 ``::`` 符号，则下面的内容就显示为源代码,源代码需要缩进，例如::

    You can represent code blocks fairly easily::

       import numpy as np
       x = np.random.rand(12)

以上代码显示效果如下：

You can represent code blocks fairly easily

.. code-block:: python

   import numpy as np
   x = np.random.rand(12)


"""

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        testFile = 'sphinx_cheet_sheet.rst'
        # text = TEXT
        with open(testFile,'r') as f:
            text = f.read()
        formatter = HtmlFormatter()
        # html = highlight(text, PythonLexer(), formatter)
        extra_settings = {'initial_header_level': 4,
                          'doctitle_xform': 0,
                          'syntax_highlight': 'short',
                          'stylesheet - path': 'html4css1.css',
                          'embed-stylesheet': 'no'
                          }
        # html = publish_parts(text, writer_name='html',settings_overrides=extra_settings)['html_body']
        html = publish_parts(text, writer_name='html',settings_overrides=extra_settings)['whole']
        print(html)

        self.htmlview = QWebEngineView()
        self.htmlview.setHtml(html)
        self.setCentralWidget(self.htmlview)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
