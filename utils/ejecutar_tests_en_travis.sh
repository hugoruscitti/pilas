# Este archivo contiene la lista de dependencias
# completas para instalar pilas sobre travis.ci, el
# sistema de integración contínua que estamos utilizando.
export DISPLAY=:99.0
sh -e /etc/init.d/xvfb start
nosetests
echo "Finaliza ejecutar tests."
