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

window = QX11EmbedWidget()
window.embedInto(int(sys.argv[1]))

pilas_widget = aplicacion.Window(parent=window)

window.show()

sys.exit(app.exec_())
