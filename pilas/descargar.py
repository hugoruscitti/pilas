# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar
#
# Creditos: http://stackoverflow.com/questions/6852038/threading-in-pyqt4

from PyQt4.QtCore import QUrl, QFile, QIODevice
from PyQt4.QtGui import QDialog, QProgressBar
from PyQt4.QtGui import QLabel, QPushButton, QDialogButtonBox, QVBoxLayout, QMessageBox
from PyQt4.QtNetwork import QHttp
import os


class Descargar(QDialog):

    def __init__(self, parent, url, archivo_destino):
        super(Descargar, self).__init__(parent)

        self.url = url
        self.httpGetId = 0
        self.httpRequestAborted = False
        self.statusLabel = QLabel('Descargando el manual completo ...')
        self.closeButton = QPushButton("Cerrar")
        self.closeButton.setAutoDefault(False)
        self.barra = QProgressBar()

        buttonBox = QDialogButtonBox()
        buttonBox.addButton(self.closeButton, QDialogButtonBox.RejectRole)

        self.http = QHttp(self)
        self.http.requestFinished.connect(self.cuando_finalizar_request)
        self.http.dataReadProgress.connect(self.cuando_actualiza_descarga)
        self.http.responseHeaderReceived.connect(self.cuando_responder_header)
        self.closeButton.clicked.connect(self.cuando_cancela)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.statusLabel)
        mainLayout.addWidget(self.barra)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle('Descargando manual')
        self.downloadFile(url, archivo_destino)

    def downloadFile(self, url, archivo_destino):
        url = QUrl(url)
        fileName = archivo_destino
        directorio_usuario_para_pilas = os.path.dirname(archivo_destino)

        if not os.path.exists(directorio_usuario_para_pilas):
            os.mkdir(directorio_usuario_para_pilas)

        if QFile.exists(fileName):
            QFile.remove(fileName)

        self.outFile = QFile(fileName)

        if not self.outFile.open(QIODevice.WriteOnly):
            QMessageBox.information(self, 'Error', 'Lo siento, no se puede descargar el archivo desde %s: %s.' % (self.url, self.outFile.errorString()))
            self.outFile = None
            return

        mode = QHttp.ConnectionModeHttp
        port = url.port()
        if port == -1:
            port = 0
        self.http.setHost(url.host(), mode, port)
        self.httpRequestAborted = False

        path = QUrl.toPercentEncoding(url.path(), "!$&'()*+,;=:@/")
        if path:
            path = str(path)
        else:
            path = '/'

        self.httpGetId = self.http.get(path, self.outFile)

    def cuando_cancela(self):
        self.statusLabel.setText("Descarga cancelada")
        self.httpRequestAborted = True
        self.http.abort()
        self.close()

    def cuando_finalizar_request(self, request_id, error):
        if request_id != self.httpGetId:
            return

        if self.httpRequestAborted:
            if self.outFile is not None:
                self.outFile.close()
                self.outFile.remove()
                self.outFile = None
            return

        self.outFile.close()

        if error:
            self.outFile.remove()
            QMessageBox.information(self, 'Error', u'Hay un error de conexión: %s.' % self.http.errorString())

        self.statusLabel.setText(u'Perfecto, ahora podrás explorar el manual.')

    def cuando_responder_header(self, responseHeader):
        if responseHeader.statusCode() not in (200, 300, 301, 302, 303, 307):
            mensaje = 'Ha fallado la descarga del archivo: \n"%s" \n%s.' %(self.url, responseHeader.reasonPhrase())
            QMessageBox.information(self, 'Error', mensaje)

            self.httpRequestAborted = True
            self.http.abort()
            self.close()

    def cuando_actualiza_descarga(self, bytes_leidos, total_bytes):
        if self.httpRequestAborted:
            return

        self.barra.setMaximum(total_bytes)
        self.barra.setValue(bytes_leidos)
