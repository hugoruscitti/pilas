ui:
	pyuic4 -o ui.py -x ui.ui


capturas:
	cd ejemplos; for x in `ls *.png`; do convert -scale 400 "$$x" "capturas/$$x"; echo $$x; done
