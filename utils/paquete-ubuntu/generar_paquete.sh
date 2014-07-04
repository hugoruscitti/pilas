#!/bin/bash


VERSION=$1

echo "Creando o reiniciando el directorio 'resultado' para la version ${VERSION}"
rm -r -f resultado
mkdir resultado
cd resultado

echo "Clonando box2d"
svn checkout http://pybox2d.googlecode.com/svn/trunk/ pybox2d > box2d_clone.log
cd pybox2d
find . -type f -print0 | xargs -0 sed -i 's/sáb /sab /g'
find . -type f -print0 | xargs -0 sed -i 's/mié /mie /g'
python setup.py bdist > pybox2d_bdist.log

# El directorio 'dist' tiene el paquete binario de box2d

cd dist
tar xzf Box2D*
cd ../../

# Clonando pilas

echo "Clonando pilas"
git clone http://github.com/hugoruscitti/pilas > pilas_clone.log
cd pilas
git submodule init
git submodule update
python setup.py bdist > pilas_bdist.log
cd dist
tar xzf pilas*
cd ../..

# Mezclando version binaria de box2d con pilas

cp -r -f pybox2d/dist/usr/* pilas/dist/usr

# Generando el paquete .deb
cd pilas/dist

cp -r ../../../DEBIAN ./

mkdir -p usr/share/applications
cp ../../../desktop/pilas.desktop usr/share/applications

mkdir -p usr/local/share/pixmaps
cp ../pilas/data/pilas-64x64.png usr/local/share/pixmaps

rm pilas-*
cd ..
dpkg --build dist pilas-${VERSION}.deb
mv pilas-${VERSION}.deb ../../

cd ../../
echo "Archivos generados:"
ls *.deb
