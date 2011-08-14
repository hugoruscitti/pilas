import os

def renombrar_instalador_para_windows():
    lista = os.listdir('dist/')
    instalador_windows = [item for item in lista if item.endswith(".exe")]
    nombre = "dist/" + instalador_windows[0]
    os.rename(nombre, nombre.replace("linux-i686", "win32"))


os.system("python setup.py sdist")
os.system("python setup.py bdist_wininst")
renombrar_instalador_para_windows()

os.system("python setup.py sdist upload")
os.system("python setup.py bdist_wininst upload")
