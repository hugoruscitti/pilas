# -*- encoding: utf-8 -*-
import datetime
import subprocess


template = u"""
window.DESCRIPCION_VERSION = {
  version: 'VERSION_STR',
  fecha: 'FECHA',
  commit: 'COMMIT',
  changelog: CHANGELOG_LIST
}
"""

lista = subprocess.check_output(['sh', 'extras/listar_mensajes_commits.sh']).splitlines()

commit = subprocess.check_output(['git', 'log', '-1', '--oneline']).split(' ')[0]
hoy = datetime.date.today()

template = template.\
  replace('VERSION_STR', '0.90.3').\
  replace('FECHA', hoy.strftime('%d de %b del %Y')).\
  replace('CHANGELOG_LIST', str(lista)).\
  replace('COMMIT', str(commit))

f = open('data/asistente/js/version.js', 'wt')
f.write(template)
f.close()

print "Generando el archivo 'data/asistente/js/version.js' con los datos de versión actualizados."
