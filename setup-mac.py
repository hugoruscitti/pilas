#
# Este script permite generar la imagen de aplicacion para Mac OS X
#
# El comando que permite generar y probar la aplicacion es::
#
#    rm -r -f dist build; python setup.py py2app; ./dist/pilas-engine.app/Contents/MacOS/pilas-engine
#
# y la aplicacion generada quedara en el directorio 'dist'.
from setuptools import setup

setup(
    name='pilas-engine',
    app=["bin/pilas-mac.py"],
    data_files = [
                    ('../lanas', ['lanas']),
                    ('../lanas/lanas/lang', ['lanas/lanas/lang']),
                    ('bin/pilas-mac.py', ['bin/pilas-mac.py']),
                 ],
        options={
                    "py2app":
                        {"argv_emulation": True,
                            "includes": ["sip", "PyQt4", 'PyQt4.QtWebKit', 'PyQt4.QtNetwork'],

                    "resources": ['./README.md'],
                    'packages': ['pilas', 'lanas'],
                    'iconfile': 'pilas/data/pilas-icono.icns',

                            },
                },
    setup_requires=["py2app"]
)
