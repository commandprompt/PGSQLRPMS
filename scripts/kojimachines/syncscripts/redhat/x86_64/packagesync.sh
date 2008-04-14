#!/bin/bash
#  
# Upload under ~postgres, chmod 700.
#  

rsync --stats -ave ssh --delete /var/lib/pgsql/rpm/RPMS/x86_64/* root@192.168.1.44:/media/disk/RPMS/8.3/redhat/rhel-5-x86_64/
rsync --stats -ave ssh --delete /var/lib/pgsql/rpm/RPMS/noarch/* root@192.168.1.44:/media/disk/RPMS/8.3/redhat/rhel-5-x86_64/

