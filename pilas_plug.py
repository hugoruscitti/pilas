"""

This command provides a plug to embed Qt.

The X11 window ID is passed as the unique parameter.

"""

import os
import sys

base = os.environ['SUGAR_BUNDLE_PATH']

qtpath = os.path.join(base, 'qt')
sys.path.append(qtpath)

# del sys.path[sys.path.index('/usr/lib/python2.7/site-packages')]

from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QString
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QX11EmbedWidget

import pilas
from pilas import aplicacion

app = QApplication(sys.argv)

parent_window_id = int(sys.argv[1])
screen_width = int(sys.argv[2])
screen_height = int(sys.argv[3])

window = QX11EmbedWidget()
window.embedInto(parent_window_id)
window.show()

hbox = QHBoxLayout(window)
pilas_height = 2.0 / 3 * screen_height
pilas_widget = aplicacion.Window(parent=window, pilas_height=pilas_height)
hbox.addWidget(pilas_widget)

sys.exit(app.exec_())
