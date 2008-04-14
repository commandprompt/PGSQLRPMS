#!/bin/bash
#  
# Upload under ~postgres, chmod 700.
#  

rm -rf ~postgres/rpm/BUILD/*
rm -rf ~postgres/rpm/SOURCES/*
rsync -ave ssh --delete root@192.168.1.44:/media/disk/RPMS/srpms/8.3/common/* /var/lib/pgsql/rpm/SRPMS
rsync -ave ssh --delete root@192.168.1.44:/media/disk/RPMS/srpms/8.3/F-8/* /var/lib/pgsql/rpm/SRPMS

