import pilas
from PySFML import sf

import os

def get_file_path(path):

    dirs = ['./', 'data', pilas.path, pilas.path + '/data']

    for x in dirs:
        full_path = os.path.join(x, path)
        #DEBUG: print "buscando en: '%s'" %(full_path)

        if os.path.exists(full_path):
            return full_path

    # Si no ha encontrado el archivo lo reporta.
    raise IOError("El archivo '%s' no existe." %(path))

def cargar(path):
    path = get_file_path(path)

    buff = sf.SoundBuffer()
    buff.LoadFromFile(path)
    return sf.Sound(buff)
