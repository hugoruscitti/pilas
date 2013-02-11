all:
	@echo "Por favor especifica el comando de make:"
	@echo ""
	@echo "test \t Ejecuta todas las pruebas unitarias con nosetest."
	@echo "html \t Genera toda la documentacion en formato HTML."
	@echo "api \t Genera la referencia de clases, metodos y funciones."
	@echo "mac \t Genera el paquete de aplicacion para MacOSX."


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
	hdiutil create pilas-engine-0.72.dmg -srcfolder ./dist/pilas-engine.app
	@echo ""
	@echo "Para probar el programa generado ejecuta o utiliza el dmg:"
	@echo "  ./dist/pilas-engine.app/Contents/MacOS/pilas-engine"
