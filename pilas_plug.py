"""

This command provides a plug to embed Qt.

The X11 window ID is passed as the unique parameter.

"""

import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QString
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QX11EmbedWidget

import pilas

app = QApplication(sys.argv)

windowId = QString(app.arguments()[1])
window = QX11EmbedWidget()
window.embedInto(int(sys.argv[1]))
window.show()

line = QLineEdit()
hbox = QHBoxLayout(window)
hbox.addWidget(line)
line.setText('sugar labs')

sys.exit(app.exec_())
