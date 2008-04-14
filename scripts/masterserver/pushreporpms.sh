#!/bin/bash

# This scripts copies repository RPMS. Then use regular
# package sync script.
# You don't *need to* remove old versions everytime, yum will
# pick up the latest versions for users.

# This is the default root for the RPMs:
cd /media/disk/RPMS/


for i in `ls -d 7* 8*`
# If you want to push a specifix version, use it like below:
#for i in `ls -d 8.3`
do
	cd $i
	for j in `ls -d fedora`
	do
		cd $j
		for k in `ls -d a`
		do
			cd $k
			echo "Working on $i - $j - $k"
			# Delete old repo packages
			rm -f pgdg-*
			# Now copy the new ones
			cp /media/disk/RPMS/reporpms/$i/pgdg-fedora* /media/disk/RPMS/$i/$j/$k
			cd ..
		done

		for k in `ls -d redhat`
		do
			cd $k
			echo "Working on $i - $j - $k"
			# Delete old repo packages
			rm -f pgdg-*
			# Now copy the new ones
			cp /media/disk/RPMS/reporpms/$i/pgdg-redhat* /media/disk/RPMS/$i/$j/$k
			cp /media/disk/RPMS/reporpms/$i/pgdg-centos* /media/disk/RPMS/$i/$j/$k
			cd ..
		done

		cd ..
	done
	cd ..
done
