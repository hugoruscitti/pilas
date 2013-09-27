Depurando y buscando detalles
=============================

Pilas incluye varios modos de ejecución que te
pueden resultar de utilidad para ver en detalle
el funcionamiento de tu juego.

La depuración dentro de la progración de juegos permite detectar errores, corregir
detalles e incluso comprender algunas interacciones complejas.

Modo pausa y manejo de tiempo
-----------------------------

Si pulsas las teclas ``ALT + P`` durante la ejecución de
pilas, el juego completo se detiene. En ese 
momento puedes pulsar cualquier tecla
para avanzar un instante de la simulación o 
la tecla ``flecha derecha`` para avanzar mas rápidamente.

Esto es muy útil cuando trabajas con colisiones físicas, porque
este modo de pausa y manejo de tiempo te permite
ver en detalle la interacción de los objetos y detectar
cualquier inconveniente rápidamente.


Modos depuración
----------------

Las teclas **F6**, **F7**, **F8**, **F9**, **F10**, **F11** y **F12** te permiten
hacer visibles los modos de depuración.

Cada modo representa un aspecto interno del juego que podrías ver. Por ejemplo, el
modo que se activa con la tecla **F12** te permite ver la posición exácta de
cada actor, mientras que al tecla **F11** te permite ver las figuras físicas.

Activar modos desde código
--------------------------

Si quieres que el juego inicie alguno de los modos, puedes usar la
función ``pilas.atajos.definir_modos``. Por ejemplo, para habilitar el
modo depuración física podrías escribir:

.. code-block:: python

    pilas.atajos.definir_modos(fisica=True)

esta función tiene varios argumentos opcionales, cómo ``posicion``, ``radios`` etc. Mira
la definición de la función para obtener mas detalles:

.. automethod:: pilas.depurador.Depurador.definir_modos

Activando los modos para detectar errores
-----------------------------------------

Ten en cuenta que puedes activar los modos depuración en cualquier momento,
incluso en medio de una pausa, ir del modo depuración al
modo pausa y al revés. Los dos modos se pueden
combinar fácilmente.

Mi recomendación es que ante la menor duda, pulses **alt + p** para
ir al modo pausa, y luego comiences a pulsar alguna de las teclas para
activar los modos depuración y observar en detalle qué está ocurriendo: **F6** , **F7** etc.
