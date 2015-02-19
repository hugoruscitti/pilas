N=[0m
V=[01;32m

VERSION=0.90.26

all:
	@echo ""
	@echo "Comandos disponibles versión: (${VERSION})"
	@echo ""
	@echo "  $(V)actualizar$(N)  Actualiza pilas y los submodulos."
	@echo "  $(V)ejecutar$(N)    Ejecuta pilas sin instarlo."
	@echo "  $(V)utest$(N)       Lanza todos los test de unidad."
	@echo "  $(V)ui$(N)          Actualiza todas las interfaces de usuario."
	@echo "  $(V)manual$(N)      Actualiza el manual y lo copia a data/manual."
	@echo "  $(V)rm_pyc$(N)      Borra todos los archivos .pyc del proyecto."
	@echo ""
	@echo "  $(V)clean$(N)       Limpia los archivos temporales."
	@echo "  $(V)version$(N)     Genera el changelog y la informacion de versión."
	@echo "  $(V)ver_sync$(N)    Sube la nueva version al servidor."
	@echo "  $(V)ejemplos$(N)    Prueba los ejemplos uno a uno."
	@echo ""
	@echo "  $(V)dist$(N)        Genera todos los binarios (excepto .deb)"
	@echo "   $(V)distmac$(N)     Genera la versión compilada para macos."
	@echo "   $(V)distwin$(N)     Genera la versión compilada para windows."
	@echo "   $(V)distdeb$(N)     Genera la versión compilada para debian o huayra."
	@echo ""

actualizar:
	git pull
	git submodule update --init

ejecutar:
	python bin/pilasengine

test_mac:
	python bin/pilasengine

ejecutar_mac: test_mac

.PHONY: test ejemplos

version:
	@bumpversion --current-version ${VERSION} patch setup.py setup-mac.py pilasengine/__init__.py ./extras/actualizar_version.py ./extras/instalador.nsi Makefile --list
	@python extras/actualizar_version.py
	@echo "Es recomendable escribir el comando que genera los tags y sube todo a github:"
	@echo ""
	@echo "make ver_sync"

ver_sync:
	git commit -am 'release ${VERSION}'
	git tag '${VERSION}'
	git push
	git push --all
	git push --tags

utest:
	@python -m unittest discover pilasengine/tests '*.py'
	# O una version mas linda si se instala nose y nosecolor con pip
	#@nosetests --color pilasengine/tests/*

manual:
	mkdir -p data/manual
	cd ../pilas-manual; make generar;
	cp -R -f ../pilas-manual/site/* data/manual/
	git add data/manual
	git commit -m "actualizando manual."

ui:
	pyuic4 -xo pilasengine/asistente/asistente_base.py pilasengine/asistente/asistente.ui
	pyuic4 -xo pilasengine/manual/manual_base.py pilasengine/manual/manual.ui
	pyuic4 -xo pilasengine/interprete/interprete_base.py pilasengine/interprete/interprete.ui
	pyuic4 -xo pilasengine/interprete/editor_ui.py pilasengine/interprete/editor.ui
	pyuic4 -xo pilasengine/interprete/lanas_ui.py pilasengine/interprete/lanas.ui
	pyuic4 -xo pilasengine/configuracion/configuracion_base.py pilasengine/configuracion/configuracion.ui
	@echo "Quitando la marca de fechas."
	@sed -i '' '/Created:/d' pilasengine/asistente/asistente_base.py
	@sed -i '' '/Created:/d' pilasengine/manual/manual_base.py
	@sed -i '' '/Created:/d' pilasengine/interprete/interprete_base.py
	@sed -i '' '/Created:/d' pilasengine/interprete/editor_ui.py
	@sed -i '' '/Created:/d' pilasengine/interprete/lanas_ui.py
	@sed -i '' '/Created:/d' pilasengine/configuracion/configuracion_base.py


clean:
	rm -r -f *.dmg
	rm -r -f dist build


directorio_dist:
	@echo "Limpiando el directorio dist."
	@rm -r -f dist
	@mkdir -p dist

dist: directorio_dist distmac distwin
	@echo "listo..."
	@echo ""
	@echo "$(V)Usa el comando 'make upload' para subir esta version a dropbox.$(N)"
	@echo ""

upload:
	mkdir -p ~/Dropbox/Public/releases/pilas-engine/${VERSION}
	cp dist/pilas-engine-${VERSION}.dmg ~/Dropbox/Public/releases/pilas-engine/${VERSION}/
	cp dist/pilas-engine_${VERSION}.exe ~/Dropbox/Public/releases/pilas-engine/${VERSION}/

distmac:
	@mkdir -p tmp
	@echo "Limpiando escenario"
	@rm -r -f __MACOSX
	@rm -r -f pilas-engine.app
	@rm -r -f pilas-engine.app.zip
	@echo "Copiando plantilla de aplicación para osx desde dropbox"
	@cp /Users/hugoruscitti/Dropbox/pilas-engine-bins/pilas-engine.app.zip ./
	@echo "Descomprimiendo..."
	@unzip pilas-engine.app.zip > tmp/log_unzip_pilas-engine.zip.log
	@echo "Actualizando contenido..."
	@rm pilas-engine.app.zip
	@rm -r -f pilas-engine.app/Contents/Resources/data
	@rm -r -f pilas-engine.app/Contents/Resources/lib/python2.7/pilasengine
	@rm -r -f pilas-engine.app/Contents/Resources/lib/python2.7/pilas
	@cp -r -f data pilas-engine.app/Contents/Resources/
	@cp -r -f pilasengine pilas-engine.app/Contents/Resources/lib/python2.7/
	@cp -r -f pilas pilas-engine.app/Contents/Resources/lib/python2.7/
	@rm -r -f dist/pilas-engine-${VERSION}.dmg
	@echo "Generando imagen .dmg (esto tarda un huevo...)"
	@hdiutil create dist/pilas-engine-${VERSION}.dmg -srcfolder pilas-engine.app -size 500mb > tmp/log_creacion_dmg.log
	@rm -r -f __MACOSX
	@rm -r -f pilas-engine.app
	@rm -r -f pilas-engine.app.zip
	@echo "Todo OK!"
	@echo "Los archivos generados están en el directorio dist/"
	@echo "Se abre una ventana para mostrarlos."
	@open dist


distmac_anterior: clean
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
	@mkdir -p tmp
	@echo "Limpiando escenario"
	@rm -r -f tmp/pilas-engine
	@rm -r -f tmp/__MACOSX
	@echo "Copiando plantilla de aplicación para windows desde dropbox"
	@cp /Users/hugoruscitti/Dropbox/pilas-engine-bins/pilas-engine-cargador-windows.zip ./tmp
	@echo "Descomprimiendo..."
	@unzip tmp/pilas-engine-cargador-windows.zip -d tmp/ > tmp/log_unzip_pilas-engine.zip.log
	@echo "Actualizando contenido..."
	@cp -r -f data tmp/pilas-engine/
	@cp -r -f pilasengine tmp/pilas-engine/
	@cp -r -f pilas tmp/pilas-engine/
	@cp extras/instalador.nsi tmp/pilas-engine
	@echo "Generando el installador para windows..."
	@makensis tmp/pilas-engine/instalador.nsi > tmp/log_instalador.log
	@mv tmp/pilas-engine/pilas-engine_${VERSION}.exe dist/
	@echo "Todo OK!"
	@echo "Los archivos generados están en el directorio dist/"
	@echo "Se abre una ventana para mostrarlos."
	@open dist


distdeb:
	extras/actualizar_changelog.sh
	pdebuild
