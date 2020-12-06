#!/bin/bash
ZIPDIR='./zipdataset/*'
DESTDIR='./dataset/'

for f in $ZIPDIR
do
	unzip -d $DESTDIR $f
	rm $f
done

