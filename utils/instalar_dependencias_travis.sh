# Este archivo contiene la lista de dependencias
# completas para instalar pilas sobre travis.ci, el
# sistema de integración contínua que estamos utilizando.
export DISPLAY=:99.0
sh -e /etc/init.d/xvfb start

sudo apt-get update 
sudo apt-get install g++ make python-dev libxext-dev
sudo apt-get install libqt4-dev python-qt4 pyqt4-dev-tools qt4-designer python-qt4-gl python-qt4-phonon
wget http://thomasmansencal.com/Sharing/ThirdParty/Riverbank/sip-4.13.3/sip-4.13.3.tar.gz 
tar zxf sip-4.13.3.tar.gz
cd sip-4.13.3/
python configure.py
make
sudo make install
cd ..
python -c 'import sip'
wget http://thomasmansencal.com/Sharing/ThirdParty/Riverbank/PyQt%204.9.4/PyQt-x11-gpl-4.9.4.tar.gz
tar zxf PyQt-x11-gpl-4.9.4.tar.gz
cd PyQt-x11-gpl-4.9.4/
echo 'yes' | python configure.py
make
sudo make install
cd ..
python -c 'import PyQt4'
python -c 'import PyQt4.QtCore'
python -c 'import PyQt4.QtGui'
