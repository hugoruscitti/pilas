VERSION=0.78


all:
	@echo "Por favor especifica el comando de make:"
	@echo ""
	@echo "  test     Ejecuta todas las pruebas unitarias con nosetest."
	@echo "  html     Genera toda la documentacion en formato HTML."
	@echo "  api      Genera la referencia de clases, metodos y funciones."
	@echo "  mac      Genera el paquete de aplicacion para MacOSX."
	@echo "  ubuntu   Genera el paquete de aplicacion para Ubuntu GNU/Linux."
	@echo "  pypi     Genera y sube el paquete de código a pypi.org"
	@echo ""


test:
	nosetests

html:
	@cd doc; make html

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
	rm -r -f dist build; python setup-mac.py py2app;
	rm dist/pilas-engine.app/Contents/Resources/qt.conf
	macdeployqt dist/pilas-engine.app
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
