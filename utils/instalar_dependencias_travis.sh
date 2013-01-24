# Este archivo contiene la lista de dependencias
# completas para instalar pilas sobre travis.ci, el
# sistema de integración contínua que estamos utilizando.
export DISPLAY=:99.0
sh -e /etc/init.d/xvfb start

sudo apt-get update 
sudo apt-get install g++ make python-dev libxext-dev
sudo apt-get install libqt4-dev python-qt4 pyqt4-dev-tools qt4-designer python-qt4-gl python-qt4-phonon
#wget http://thomasmansencal.com/Sharing/ThirdParty/Riverbank/sip-4.13.3/sip-4.13.3.tar.gz 
#tar zxf sip-4.13.3.tar.gz
#cd sip-4.13.3/
#python configure.py
#make -j 4
#sudo make install
#cd ..
#python -c 'import sip'
#wget http://thomasmansencal.com/Sharing/ThirdParty/Riverbank/PyQt%204.9.4/PyQt-x11-gpl-4.9.4.tar.gz
#tar zxf PyQt-x11-gpl-4.9.4.tar.gz
#cd PyQt-x11-gpl-4.9.4/
#echo 'yes' | python configure.py
#make -j 4
#sudo make install
#cd ..


#!/bin/bash
# This hook is run after a new virtualenv is activated.
# ~/.virtualenvs/postmkvirtualenv
 
libs=( PyQt4 sip.so )
 
python_version=python$(python -c "import sys; print (str(sys.version_info[0])+'.'+str(sys.version_info[1]))")
var=( $(which -a $python_version) )
 
get_python_lib_cmd="from distutils.sysconfig import get_python_lib; print (get_python_lib())"
lib_virtualenv_path=$(python -c "$get_python_lib_cmd")
lib_system_path=$(${var[-1]} -c "$get_python_lib_cmd")
 
for lib in ${libs[@]}
do
    ln -s $lib_system_path/$lib $lib_virtualenv_path/$lib 
done




python -c 'import PyQt4'
python -c 'import PyQt4.QtCore'
python -c 'import PyQt4.QtGui'
echo "Finaliza instalar dependencias"
