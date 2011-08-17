import os
directorio_actual = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(directorio_actual, 'asteroides'))
from asteroides import ejecutar
