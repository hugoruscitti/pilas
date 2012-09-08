=====
lanas
=====

Una consola interactiva de python simple y atractiva.

.. image:: http://farm9.staticflickr.com/8035/7952092670_f578a19afe_b.jpg


Instalación en ubuntu
---------------------

::

    sudo apt-get install python-setuptools python-qt4
    git clone http://github.com/hugoruscitti/lanas
    cd lanas
    git submodule init
    git submodule update
    sudo python setup.py install


Instalación en Mac OSX
----------------------

Similar a los pasos en ubuntu, solo que hay que usar homebrew_ para instalar pyqt4.


Gracias!
--------

A los desarrolladores kanzen_ por su magnifica biblioteca.

.. _kanzen: https://github.com/ninja-ide/kanzen
.. _homebrew: http://mxcl.github.com/homebrew/
