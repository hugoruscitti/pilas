# -*- coding: utf-8 -*-
import codecs
import pilasengine

from PyQt4.QtCore import Qt
from PyQt4.QtGui import (QTextEdit, QTextCursor, QFileDialog,
                         QMessageBox)

import autocomplete
import editor_con_deslizador
import highlighter


class EditorBase(autocomplete.CompletionTextEdit,
                 editor_con_deslizador.EditorConDeslizador):
    """Editor de texto basado en QTextEdit con autocompletador y un deslizador
    para modificar variables asociadas a objetos enteros o flotantes"""

    def __init__(self):
        autocomplete.CompletionTextEdit.__init__(self, None)
        self._cargar_resaltador_de_sintaxis()
        self.nombre_de_archivo_sugerido = "juego.py"
        self.configuracion = pilasengine.configuracion.Configuracion()

    def insertFromMimeData(self, source):
        self.insertPlainText(source.text())

    def actualizar_scope(self, scope):
        self.interpreterLocals = scope

    def keyPressEvent(self, event):
        if self.configuracion.atajos_de_teclado_habilitado():
            if event.modifiers() & Qt.AltModifier:
                if event.key() == Qt.Key_Minus:
                    self.cambiar_tamano_fuente(-1)
                    return True
                elif event.key() == Qt.Key_Plus:
                    self.cambiar_tamano_fuente(1)
                    return True

        if event.key() == Qt.Key_Tab:
            tc = self.textCursor()
            tc.insertText("    ")
            return True

    def wheelEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            self.cambiar_tamano_fuente(event.delta())
            return

        return QTextEdit.wheelEvent(self, event)

    def _get_current_line(self):
        raise NotImplementedError('Es necesario sobreescribir \
                                  el metodo _get_current_line')

    def _get_current_word(self):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def _get_position_in_block(self):
        raise NotImplementedError('Es necesario sobreescribir el metodo \
                                    _get_position_in_block')

    def cambiar_tamano_fuente(self, delta):
        if delta < 0:
            self.zoomOut(1)
        elif delta > 0:
            self.zoomIn(1)
        self.ensureCursorVisible()

    def definir_fuente(self, fuente):
        self.setFont(fuente)
        self.font_family = fuente.rawName()
        self.font_size = fuente.pointSize()

    def abrir_dialogo_guardar_archivo(self):
        return QFileDialog.getSaveFileName(self, "Guardar Archivo",
                                           self.nombre_de_archivo_sugerido,
                                           "Archivos python (*.py)",
                                           options=QFileDialog.DontUseNativeDialog)

    def guardar_contenido_con_dialogo(self):
        raise NotImplementedError('Es necesario sobreescribir el metodo \
                                    guardar_contenido_con_dialogo')

    def obtener_contenido(self):
        """Retorna el contenido del editor segun las condiciones indicadas"""
        raise NotImplementedError('Es necesario sobreescribir el metodo \
                                    obtener_contenido')

    def guardar_contenido_en_el_archivo(self, ruta):
        texto = self.obtener_contenido()
        with codecs.open(unicode(ruta), 'w', 'utf-8') as archivo:
            archivo.write(texto)

    def mensaje_contenido_guardado(self):
        QMessageBox.information(self, 'Contenido guardado',
                               'Se ha guardado el archivo',
                               'De acuerdo')

    def _cargar_resaltador_de_sintaxis(self):
        self._highlighter = highlighter.Highlighter(
            self.document(),
            'python',
            highlighter.COLOR_SCHEME)
