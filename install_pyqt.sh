#!/bin/sh
cd ..
curl -O http://thomasmansencal.com/Sharing/ThirdParty/Riverbank/sip-4.13.3/sip-4.13.3.tar.gz
tar -xvf sip-4.13.3.tar.gz
cd sip-4.13.3
python configure.py
make
sudo make install
cd ..
curl -O http://thomasmansencal.com/Sharing/ThirdParty/Riverbank/PyQt%204.9.4/PyQt-x11-gpl-4.9.4.tar.gz
tar -xvf PyQt-x11-gpl-4.9.4.tar.gz
cd PyQt-x11-gpl-4.9.4
python configure.py --confirm-license
make
sudo make install
cd ..
cd qt-travis-test
cd ..
curl -O http://thomasmansencal.com/Sharing/ThirdParty/Riverbank/sip-4.13.3/sip-4.13.3.tar.gz
tar -xvf sip-4.13.3.tar.gz
cd sip-4.13.3
python configure.py
make
sudo make install
cd ..
curl -O http://thomasmansencal.com/Sharing/ThirdParty/Riverbank/PyQt%204.9.4/PyQt-x11-gpl-4.9.4.tar.gz
tar -xvf PyQt-x11-gpl-4.9.4.tar.gz
cd PyQt-x11-gpl-4.9.4
python configure.py --confirm-license
make
sudo make install
cd ..
cd qt-travis-test
