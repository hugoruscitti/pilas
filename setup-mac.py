#
# Este script permite generar la imagen de aplicacion para Mac OS X
#
# El comando que permite generar y probar la aplicacion es::
#
"""

rm -r -f dist build; python setup-mac.py py2app;
rm dist/pilas-engine.app/Contents/Resources/qt.conf
macdeployqt dist/pilas-engine.app
hdiutil create pilas-engine-0.72.dmg -srcfolder ./dist/pilas-engine.app

"""
#
#
#    ./dist/pilas-engine.app/Contents/MacOS/pilas-engine
#
# y la aplicacion generada quedara en el directorio 'dist'.
from setuptools import setup

setup(
    name='pilas-engine',
    app=["bin/pilas-mac.py"],
    data_files = [
        ('../lanas', ['lanas']),
        ('bin/pilas-mac.py', ['bin/pilas-mac.py']),
        #('../PlugIns/phonon_backend', ['/usr/local/Cellar/qt/4.8.4/plugins/phonon_backend/libphonon_qt7.dylib']),
        ],
    options={
        "py2app": {
            "argv_emulation": False,
            "includes": ["sip", "PyQt4", 'PyQt4.QtWebKit', 'PyQt4.QtNetwork'],
            "resources": ['./README.md'],
            'packages': ['pilas', 'lanas'],
            'iconfile': 'pilas/data/pilas-icono.icns',
        },
    },
    setup_requires=["py2app"]
)
