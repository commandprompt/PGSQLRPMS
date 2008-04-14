#!/bin/bash
#
# Upload to ~postgres ; chmod 700 .

cd ~/rpm/RPMS/i686
rpm --addsign *.rpm
cd ~/rpm/RPMS/noarch
rpm --addsign *.rpm

