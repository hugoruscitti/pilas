# -*- encoding: utf-8 -*-

import pilas
import opencv
from opencv import highgui
import os
from PySFML import sf

class DeCamara(pilas.actores.Actor):
    """
    Nos permite poner en pantalla el video proveniente de la camara web.
    
    """
    def __init__(self, ancho=640, alto=480):
        import webcam
        self.camara = webcam.CamaraWeb
        self.ultimo_numero_de_cuadro = 0
        pilas.actores.Actor.__init__(self, 'fondos/pasto.png')
        pilas.mundo.agregar_tarea(0.15,self.actualizar_video)

    def actualizar_video(self):
        cuadro, numero_de_cuadro = self.camara.obtener_imagen(self.ultimo_numero_de_cuadro)
        self.ultimo_numero_de_cuadro = numero_de_cuadro
        self.imagen.LoadFromPixels(640, 480, cuadro)        
        return True

class VideoDeArchivo(object):
    def __init__(self, ruta):
        if not os.path.isfile(ruta):
            raise IOError('El archiyo no existe')
        self._camara = highgui.cvCreateFileCapture(ruta)
        self.fps = highgui.cvGetCaptureProperty(self._camara, highgui.CV_CAP_PROP_FPS)
        self.altura = highgui.cvGetCaptureProperty(self._camara, highgui.CV_CAP_PROP_FRAME_HEIGHT)
        self.ancho =highgui.cvGetCaptureProperty(self._camara, highgui.CV_CAP_PROP_FRAME_WIDTH)
        super(VideoDeArchivo, self).__init__()

    def obtener_imagen(self):
        imagen_ipl = highgui.cvQueryFrame(self._camara)
        imagen_ipl = opencv.cvGetMat(imagen_ipl)
        return opencv.adaptors.Ipl2PIL(imagen_ipl).convert('RGBA').tostring() 
        

class DePelicula(pilas.actores.Actor):
    """
    Nos permite poner en pantalla un video desde un archivo.
    Toma como parámetro la ruta del video.
    """
    def __init__(self, path, ancho=640, alto=480):
        self._camara = VideoDeArchivo(path)
        pilas.actores.Actor.__init__(self)
        self._altura_cuadro = self._camara.altura
        self._ancho_cuadro = self._camara.ancho
        subrect = self._actor.GetSubRect()
        subrect.Right = self._ancho_cuadro
        subrect.Bottom = self._altura_cuadro
        self._actor.SetSubRect(subrect)
        self.centro = ('centro', 'centro')
        pilas.mundo.agregar_tarea(1/self._camara.fps,self.actualizar_video)

    def actualizar_video(self):
        self.imagen.LoadFromPixels(self._ancho_cuadro, self._altura_cuadro, self._camara.obtener_imagen())        
        return True
