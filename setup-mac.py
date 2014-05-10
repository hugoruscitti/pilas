from setuptools import setup

setup(
    name='pilas-engine',
    app=["bin/pilas.py"],
    data_files = [
        ('bin/pilas.py', ['bin/pilas.py']),
        ],
    options={
        "py2app": {
            "argv_emulation": False,
            "includes": ["sip", "PyQt4", 'PyQt4.QtWebKit', 'PyQt4.QtNetwork'],
            "resources": ['./README.md', 'data'],
            'packages': ['pilasengine', 'lanas'],
            'iconfile': 'data/iconos/pilas.icns',
        },
    },
    setup_requires=["py2app"]
)
