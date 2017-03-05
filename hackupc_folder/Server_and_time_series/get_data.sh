#!/usr/bin/env bash
URL_DATA='http://www.ree.es/sites/default/files/simel/demd/'$1'.gz'
FILE_NAME=$1'.gz'
wget $URL_DATA
rm -f temp.txt
zcat $FILE_NAME > temp.txt
awk -F';' 'NR>1 {print $6}' >> series.txt
rm -f $FIlE_NAME
