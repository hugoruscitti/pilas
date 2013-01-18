# Este archivo contiene la lista de dependencias
# completas para instalar pilas sobre travis.ci, el
# sistema de integración contínua que estamos utilizando.
export DISPLAY=:99.0
sh -e /etc/init.d/xvfb start

sudo apt-get update 
sudo apt-get install g++ make python-dev libxext-dev
sudo apt-get install libqt4-dev python-qt4 pyqt4-dev-tools qt4-designer python-qt4-gl python-qt4-phonon
wget http://www.riverbankcomputing.co.uk/static/Downloads/sip4/sip-4.14.3-snapshot-ee3b1348996c.tar.gz
tar zxf sip-4.14.3-snapshot-ee3b1348996c.tar.gz
cd sip-4.14.3-snapshot-ee3b1348996c/
python configure.py
make
sudo make install
cd ..
python -c 'import sip'
wget http://www.riverbankcomputing.co.uk/static/Downloads/PyQt4/PyQt-x11-gpl-snapshot-4.10-e143a1307289.tar.gz
tar zxf PyQt-x11-gpl-snapshot-4.10-e143a1307289.tar.gz
cd PyQt-x11-gpl-snapshot-4.10-e143a1307289
echo 'yes' | python configure.py
make
sudo make install
cd ..
python -c 'import PyQt4'
python -c 'import PyQt4.QtCore'
python -c 'import PyQt4.QtGui'
