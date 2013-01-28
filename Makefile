all:
	@echo "Por favor especifica el comando de make:"
	@echo ""
	@echo "test \t Ejecuta todas las pruebas unitarias con nosetest."
	@echo "html \t Genera toda la documentacion en formato HTML."
	@echo "api \t Genera la referencia de clases, metodos y funciones."

test:
	nosetests

html:
	@cd doc; make html

api:
	epydoc pilas -c utils/epydoc.css -o doc/build/api
	@echo ""
	@echo "Nota: el resultado de la documentación está en:"
	@echo "  doc/build/html/index.html"
