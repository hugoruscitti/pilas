#!/bin/bash

if  [ $# -eq  1 ] ; then

    cp -r pilas/  /tmp/pilas-$1
    cd /tmp/pilas-$1/
    cd lanas 
    rm -fr .??*
    cd ../docs
    rm -fr .??*
    cd ../..
    tar cf pilas_$1.orig.tar pilas-$1
    xz pilas_$1.orig.tar
    cd pilas-$1
    dpkg-buildpackage

else
    echo " Es necesario ingresar un numero de version como argumento"    
fi
