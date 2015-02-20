self_mapa_teclado = {'.IZQUIERDA': 'izquierda',
                     '.DERECHA': 'derecha',
                     '.ARRIBA': 'arriba',
                     '.ABAJO': 'abajo',
                     '.ESPACIO': 'boton'
                     }
mapa_teclado = {'a': 'izquierda'}


for k, v in mapa_teclado:
    if v in self_mapa_teclado.items():
        index = self_mapa_teclado.values().index(v)
