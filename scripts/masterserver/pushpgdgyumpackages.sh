#!/bin/bash

# This scripts pushes binary RPMS to yum.pgsqlrpms.org. 
# We first create repository related files, and then rsync them.
# You don't *need to* remove old versions everytime, yum will
# pick up the latest versions for users.

# This is the default root for the RPMs:
cd /media/disk/RPMS

for i in `ls -d 7* 8*`
# If you want to push a specific version, use it like below:
#for i in `ls -d 8.3`
do
	cd $i
	for j in `ls -d *`
	do
		cd $j
		for k in `ls -d *`
		do
			cd $k
			echo "Working on $i - $j - $k"
			# Create / update repo files and web interface:
			createrepo -d --update . && repoview -u "http://yum.pgsqlrpms.org/$i/$j/$k/" -o repoview/ -t "PostgreSQL PGDG RPMs" .
			# rsync files to the relevant directory:
			rsync -ave ssh  --delete /media/disk/RPMS/$i/$j/$k  pgsqlrpms@yum.pgsqlrpms.org:/home/community/pgsqlrpms/yumrepo/$i/$j/
			cd ..
		done
		cd ..
	done
	cd ..
done
