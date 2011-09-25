'''
import pilas
try:
    import Image
    import opencv
    from opencv import highgui 

    GLOBALCAM=highgui.cvCreateCameraCapture(0)

    for algo in range(30):
        ULTIMO_CUADRO_BASURA = highgui.cvQueryFrame(GLOBALCAM)

    ULTIMO_CUADRO_BASURA = opencv.adaptors.Ipl2PIL(opencv.cvGetMat(ULTIMO_CUADRO_BASURA)).convert('RGBA')
except ImportError:
    print "Falta la biblioteca opencv o PIL"
    pass


class __camara_buffer(object):
    def __init__(self):
        self._ultimo_numero_de_cuadro = 0
        self._camera = GLOBALCAM
        self._ultimo_cuadro = ULTIMO_CUADRO_BASURA.tostring() 
        
    def _obtener_imagen_de_camara(self):
        imagen_ipl = highgui.cvQueryFrame(self._camera)
        imagen_ipl = opencv.cvGetMat(imagen_ipl)
        self._ultimo_cuadro = opencv.adaptors.Ipl2PIL(imagen_ipl).convert('RGBA').tostring() 

    def obtener_imagen(self, numero_de_cuadro=0):
        if numero_de_cuadro == self._ultimo_numero_de_cuadro:
           self._obtener_imagen_de_camara()
           self._ultimo_numero_de_cuadro += 1
        return self._ultimo_cuadro, self._ultimo_numero_de_cuadro

CamaraWeb = __camara_buffer()
'''
