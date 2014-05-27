# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
import codecs

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import Qt

from pilasengine.lanas import autocomplete
from pilasengine.lanas import editor_con_deslizador

CONTENIDO = """import pilasengine

pilas = pilasengine.iniciar()

mono = pilas.actores.Mono()

# Algunas transformaciones:
mono.x = 0
mono.y = 0
mono.escala = 1.0
mono.rotacion = 0

pilas.ejecutar()"""

class Editor(autocomplete.CompletionTextEdit, editor_con_deslizador.EditorConDeslizador):
    """Representa el editor de texto que aparece en el panel derecho.

    El editor soporta autocompletado de código y resaltado de sintáxis.
    """

    def __init__(self, main, interpreterLocals, ventana_interprete):
        autocomplete.CompletionTextEdit.__init__(self, None, self.funcion_valores_autocompletado)
        self.interpreterLocals = interpreterLocals
        self.insertPlainText(CONTENIDO)
        self.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self._cambios_sin_guardar = False
        self.main = main
        self.ventana_interprete = ventana_interprete

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

        if event.key() == QtCore.Qt.Key_Tab:
            tc = self.textCursor()
            tc.insertText("    ")
        else:
            if self.autocomplete(event):
                return None

            return QtGui.QTextEdit.keyPressEvent(self, event)

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
        tc.select(QtGui.QTextCursor.LineUnderCursor)
        return tc.selectedText()

    def cargar_desde_archivo(self, ruta):
        "Carga todo el contenido del archivo indicado por ruta."
        archivo = codecs.open(unicode(ruta), 'r', 'utf-8')
        contenido = archivo.read()
        archivo.close()
        self.setText(contenido)

    def guardar_contenido_en_el_archivo(self, ruta):
        texto = unicode(self.document().toPlainText())
        archivo = codecs.open(unicode(ruta), 'w', 'utf-8')
        archivo.write(texto)
        archivo.close()

    def paint_event_falso(self, event):
        pass

    def _reemplazar_rutina_redibujado(self):
        # HACK: en macos la aplicación se conjela si el dialogo está
        # activo y el widget de pilas se sigue dibujando. Así que
        # mientras el dialogo está activo, reemplazo el dibujado
        # del widget de pilas por unos segundos.
        pilas = self.interpreterLocals['pilas']

        widget = pilas.obtener_widget()
        paint_event_original = widget.__class__.paintEvent
        widget.__class__.paintEvent = Editor.paint_event_falso
        return paint_event_original


    def _restaurar_rutina_de_redibujado_original(self, paint_event_original):
        pilas = self.interpreterLocals['pilas']
        pilas.reiniciar()
        widget = pilas.obtener_widget()
        widget.__class__.paintEvent = paint_event_original

    def abrir_con_dialogo(self):
        if self.tiene_cambios_sin_guardar():
            if not self.ventana_interprete.consultar_si_quiere_perder_cambios():
                return

        paint_event_original = self._reemplazar_rutina_redibujado()

        ruta = QtGui.QFileDialog.getOpenFileName(self, "Abrir Archivo", "", "Archivos python (*.py)")

        if ruta:
            self.cargar_desde_archivo(ruta)
            self._cambios_sin_guardar = False

        self._restaurar_rutina_de_redibujado_original(paint_event_original)

        if ruta:
            self.ejecutar()

    def ejecutar(self):
        texto = unicode(self.document().toPlainText())
        self.ventana_interprete.ejecutar_codigo_como_string(texto)

    def guardar_con_dialogo(self):
        paint_event_original = self._reemplazar_rutina_redibujado()
        ruta = QtGui.QFileDialog.getSaveFileName(self, "Guardar Archivo", "", "Archivos python (*.py)")

        if ruta:
            self.guardar_contenido_en_el_archivo(ruta)
            self._cambios_sin_guardar = False

        self._restaurar_rutina_de_redibujado_original(paint_event_original)
        self.ejecutar()