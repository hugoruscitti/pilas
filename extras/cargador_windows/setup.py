# -*- encoding: utf-8 -*-
from cx_Freeze import setup
from cx_Freeze import Executable
import pkg_resources

exe = Executable(
        script="cargador.py",
        base="Win32GUI",
        #base="Console",
        icon='pilas.ico',
        
        compress = True,
        copyDependentFiles = True,
        appendScriptToExe = False,
        appendScriptToLibrary = False,
)

extra_options = {
    "packages": ["pilasengine", "lanas", "json", "pygame", "setuptools", "code", "simplejson"],
    "optimize" : 2,
    "compressed": False,
}

setup(
    name="Cargador",
    version="0.1",
    options = {"build_exe": extra_options},
    description="Un cargador de juegos realizados con pilas-engine",
    executables=[exe],
)
