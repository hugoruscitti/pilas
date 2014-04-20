all:
	@echo "Comando disponibles"
	@echo ""
	@echo "  ejecutar    Ejecuta pilas sin instarlo."
	@echo "  test        Lanza todos los test de unidad."
	@echo "  ui          Actualiza todas las interfaces de usuario."
	@echo ""

ejecutar:
	python bin/pilasengine

test:
	@python -m unittest discover pilasengine/tests '*.py'

ui:
	pyuic4 -xo pilasengine/asistente/asistente_base.py pilasengine/asistente/asistente.ui
	pyuic4 -xo pilasengine/manual/manual_base.py pilasengine/manual/manual.ui
	pyuic4 -xo pilasengine/interprete/interprete_base.py pilasengine/interprete/interprete.ui
