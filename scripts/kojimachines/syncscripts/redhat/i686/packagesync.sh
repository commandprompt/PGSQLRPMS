#!/bin/bash
#  
# Upload under ~postgres, chmod 700.
#  

rsync --stats -ave ssh --delete /var/lib/pgsql/rpm/RPMS/i686/* root@192.168.1.44:/media/disk/RPMS/8.3/redhat/rhel-5-i386/
rsync --stats -ave ssh --delete /var/lib/pgsql/rpm/RPMS/noarch/* root@192.168.1.44:/media/disk/RPMS/8.3/redhat/rhel-5-i386/
