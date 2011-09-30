import os
directorio_actual = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(directorio_actual, 'tres_en_raya'))
from tres_en_raya import ejecutar
