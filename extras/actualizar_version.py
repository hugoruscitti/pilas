# -*- encoding: utf-8 -*-
import datetime
import subprocess
import codecs


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

changelist = [item.decode('utf-8') for item in lista]
item = u"["

for x in changelist:
    item = item + "'" + x.replace("'", "\"") + "', "

item = item + ']'
changelist = item

template = template.\
  replace('VERSION_STR', '0.90.30').\
  replace('FECHA', hoy.strftime('%d de %b del %Y')).\
  replace('CHANGELOG_LIST', changelist).\
  replace('COMMIT', str(commit))

file = codecs.open('data/asistente/js/version.js', 'wt', 'utf-8')
file.write(template)
file.close()

print "Generando el archivo 'data/asistente/js/version.js' con los datos de versión actualizados."
