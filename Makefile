N=\x1b[0m
V=\x1b[32;01m

VERSION=0.90

all:
	@echo "Comando disponibles"
	@echo ""
	@echo "  $(V)actualizar$(N)  Actualiza pilas y los submodulos."
	@echo "  $(V)ejecutar$(N)    Ejecuta pilas sin instarlo."
	@echo "  $(V)test$(N)        Lanza todos los test de unidad."
	@echo "  $(V)ui$(N)          Actualiza todas las interfaces de usuario."
	@echo "  $(V)html$(N)        Actualiza toda la documentación y la copia a pilas/data/manual."
	@echo "  $(V)rm_pyc$(N)      Borra todos los archivos .pyc del proyecto."
	@echo ""
	@echo "  $(V)clean$(N)       Limpia los archivos temporales."
	@echo "  $(V)distmac$(N)     Genera la versión compilada para macos."
	@echo "  $(V)distwin$(N)     Genera la versión compilada para windows."
	@echo ""

actualizar:
	git pull
	git submodule update --init

ejecutar:
	python bin/pilas.py

test_mac:
	python bin/pilas.py


test:
	@python -m unittest discover pilasengine/tests '*.py'
	# O una version mas linda si se instala nose y nosecolor con pip
	#@nosetests --color pilasengine/tests/*

html:
	cd docs; make

ui:
	pyuic4 -xo pilasengine/asistente/asistente_base.py pilasengine/asistente/asistente.ui
	pyuic4 -xo pilasengine/manual/manual_base.py pilasengine/manual/manual.ui
	pyuic4 -xo pilasengine/interprete/interprete_base.py pilasengine/interprete/interprete.ui

clean:
	rm -r -f *.dmg
	rm -r -f dist build

distmac: clean
	python setup-mac.py py2app --no-strip > log_distmac.txt
	hdiutil create dist/pilas-engine-${VERSION}.dmg -srcfolder ./dist/pilas-engine.app -size 200mb
	@echo "Los archivos generados están en el directorio dist/"
	@echo "Se abre una ventana para mostrarlos."
	@open dist

rm_pyc: clean
	find . -name "*.pyc" -exec rm -rf {} \;


distwin:
	clear
	git submodule update --init
	git pull

	echo "Compilando pilas ..."
	/C/Python27/python.exe setup.py build > pilas_build.log

	echo "Instalando..."
	/C/Python27/python.exe setup.py install -f > pilas_install.lo

	echo "Generando el cargador"
	cd extras/cargador_windows/ && \
	rm -r -f build && \
	rm -r -f pilasengine && \
	python setup.py build > pilas_compilacion.log && \
	mv build/exe.win32-2.7/ pilasengine && \
	rmdir build && \
	echo "Regresa al directorio principal."
	
	echo "Copia el resto de los archivos para el cargador:"
	cp bin/pilas.py extras/cargador_windows/pilasengine/ejecutar.py
	cp -R data extras/cargador_windows/pilasengine/
	cp -R pilasengine extras/cargador_windows/pilasengine/
	cp extras/cargador_windows/pilas.ico extras/cargador_windows/pilasengine

	explorer.exe "extras\cargador_windows"
