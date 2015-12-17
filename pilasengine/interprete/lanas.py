# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
import sys
import inspect
import os
import code
import traceback

os.environ['lanas'] = 'enabled'

from PyQt4.QtGui import (QWidget, QDesktopWidget, QPalette,
                        QColor, QTextCursor, QTextEdit,
                        QInputDialog, QApplication,
                        QKeyEvent)
from PyQt4.QtCore import Qt, QTimer

from editorbase import editor_base
import lanas_ui

import io_lanas

class PythonInterpreter(code.InteractiveInterpreter):

    def __init__(self, localVars, interprete_lanas):
        code.InteractiveInterpreter.__init__(self, localVars)
        self.interprete_lanas = interprete_lanas
        self.error_io = io_lanas.ErrorOutput(interprete_lanas)
        self.normal_io = io_lanas.NormalOutput(interprete_lanas)

    def runcode(self, cd):
        self.sobreescribir_salida_por_consola(sys)
        # redirecting stdout to our method write before calling code cd
        code.InteractiveInterpreter.runcode(self, cd)
        # redirecting back to normal stdout
        self.restaurar_salida_por_consola(sys)

    def imprimir_en_pantalla(self, *arg):
        self.sobreescribir_salida_por_consola(sys)
        print ' '.join([str(x) for x in arg])
        self.restaurar_salida_por_consola(sys)

    def sobreescribir_salida_por_consola(self, sys):
        sys.stdout = self.normal_io
        sys.stderr = self.error_io

    def restaurar_salida_por_consola(self, sys):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def showsyntaxerror(self, filename=None):
        self.error_io.write("Error de sintaxis en el codigo anterior.")

    def write(self, data):
        self.error_io.write(data)

    def es_metodo(self, linea):
        codigo = "type(%s).__name__" %(linea)

        try:
            tipo_de_dato = eval(codigo, self.locals)
        except Exception, e:
            return None

        comparacion = tipo_de_dato == "instancemethod"
        return comparacion

class WidgetLanas(QWidget, lanas_ui.Ui_Lanas):

    def __init__(self, parent=None, scope=None, codigo_inicial=None):
        super(WidgetLanas, self).__init__(parent)
        self.setupUi(self)

        self.lanas = InterpreteLanas(self, codigo_inicial)
        self.lanas.init(scope)
        self.widget_interprete.addWidget(self.lanas)

        self.resize(650, 300)
        self.center_on_screen()

    def obtener_scope(self):
        return self.lanas.interpreterLocals

    def center_on_screen(self):
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

    def closeEvent(self, event):
        sys.exit(0)

    def alternar_log(self):
        if self.log_widget.isHidden():
            self.log_widget.show()
        else:
            self.log_widget.hide()


class InterpreteLanas(editor_base.EditorBase):
    """Representa el widget del interprete.

    Esta instancia tiene como atributo "self.ventana" al
    al QWidget representado por la clase Ventana.
    """

    def __init__(self, parent, codigo_inicial=None):
        super(InterpreteLanas, self).__init__()
        self.ventana = parent

        self.refreshMarker = False
        self.multiline = False
        self.command = ''
        self.history = []
        self.historyIndex = -1

        self.interpreterLocals = {'raw_input': self.raw_input,
                                  'input': self.input,
                                  'sys': sys,
                                  'help': self.help,
                                  'ayuda': self.help}

        palette = QPalette()
        palette.setColor(QPalette.Text, QColor(0, 0, 0))
        self.setPalette(palette)

        if codigo_inicial:
            self.insertar_codigo_falso(codigo_inicial)

        self.marker()
        self.setUndoRedoEnabled(False)
        self.setContextMenuPolicy(Qt.NoContextMenu)

        self.timer_cursor = QTimer()
        self.timer_cursor.start(1000)
        self.timer_cursor.timeout.connect(self.marker_si_es_necesario)

    def insertFromMimeData(self, source):
        QTextEdit.insertPlainText(self, source.text())

    def funcion_valores_autocompletado(self, texto):
        scope = self.interpreterLocals
        texto = texto.replace('(', ' ').split(' ')[-1]
        resultados = []

        if '.' in texto:
            palabras = texto.split('.')
            ultima = palabras.pop()
            prefijo = '.'.join(palabras)

            try:
                sentencia_para_obtener_autocompletado = "[(x, callable(getattr(eval('%s'), x))) for x in dir(%s)]" %(prefijo, prefijo)
                items = eval(sentencia_para_obtener_autocompletado, scope)
                elementos = []

                for (x, invocable) in items:
                    if invocable:
                        elementos.append(x + '(')
                    else:
                        elementos.append(x)

            except:
                # TODO: notificar este error de autocompletado en algun lado...
                return []

            resultados = [a for a in elementos if a.lower().startswith(ultima.lower())]
        else:
            resultados = [a for a in scope.keys() if a.lower().startswith(texto.lower())]

        return resultados

    def canInsertFromMimeData(self, *k):
        return False

    def imprimir_linea(self, linea):
        self.insertPlainText(linea)

    def insertar_error(self, mensaje):
        mensajes = mensaje.split('\n')

        for m in mensajes:
            m = m.replace('Traceback (most recent call last)', 'Traza del error (las llamadas mas recientes al final)')
            m = m.replace('File "<string>"', 'Archivo actual')
            m = m.replace('File ', 'Archivo ')
            m = m.replace(' line ', 'linea ')
            m = m.replace('in ', 'en ')
            m = m.replace('\t', ' &nbsp; &nbsp;')

            for x in range(10):
                m = m.replace('  ', '&nbsp;&nbsp;')

            self.insertHtml(u" <b style='color: #F00000'> &nbsp; ×</b> # %s <br>" %(m.decode('utf-8')))


    def insertar_error_desde_exception(self, e):
        self.insertPlainText('\n')
        self.insertar_error("%s: %s" %(e.__class__.__name__, e.message))

        tb = traceback.format_exc()

        if tb:
            self.insertar_error(" ")
            self.insertar_error(tb)

        self._mover_cursor_al_final()

    def insertar_mensaje(self, mensaje):
        self.insertPlainText('\n')
        self.insertHtml(u" <b style='color: green'>  &nbsp; %s </b><br>" %(mensaje))
        self.insertPlainText('\n')
        self._mover_cursor_al_final()

    def insertar_codigo_falso(self, codigo):
        for line in codigo.splitlines():
            self.marker()
            self.insertHtml(line)
            self.insertPlainText('\n')

    def marker(self):
        if self.multiline:
            self.insertHtml(u"<b style='color: #FF0000'>‥</b> ")
            self.insertPlainText("    ")
        else:
            self.insertHtml(u"<b style='color: #3583FC'>»</b> ")

    def init(self, interpreter_locals):
        # Mover este metodo dentro de __init__ ?
        if interpreter_locals:
            interpreter_locals.update(self.interpreterLocals)
            self.interpreterLocals = interpreter_locals

        if 'inspect' not in self.interpreterLocals:
            self.interpreterLocals['inspect'] = inspect

        self.interpreter = PythonInterpreter(self.interpreterLocals, self)

    def clearCurrentBlock(self):
        block = self.document().lastBlock().text()[2:]
        for char in block:
            self.textCursor().deletePreviousChar()

    def recall_history(self):
        self._mover_cursor_al_final()
        self.clearCurrentBlock()
        if self.historyIndex != -1:
            self.insertPlainText(self.history[self.historyIndex])

    def _get_entered_line(self):
        textCursor = self.textCursor()
        position = len(self.document().toPlainText())
        textCursor.setPosition(position)
        self.setTextCursor(textCursor)

        line = unicode(self.document().lastBlock().text())[2:]
        line.rstrip()
        return line

    def _get_position_in_block(self):
        tc = self.textCursor()
        position = tc.positionInBlock() - 3
        return position

    def _get_current_block_prefix(self):
        tc = self.textCursor()
        tc.select(QTextCursor.BlockUnderCursor)
        current_block = tc.selectedText()
        words = current_block.split(" ")
        prefix = words[-1]

        if '(' in prefix:
            prefix = prefix.split('(')[-1]

        if '.' in prefix:
            prefixes = prefix.split('.')
            prefixes = prefixes[:-1]
            return '.'.join([str(s) for s in prefixes])
        else:
            return prefix

    def _set_current_word(self, word):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        tc.removeSelectedText()
        tc.insertText(word)

    def _mover_cursor_al_final(self):
        textCursor = self.textCursor()
        textCursor.movePosition(QTextCursor.End)
        self.setTextCursor(textCursor)
        return textCursor

    def _get_current_line(self):
        "Obtiene la linea en donde se encuentra el cursor."
        tc = self.textCursor()
        tc.select(QTextCursor.LineUnderCursor)
        return tc.selectedText()[2:]

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_ParenLeft:
            self._autocompletar_argumentos_si_corresponde()

    def keyPressEvent(self, event):
        # Permite usar tab como seleccionador de la palabra actual
        # en el popup de autocompletado.
        if event.key() in [Qt.Key_Tab]:
            if self.completer and self.completer.popup().isVisible():
                event.ignore()
                nuevo_evento = QKeyEvent(QKeyEvent.KeyPress, Qt.Key_Return, Qt.NoModifier)
                try:
                    if self.autocomplete(nuevo_evento):
                        return None
                except UnicodeEncodeError:
                    pass
                return None


        if editor_base.EditorBase.keyPressEvent(self, event):
            return None

        textCursor = self.textCursor()

        # Permite mantener pulsada la tecla CTRL para copiar o pegar.
        if event.modifiers() & Qt.ControlModifier:
            # Ignorando pegar texto si cursor está en medio de consola.
            if textCursor.blockNumber() != self.document().blockCount() - 1:
                if event.key() == Qt.Key_V:
                    textCursor = self._mover_cursor_al_final()
                    return

            # Ignorando pegar texto si cursor está sobre el prompt de consola.
            elif textCursor.positionInBlock() < 2:
                if event.key() == Qt.Key_V:
                    textCursor = self._mover_cursor_al_final()
                    return

            return QTextEdit.keyPressEvent(self, event)

        # Ignorando la pulsación de tecla si está en medio de la consola.
        if textCursor.blockNumber() != self.document().blockCount() - 1:
            textCursor = self._mover_cursor_al_final()
            return

        # Ignora el evento si está sobre el cursor de la consola.
        if textCursor.positionInBlock() < 2:
            textCursor = self._mover_cursor_al_final()
            return

        if event.key() in [Qt.Key_Left, Qt.Key_Backspace]:
            if self.textCursor().positionInBlock() == 2:
                return

        # Elimina los pares de caracteres especiales si los encuentra
        if event.key() == Qt.Key_Backspace:
            self._eliminar_pares_de_caracteres()

        # navegar por el historial
        if event.key() == Qt.Key_Down:
            if self.historyIndex == len(self.history):
                self.historyIndex -= 1
            try:
                if self.historyIndex > -1:
                    self.historyIndex -= 1
                    self.recall_history()
                else:
                    self.clearCurrentBlock()
            except:
                pass
            return None

        # navegar por el historial
        if event.key() == Qt.Key_Up:
            try:
                if len(self.history) - 1 > self.historyIndex:
                    self.historyIndex += 1
                    self.recall_history()
                else:
                    self.historyIndex = len(self.history)
            except:
                pass
            return None

        # ir al primer caracter del interprete cuando pulsa HOME
        if event.key() == Qt.Key_Home:
            blockLength = len(self.document().lastBlock().text()[2:])
            lineLength = len(self.document().toPlainText())
            position = lineLength - blockLength
            textCursor = self.textCursor()
            textCursor.setPosition(position)
            self.setTextCursor(textCursor)
            return None

        try:
            if self.autocomplete(event):
                return None
        except UnicodeEncodeError:
            pass

        if event.key() in [Qt.Key_Return, Qt.Key_Enter]:
            self.limpiar_consejo() # Limpiando consejo si existe

            line = self._get_entered_line()
            self.historyIndex = -1

            if line == "clear":
                self.limpiar()
                return

            try:
                line[-1]
                self.haveLine = True
                if line[-1] in [':', ',', '[', '(']:
                    self.multiline = True
                self.history.insert(0, line)
            except:
                self.haveLine = False

            # Cuando pulsa ENTER luego de haber hecho un texto multilinea y borrado todos los caracteres.
            if self.multiline and (not self.haveLine or self._ha_ingresado_solo_espacios(line)): #  multi line done
                self.append('') # move down one line

                try:
                    self.interpreter.runsource(self.command)
                except Exception, e:
                    self.insertar_error_desde_exception(e)

                self.command = '' # clear command
                self.multiline = False # back to single line
                self.marker() # handle marker style
                return None

            if self.haveLine and self.multiline: # multi line command
                self.command += line + '\n' # + command and line
                self.append('')
                self.marker()
                return None

            # Permite escribir lineas terminas con '?' para consultar la documentacion
            # de manera similar a como lo hace ipython.
            if line.endswith('?'):
                line = 'pilas.ver(' + line[:-1] + ')'

            if self.haveLine and not self.multiline: # one line command
                self.command = line # line is the command
                self.append('') # move down one line

                if '=' in line:
                    primer_parte = line.split('=')[0]

                    if self.interpreter.es_metodo(primer_parte):
                        print "ES METOPDO"
                        self.insertar_error("No puedes sobre-escribir un metodo, lo siento.")
                        self.command = '' # clear command
                        self.marker() # handle marker style
                        return None




                try:
                    self.interpreter.runsource(self.command)
                except Exception, e:
                    self.insertar_error_desde_exception(e)

                self.command = '' # clear command
                self.marker() # handle marker style
                return None

            # Cuando pulsa ENTER sin texto.
            if not self.haveLine and not self.multiline:
                self.append('')
                self.marker()
                return None

            return None

        return QTextEdit.keyPressEvent(self, event)

    def limpiar(self):
        self.clear()
        self.marker()
        return

    def _autocompletar_argumentos_si_corresponde(self):
        """Muestra un mensaje con la documentación de una función ejecutar.

        Se invoca mientras que el usuario escribe, siempre y cuando
        se vea un paréntisis.

        Por ejemplo, si el usuario escribe 'os.system(' esta función
        intentará mostrar un tooltip con el contenido de 'os.system.__doc__'
        """
        linea = unicode(self.document().lastBlock().text())[2:]
        linea.rstrip()

        self.limpiar_consejo()

        if '(' in linea:
            principio = linea.split('(')[0]
            principio = principio.split(' ')[-1]

            # Obtiene el mensaje a mostrar y lo despliega en el tooltip
            texto_consejo = self._obtener_firma_de_funcion(principio)
            self.mostrar_consejo(texto_consejo)

    def limpiar_consejo(self):
        self.mostrar_consejo("")

    def _obtener_firma_de_funcion(self, texto):
        codigo = self.ver_codigo(texto)

        if codigo:
            posicion = codigo.find(":")
            codigo = codigo[:posicion].replace("def ", "").replace('  ', '').replace('self, ', '').replace('self', '').replace('\n', ' ')
            return codigo
        else:
            return ""

    def ver_codigo(self, texto):
        codigo = ""
        try:
            try:
                texto_a_ejecutar = 'inspect.isclass(' + texto + ")"
                es_clase = eval(texto_a_ejecutar, self.interpreterLocals)

                if es_clase:
                    texto = texto + ".__init__"

                texto_a_ejecutar = 'inspect.getsource(' + texto + ")"
                codigo = eval(texto_a_ejecutar, self.interpreterLocals)
            except TypeError, e:
                pass
        except Exception, e:
            pass

        return codigo

    def mostrar_consejo(self, linea):
        self.ventana.consejo.setText(linea)

    def guardar_contenido_con_dialogo(self):
        ruta = self.abrir_dialogo_guardar_archivo()

        if ruta:
            self.guardar_contenido_en_el_archivo(ruta)
            self.nombre_de_archivo_sugerido = ruta
            #self.mensaje_contenido_guardado()

    def _ha_ingresado_solo_espacios(self, linea):
        # TODO: Reemplazar por una expresion regular para
        #       detectar lineas donde solo hay espacios en blanco.
        if linea == "    ":
            return True

    def obtener_contenido(self):
        texto = self.document().toPlainText()
        texto = texto.replace(u'‥ ', '')
        texto = texto.replace(u'» ', '')
        return unicode(texto)

    def marker_si_es_necesario(self):
        line = unicode(self.document().lastBlock().text())
        if not line.startswith(u'» ') and not line.startswith(u'‥ '):
            self.insertPlainText("\n")
            self.marker()
            self._mover_cursor_al_final()

    def print_en_consola_de_texto(self, texto):
        #self.stdout_original.write(texto + '\n')
        pass

    def raw_input(self, mensaje):
        text, state = QInputDialog.getText(self, "raw_input", mensaje)
        return str(text)

    def input(self, expresion):
        text, state = QInputDialog.getText(self, "raw_input", expresion)
        return eval(str(text))

    def help(self, objeto=None):
        if objeto:
            self.interpreterLocals['pilas'].ver(objeto)
        else:
            print "Escribe help(objeto) para obtener ayuda sobre ese objeto."
