# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
import codecs

from PyQt4.Qt import QFrame
from PyQt4.Qt import QWidget
from PyQt4.Qt import QHBoxLayout
from PyQt4.Qt import QPainter
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QTextEdit
from PyQt4.QtGui import QTextCursor

from pilasengine.lanas import autocomplete
from pilasengine.lanas import editor_con_deslizador
from pilasengine.lanas import highlighter

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


class Editor(QFrame):

    class NumberBar(QWidget):

        #def __init__(self, main, interpreterLocals, ventana_interprete, *args):
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
                painter.drawText(-5 + self.width() - font_metrics.width(str(line_count)) - 3, round(position.y()) - contents_y + font_metrics.ascent(), str(line_count))

                block = block.next()

            self.highest_line = line_count
            painter.end()

            QWidget.paintEvent(self, event)


    def __init__(self, main, interpreterLocals, ventana_interprete, *args):
        QFrame.__init__(self, *args)

        self.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)

        self.editor = WidgetEditor(self, interpreterLocals, ventana_interprete)
        self.editor.setFrameStyle(QFrame.NoFrame)
        self.editor.setAcceptRichText(False)

        self.number_bar = self.NumberBar()
        self.number_bar.setTextEdit(self.editor)

        hbox = QHBoxLayout(self)
        hbox.setSpacing(0)
        hbox.setMargin(0)
        hbox.addWidget(self.number_bar)
        hbox.addWidget(self.editor)

        self.editor.installEventFilter(self)
        self.editor.viewport().installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj in (self.editor, self.editor.viewport()):
            self.number_bar.update()
            return False
        return QFrame.eventFilter(obj, event)


class WidgetEditor(autocomplete.CompletionTextEdit,
                   editor_con_deslizador.EditorConDeslizador):
    """Representa el editor de texto que aparece en el panel derecho.

    El editor soporta autocompletado de código y resaltado de sintáxis.
    """

    def __init__(self, main, interpreterLocals, ventana_interprete):
        autocomplete.CompletionTextEdit.__init__(self, None,
                                                 self.funcion_valores_autocompletado)
        self.interpreterLocals = interpreterLocals
        self.insertPlainText(CONTENIDO)
        self.setLineWrapMode(QTextEdit.NoWrap)
        self._cambios_sin_guardar = False
        self.main = main
        self.ventana_interprete = ventana_interprete
        self._cargar_resaltador_de_sintaxis()
        self.nombre_de_archivo_sugerido = "juego.py"

    def insertFromMimeData(self, source):
        QTextEdit.insertPlainText(self, source.text())

    def keyPressEvent(self, event):
        "Atiene el evento de pulsación de tecla."
        self._cambios_sin_guardar = True

        # Completar comillas y braces
        if event.key() == Qt.Key_QuoteDbl:
            self._autocompletar_comillas('"')

        if event.key() == Qt.Key_Apostrophe:
            self._autocompletar_comillas("'")

        if event.key() == Qt.Key_ParenLeft:
            self._autocompletar_braces('(')

        if event.key() == Qt.Key_BraceLeft:
            self._autocompletar_braces('{')

        if event.key() == Qt.Key_BracketLeft:
            self._autocompletar_braces('[')

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

    def definir_fuente(self, fuente):
        self.setFont(fuente)

    def actualizar_scope(self, scope):
        self.interpreterLocals = scope

    def funcion_valores_autocompletado(self, texto):
        "Retorna una lista de valores propuestos para autocompletar"
        scope = self.interpreterLocals
        texto = texto.replace('(', ' ').split(' ')[-1]

        if '.' in texto:
            palabras = texto.split('.')
            ultima = palabras.pop()
            prefijo = '.'.join(palabras)

            try:
                elementos = eval("dir(%s)" %prefijo, scope)
            except:
                # TODO: notificar este error de autocompletado en algun lado...
                return []

            return [a for a in elementos if a.startswith(ultima)]
        else:
            return [a for a in scope.keys() if a.startswith(texto)]

    def _get_current_line(self):
        "Obtiene la linea en donde se encuentra el cursor."
        tc = self.textCursor()
        tc.select(QTextCursor.LineUnderCursor)
        return tc.selectedText()

    def cargar_desde_archivo(self, ruta):
        "Carga todo el contenido del archivo indicado por ruta."
        archivo = codecs.open(unicode(ruta), 'r', 'utf-8')
        contenido = archivo.read()
        archivo.close()
        self.setText(contenido)
        self.nombre_de_archivo_sugerido = ruta

    def guardar_contenido_en_el_archivo(self, ruta):
        texto = unicode(self.document().toPlainText())
        archivo = codecs.open(unicode(ruta), 'w', 'utf-8')
        archivo.write(texto)
        archivo.close()
        self.nombre_de_archivo_sugerido = ruta

    def paint_event_falso(self, event):
        pass

    def _restaurar_rutina_de_redibujado_original(self, paint_event_original):
        pilas = self.interpreterLocals['pilas']
        pilas.reiniciar()
        widget = pilas.obtener_widget()
        widget.__class__.paintEvent = paint_event_original

    def abrir_con_dialogo(self):
        if self.tiene_cambios_sin_guardar():
            if not self.ventana_interprete.consultar_si_quiere_perder_cambios():
                return

        ruta = QFileDialog.getOpenFileName(self, "Abrir Archivo",
                                           self.nombre_de_archivo_sugerido,
                                           "Archivos python (*.py)",
                                           options=QFileDialog.DontUseNativeDialog)

        if ruta:
            self.cargar_desde_archivo(ruta)
            self._cambios_sin_guardar = False

        if ruta:
            self.ejecutar()

    def ejecutar(self):
        texto = unicode(self.document().toPlainText())
        self.ventana_interprete.ejecutar_codigo_como_string(texto)

    def guardar_con_dialogo(self):
        ruta = QFileDialog.getSaveFileName(self, "Guardar Archivo",
                                           self.nombre_de_archivo_sugerido,
                                           "Archivos python (*.py)",
                                           options=QFileDialog.DontUseNativeDialog)

        if ruta:
            self.guardar_contenido_en_el_archivo(ruta)
            self._cambios_sin_guardar = False

        self.ejecutar()

    def _cargar_resaltador_de_sintaxis(self):
        self._highlighter = highlighter.Highlighter(
            self.document(),
            'python',
            highlighter.COLOR_SCHEME)
