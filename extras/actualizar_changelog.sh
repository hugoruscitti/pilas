#!/bin/bash
read -p "Vas a escribir una reseña del cambio, con 'dch' ? (s/n) " -n 1
echo
if [[ $REPLY =~ ^[YysS]$ ]]; then
    dch -i
fi
