N=[0m
V=[01;32m

VERSION=0.90.5

all:
	@echo "Comando disponibles"
	@echo ""
	@echo "  $(V)actualizar$(N)  Actualiza pilas y los submodulos."
	@echo "  $(V)ejecutar$(N)    Ejecuta pilas sin instarlo."
	@echo "  $(V)utest$(N)       Lanza todos los test de unidad."
	@echo "  $(V)ui$(N)          Actualiza todas las interfaces de usuario."
	@echo "  $(V)manual$(N)      Intenta actualizar la documentación y la copia a data/manual."
	@echo "  $(V)rm_pyc$(N)      Borra todos los archivos .pyc del proyecto."
	@echo ""
	@echo "  $(V)clean$(N)       Limpia los archivos temporales."
	@echo "  $(V)version$(N)     Genera el changelog y la informacion de versión en el asistente."
	@echo "  $(V)ver_sync$(N)    Sube la nueva version al servidor."
	@echo "  $(V)ejemplos$(N)    Prueba los ejemplos uno a uno."
	@echo ""
	@echo "  $(V)distmac$(N)     Genera la versión compilada para macos."
	@echo "  $(V)distwin$(N)     Genera la versión compilada para windows."
	@echo "  $(V)distdeb$(N)     Genera la versión compilada para debian, ubuntu o huayra."
	@echo ""

actualizar:
	git pull
	git submodule update --init

ejecutar:
	python bin/pilasengine

test_mac:
	python bin/pilasengine

.PHONY: test ejemplos

version:
	@bumpversion --current-version ${VERSION} patch setup.py setup-mac.py ./extras/actualizar_version.py Makefile --list
	@python extras/actualizar_version.py
	@echo "Es recomendable escribir el comando que genera los tags y sube todo a github:"
	@echo ""
	@echo "make ver_sync"

ver_sync:
	git commit -am 'release ${VERSION}'
	git tag '${VERSION}'
	git push --all

utest:
	@python -m unittest discover pilasengine/tests '*.py'
	# O una version mas linda si se instala nose y nosecolor con pip
	#@nosetests --color pilasengine/tests/*

manual:
	mkdir -p data/manual
	cd ../pilas-manual; make generar; 
	cp -R -f ../pilas-manual/site/* data/manual/

ui:
	pyuic4 -xo pilasengine/asistente/asistente_base.py pilasengine/asistente/asistente.ui
	pyuic4 -xo pilasengine/manual/manual_base.py pilasengine/manual/manual.ui
	pyuic4 -xo pilasengine/interprete/interprete_base.py pilasengine/interprete/interprete.ui
	pyuic4 -xo pilasengine/interprete/editor_ui.py pilasengine/interprete/editor.ui
	pyuic4 -xo pilasengine/interprete/lanas_ui.py pilasengine/interprete/lanas.ui
	pyuic4 -xo pilasengine/configuracion/configuracion_base.py pilasengine/configuracion/configuracion.ui

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

ejemplos:
	python extras/probar_ejemplos.py

distwin:
	clear
	git submodule update --init
	git pull

	@echo ""
	@echo "$(V)Compilando pilas ...$(N)"
	@echo ""
	/C/Python27/python.exe setup.py build > pilas_build.log

	@echo ""
	@echo "$(V)Instalando...$(N)"
	@echo ""
	/C/Python27/python.exe setup.py install -f > pilas_install.lo

	@echo ""
	@echo "$(V)Generando el cargador$(N)"
	@echo ""
	cd extras/cargador_windows/ && \
	rm -r -f build && \
	rm -r -f pilasengine && \
	python setup.py build > pilas_compilacion.log && \
	mv build/exe.win32-2.7/ pilasengine && \
	rmdir build

	@echo ""
	@echo "$(V)Regresa al directorio principal.$(N)"
	@echo ""
	
	@echo ""
	@echo "$(V)Copia el resto de los archivos para el cargador:$(N)"
	@echo ""

	cp bin/pilasengine extras/cargador_windows/pilasengine/ejecutar.py
	cp -R data extras/cargador_windows/pilasengine/
	cp -R pilasengine extras/cargador_windows/pilasengine/
	cp extras/cargador_windows/pilas.ico extras/cargador_windows/pilasengine

	explorer.exe "extras\cargador_windows"

distdeb:
	extras/actualizar_changelog.sh
	pdebuild
