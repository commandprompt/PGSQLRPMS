#!/bin/bash

# Script to push packages to ftp.postgresql.org

if [ ! $1 ]
then
 echo "Full version number cannot be null! Format is: 8.3.0 , etc."
 exit
fi

if [ ! $2 ]
then
 echo "Major version number cannot be null! Format is: 8.3 , etc."
 exit
fi

cd /media/disk/RPMS

for i in `ls -d $2`
do
	cd $i
	for j in `ls -d *`
	do
		cd $j
		for k in `ls -d *`
		do
			cd $k
			echo "Working on $i - $j - $k"
			scp /media/disk/RPMS/$i/$j/$k/postgresql*$1* devrim@developer.postgresql.org:/var/spool/ftp/pub/binary/v$1/linux/rpms/$j/$k
			scp compat-postgresql* devrim@developer.postgresql.org:/var/spool/ftp/pub/binary/v$1/linux/rpms/$j/$k
			cd ..
		done
		cd ..
	done
	cd ..
done
