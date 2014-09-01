from setuptools import setup

setup(
    name='pilas-engine',
    version="0.90.3",
    app=["bin/pilasengine"],
    data_files = [
        ('bin/pilasengine', ['bin/pilasengine']),
        ],
    options={
        "py2app": {
            "argv_emulation": False,
            "includes": ["sip", "PyQt4", 'PyQt4.QtWebKit', 'PyQt4.QtNetwork'],
            "resources": ['./README.md', 'data'],
            'packages': ['pilasengine'],
            'iconfile': 'data/iconos/pilas.icns',
        },
    },
    setup_requires=["py2app"]
)
