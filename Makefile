N=\x1b[0m
V=\x1b[32;01m

VERSION=0.85

all:
	@echo "Comando disponibles"
	@echo ""
	@echo "  $(V)actualizar$(N)  Actualiza pilas y los submodulos."
	@echo "  $(V)ejecutar$(N)    Ejecuta pilas sin instarlo."
	@echo "  $(V)test$(N)        Lanza todos los test de unidad."
	@echo "  $(V)ui$(N)          Actualiza todas las interfaces de usuario."
	@echo ""
	@echo "  $(V)clean$(N)       Limpia los archivos temporales."
	@echo "  $(V)distmac$(N)     Genera la versión compilada para macos."
	@echo ""

actualizar:
	git pull
	git submodule update --init

ejecutar:
	python bin/pilas.py

test:
	@python -m unittest discover pilasengine/tests '*.py'
	# O una version mas linda si se instala nose y nosecolor con pip
	#@nosetests --color pilasengine/tests/*

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
