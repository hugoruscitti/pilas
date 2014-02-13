VERSION=0.84


all:
	@echo "Por favor especifica el comando de make:"
	@echo ""
	@echo "  test     Ejecuta todas las pruebas unitarias con nosetest."
	@echo "  test_mac Ejecuta la aplicacion en macosx."
	@echo "  html     Actualiza el manual en HTML y genera los PDF para subir a la web."
	@echo "  api      Genera la referencia de clases, metodos y funciones."
	@echo "  mac      Genera el paquete de aplicacion para MacOSX."
	@echo "  ubuntu   Genera el paquete de aplicacion para Ubuntu GNU/Linux."
	@echo "  pypi     Genera y sube el paquete de código a pypi.org"
	@echo "  ui       Vuelve a generar los archivo de interfaz de usuario hechos con QtDesigner"
	@echo ""


test:
	nosetests

# TODO: hacer que tambien genere el archivo PDF del manual y que la regla se llame 'docs'
html:
	@cd docs; make


ui:
	pyuic4 -o pilas/lanzador_base.py -x pilas/data/lanzador.ui
	pyuic4 -o pilas/asistente_base.py -x pilas/data/asistente.ui
	pyuic4 -o pilas/interprete_base.py -x pilas/data/interprete.ui
	pyuic4 -o pilas/manual_base.py -x pilas/data/manual.ui
	pyuic4 -o pilas/tutoriales_base.py -x pilas/data/tutoriales.ui

api:
	## IMPORTANTE: Aplica el siguiente patch a epydoc
	## 
	## http://stackoverflow.com/a/6705529
	rm -r -f doc/build/api
	mkdir -p doc/build/api
	epydoc pilas -c utils/epydoc.css -o doc/build/api --html --graph classtree --docformat restructuredtext --debug -v --no-frames
	cp -r doc/source/images doc/build/api/
	@echo ""
	@echo "Nota: el resultado de la documentación está en:"
	@echo "  doc/build/api/index.html"

mac:
	rm -r -f *.dmg
	rm -r -f dist build; python setup-mac.py py2app --no-strip;
	rm dist/pilas-engine.app/Contents/Resources/qt.conf
	macdeployqt dist/pilas-engine.app
	#rm -r -f macbins.tar.gz
	#cp /Users/hugoruscitti/Dropbox/macbins.tar.gz ./
	#tar xzvf macbins.tar.gz
	#cp -r -f macbins/Frameworks dist/pilas-engine.app/Contents/
	#cp -r -f macbins/PlugIns dist/pilas-engine.app/Contents/
	#cp -r -f macbins/Resources/lib/python2.7/lib-dynload dist/pilas-engine.app/Contents/Resources/lib/python2.7/
	hdiutil create pilas-engine-${VERSION}.dmg -srcfolder ./dist/pilas-engine.app
	@echo ""
	@echo "Para probar el programa generado ejecuta o utiliza el dmg:"
	@echo "  ./dist/pilas-engine.app/Contents/MacOS/pilas-engine"

ubuntu:
	@echo "Limpiando los paquetes de pilas .deb antiguos"
	rm -rf utils/paquete-ubuntu/*.deb
	cd utils/paquete-ubuntu/; sh generar_paquete.sh ${VERSION}; mv *.deb ../../

pypi:
	python utils/actualizar_pypi.py

test_mac:
	python bin/pilas
