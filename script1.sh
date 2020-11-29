#!/bin/bash
ZIPDIR=/home/chinmaya/Desktop/test/zipfol/*
DESTDIR=/home/chinmaya/Desktop/test/zipfol/

for f in $ZIPDIR
do
	unzip -d $DESTDIR $f
	rm $f
done
for f in $DESTDIR
do
	gsutil cp -r $f gs://mybucket
	rm $f
	
done

