all:
	@echo "Comando disponibles"
	@echo ""
	@echo "  ejecutar    Ejecuta pilas sin instarlo."
	@echo "  test        Lanza todos los test de unidad."
	@echo ""

ejecutar:
	python bin/pilasengine

test:
	@python -m unittest discover pilasengine/tests '*.py'
