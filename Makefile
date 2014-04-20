N=\x1b[0m
V=\x1b[32;01m

all:
	@echo "Comando disponibles"
	@echo ""
	@echo "  $(V)actualizar$(N)  Actualiza pilas y los submodulos."
	@echo "  $(V)ejecutar$(N)    Ejecuta pilas sin instarlo."
	@echo "  $(V)test$(N)        Lanza todos los test de unidad."
	@echo "  $(V)ui$(N)          Actualiza todas las interfaces de usuario."
	@echo ""

actualizar:
	git pull
	git submodule update --init

ejecutar:
	python bin/pilas.py

test:
	@python -m unittest discover pilasengine/tests '*.py'

ui:
	pyuic4 -xo pilasengine/asistente/asistente_base.py pilasengine/asistente/asistente.ui
	pyuic4 -xo pilasengine/manual/manual_base.py pilasengine/manual/manual.ui
	pyuic4 -xo pilasengine/interprete/interprete_base.py pilasengine/interprete/interprete.ui
