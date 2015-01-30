HASH=309d0cadce2dc81ce110f3aea50933e81376c169
wget -N https://github.com/hugoruscitti/pilas/archive/$HASH/pilas-$HASH.tar.gz

tar xvfz pilas-$HASH.tar.gz

cd pilas-$HASH/

python setup.py build
sudo python setup.py install
