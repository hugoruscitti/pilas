import os

def renombrar_instalador_para_windows():
    lista = os.listdir('dist/')
    instalador_windows = [item for item in lista if item.endswith(".exe") and ('linux' in item or "mac" in item)]
    nombre = "dist/" + instalador_windows[0]
    os.rename(nombre, nombre.replace("linux-i686", "win32").replace("macosx-10.5-intel", "win32"))


os.system("find . -name '*.pyc' -delete")
#os.system("python setup.py sdist")
#os.system("python setup.py bdist_wininst")
#renombrar_instalador_para_windows()

os.system("python setup.py sdist upload")
#os.system("python setup.py bdist_wininst upload")
