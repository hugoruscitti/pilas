# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
import codecs
import re
import sys

from PyQt4.Qt import (QFrame, QWidget, QPainter, QSize)
from PyQt4.QtGui import (QTextEdit, QTextCursor, QFileDialog,
                         QIcon, QMessageBox, QShortcut,
                         QKeySequence)
from PyQt4.QtCore import Qt
from PyQt4 import QtCore

from editorbase import editor_base
import editor_ui
import pilasengine

CONTENIDO = u"""import pilasengine

pilas = pilasengine.iniciar()

mono = pilas.actores.Mono()

# Algunas transformaciones:
# (Pulsá el botón derecho del
#  mouse sobre alguna de las
#  sentencias)

mono.x = 0
mono.y = 0
mono.escala = 1.0
mono.rotacion = 0

pilas.ejecutar()"""


class WidgetEditor(QWidget, editor_ui.Ui_Editor):

    class NumberBar(QWidget):

        def __init__(self, *args):
            QWidget.__init__(self, *args)
            self.edit = None
            # This is used to update the width of the control.
            # It is the highest line that is currently visible.
            self.highest_line = 0

        def setTextEdit(self, edit):
            self.edit = edit

        def update(self, *args):
            '''
            Updates the number bar to display the current set of numbers.
            Also, adjusts the width of the number bar if necessary.
            '''
            # The + 4 is used to compensate for the current line being bold.
            width = self.fontMetrics().width(str(self.highest_line)) + 4

            if self.width() != width:
                self.setFixedWidth(width + 15)

            QWidget.update(self, *args)

        def paintEvent(self, event):
            contents_y = self.edit.verticalScrollBar().value()
            page_bottom = contents_y + self.edit.viewport().height()
            font_metrics = self.fontMetrics()

            painter = QPainter(self)

            line_count = 0

            # Iterate over all text blocks in the document.
            block = self.edit.document().begin()

            while block.isValid():
                line_count += 1

                # The top left position of the block in the document
                position = self.edit.document().documentLayout().blockBoundingRect(block).topLeft()

                # Check if the position of the block is out side of the visible
                # area.
                if position.y() > page_bottom:
                    break

                # Draw the line number right justified at the y position of the
                # line. 3 is a magic padding number. drawText(x, y, text).
                painter.drawText(-5 + self.width() - font_metrics.width(str(line_count)) - 3,
                                round(position.y()) - contents_y + font_metrics.ascent(),
                                str(line_count))

                block = block.next()

            self.highest_line = line_count
            painter.end()

            QWidget.paintEvent(self, event)

    def __init__(self, main=None, interpreter_locals=None, *args):
        QWidget.__init__(self, *args)
        self.setupUi(self)
        self.setLayout(self.vertical_layout)

        if interpreter_locals is None:
            interpreter_locals = locals()

        self.editor = Editor(self, interpreter_locals)
        self.editor.setFrameStyle(QFrame.NoFrame)
        self.editor.setAcceptRichText(False)

        self.number_bar = self.NumberBar()
        self.number_bar.setTextEdit(self.editor)

        # Agregando editor y number_bar a hbox_editor layout
        self.hbox_editor.addWidget(self.number_bar)
        self.hbox_editor.addWidget(self.editor)

        # Boton Abrir
        self.set_icon(self.boton_abrir, 'iconos/abrir.png')
        self.boton_abrir.connect(self.boton_abrir,
                                    QtCore.SIGNAL('clicked()'),
                                    self.editor.abrir_archivo_con_dialogo)

        # Boton Guardar
        self.set_icon(self.boton_guardar, 'iconos/guardar.png')
        self.boton_guardar.connect(self.boton_guardar,
                                    QtCore.SIGNAL('clicked()'),
                                    self.editor.guardar_contenido_con_dialogo)

        # Boton Ejecutar
        self.set_icon(self.boton_ejecutar, 'iconos/ejecutar.png')
        self.boton_ejecutar.connect(self.boton_ejecutar,
                                    QtCore.SIGNAL('clicked()'),
                                    self.cuando_pulsa_el_boton_ejecutar)

        # Boton Pausar
        self.set_icon(self.boton_pausar, 'iconos/pausa.png')
        self.boton_pausar.connect(self.boton_pausar,
                                    QtCore.SIGNAL('clicked()'),
                                    self.cuando_pulsa_el_boton_pausar)

        # Boton Siguiente
        self.set_icon(self.boton_siguiente, 'iconos/siguiente.png')
        self.boton_siguiente.connect(self.boton_siguiente,
                                    QtCore.SIGNAL('clicked()'),
                                    self.cuando_pulsa_el_boton_siguiente)

        self._vincular_atajos_de_teclado()

        self.editor.installEventFilter(self)
        self.editor.viewport().installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj in (self.editor, self.editor.viewport()):
            self.number_bar.update()
            return False
        return QWidget.eventFilter(obj, event)

    def set_icon(self, boton, ruta):
        icon = QIcon()
        archivo = pilasengine.utils.obtener_ruta_al_recurso(ruta)
        icon.addFile(archivo, QSize(), QIcon.Normal, QIcon.Off)
        boton.setIcon(icon)
        boton.setText('')

    def _vincular_atajos_de_teclado(self):
        QShortcut(QKeySequence("F5"), self,
                  self.cuando_pulsa_el_boton_ejecutar)
        QShortcut(QKeySequence("Ctrl+r"), self,
                  self.cuando_pulsa_el_boton_ejecutar)

        # Solo en MacOS informa que la tecla Command sustituye a CTRL.
        if sys.platform == 'darwin':
            self.boton_ejecutar.setToolTip(u"Ejecutar el código actual (F5 o ⌘R)")

    def cuando_pulsa_el_boton_ejecutar(self):
        self.editor.ejecutar()
        self.boton_pausar.setChecked(False)

    def cuando_pulsa_el_boton_pausar(self):
        if self.boton_pausar.isChecked():
            self.editor.interpreterLocals['pilas'].widget.pausar()
        else:
            self.editor.interpreterLocals['pilas'].widget.continuar()

    def cuando_pulsa_el_boton_siguiente(self):
        if not self.boton_pausar.isChecked():
            self.boton_pausar.click()

        self.editor.interpreterLocals['pilas'].widget.avanzar_un_solo_cuadro()


class Editor(editor_base.EditorBase):
    """Representa el editor de texto que aparece en el panel derecho.

    El editor soporta autocompletado de código y resaltado de sintáxis.
    """

    # Señal es emitida cuando el Editor ejecuta codigo
    signal_ejecutando = QtCore.pyqtSignal()

    def __init__(self, main, interpreterLocals):
        super(Editor, self).__init__()
        self.interpreterLocals = interpreterLocals
        self.insertPlainText(CONTENIDO)
        self.setLineWrapMode(QTextEdit.NoWrap)
        self._cambios_sin_guardar = False
        self.main = main

    def keyPressEvent(self, event):
        "Atiene el evento de pulsación de tecla."
        self._cambios_sin_guardar = True

        if editor_base.EditorBase.keyPressEvent(self, event):
            return None

        # Elimina los pares de caracteres especiales si los encuentra
        if event.key() == Qt.Key_Backspace:
            self._eliminar_pares_de_caracteres(es_consola=False)

        if event.key() == Qt.Key_Tab:
            tc = self.textCursor()
            tc.insertText("    ")
        else:
            if self.autocomplete(event):
                return None

            return QTextEdit.keyPressEvent(self, event)

    def tiene_cambios_sin_guardar(self):
        return self._cambios_sin_guardar

    def _get_current_line(self):
        "Obtiene la linea en donde se encuentra el cursor."
        tc = self.textCursor()
        tc.select(QTextCursor.LineUnderCursor)
        return tc.selectedText()

    def _get_position_in_block(self):
        tc = self.textCursor()
        position = tc.positionInBlock() - 1
        return position

    def cargar_contenido_desde_archivo(self, ruta):
        "Carga todo el contenido del archivo indicado por ruta."
        with codecs.open(unicode(ruta), 'r', 'utf-8') as archivo:
            contenido = archivo.read()
        self.setText(contenido)

        self.nombre_de_archivo_sugerido = ruta
        self._cambios_sin_guardar = False

    def abrir_dialogo_cargar_archivo(self):
        return QFileDialog.getOpenFileName(self, "Abrir Archivo",
                                   self.nombre_de_archivo_sugerido,
                                   "Archivos python (*.py)",
                                   options=QFileDialog.DontUseNativeDialog)

    def abrir_archivo_con_dialogo(self):
        self.quiere_perder_cambios()

        ruta = self.abrir_dialogo_cargar_archivo()

        if ruta:
            self.cargar_contenido_desde_archivo(ruta)
            self.ejecutar()

    def quiere_perder_cambios(self):
        if self.tiene_cambios_sin_guardar():
            if self.mensaje_quiere_guardar_cambios():
                self.guardar_contenido_con_dialogo()

    def mensaje_quiere_guardar_cambios(self):
        """Realizar una consulta usando un cuadro de dialogo simple.
        Este método retorna True si el usuario presiona el boton 'Guardar'."""

        titulo = u"Se perderán los cambios sin guardar"
        mensaje = u"¿Deseas guardar los cambios?"

        # False si respuesta es "Guardar", True si la respuesta es "No"
        respuesta = QMessageBox.question(self, titulo, mensaje,
                                         "Guardar", "No")

        return (respuesta == False)

    def guardar_contenido_con_dialogo(self):
        ruta = self.abrir_dialogo_guardar_archivo()

        if ruta:
            self.guardar_contenido_en_el_archivo(ruta)
            self._cambios_sin_guardar = False
            self.nombre_de_archivo_sugerido = ruta
            self.mensaje_contenido_guardado()

    def obtener_contenido(self):
        return unicode(self.document().toPlainText())

    def ejecutar(self, ruta_personalizada=None):
        #print "ejecutando texto desde widget editor"
        texto = self.obtener_contenido()
        #texto = self.editor.obtener_texto_sanitizado(self)
        # elimina cabecera de encoding.
        contenido = re.sub('coding\s*:\s*', '', texto)
        contenido = contenido.replace('import pilasengine', '')
        contenido = contenido.replace('pilas = pilasengine.iniciar', 'pilas.reiniciar')

        # Muchos códigos personalizados necesitan cargar imágenes o sonidos
        # desde el directorio que contiene al archivo. Para hacer esto posible,
        # se llama a la función "pilas.utils.agregar_ruta_personalizada" con el
        # path al directorio que representa el script. Así la función "obtener_ruta_al_recurso"
        # puede evaluar al directorio del script en busca de recursos también.
        if ruta_personalizada:
            agregar_ruta_personalizada = 'pilas.utils.agregar_ruta_personalizada("%s")' %(ruta_personalizada)
            contenido = contenido.replace('pilas.reiniciar(', agregar_ruta_personalizada+'\n'+'pilas.reiniciar(')

        exec(contenido, self.interpreterLocals)
        self.signal_ejecutando.emit()
