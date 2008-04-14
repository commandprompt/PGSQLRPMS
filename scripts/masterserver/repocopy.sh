#!/bin/bash
REPORPMPATH=/var/lib/pgsql/rpm/RPMS/noarch
DESTPATH=/media/disk/RPMS/reporpms
RPMPATH=/media/disk/RPMS

cp $REPORPMPATH/*7.3* $DESTPATH/7.3/
cp $REPORPMPATH/*7.4* $DESTPATH/7.4/
cp $REPORPMPATH/*8.0* $DESTPATH/8.0/
cp $REPORPMPATH/*8.1* $DESTPATH/8.1/
cp $REPORPMPATH/*8.2* $DESTPATH/8.2/
cp $REPORPMPATH/*8.3* $DESTPATH/8.3/

# 7.3

for i in `find $RPMPATH/7.3/fedora/ -iname "pgdg*.rpm"`
do
 rm -f $i
 for k in `ls -d $RPMPATH/7.3/fedora/*`
 do
  cp $REPORPMPATH/pgdg-fedora-7.3* $k
  done
done

for i in `find $RPMPATH/7.3/redhat/ -iname "pgdg*.rpm"`
do
 rm -f $i
 for k in `ls -d $RPMPATH/7.3/redhat/*`
 do
  cp $REPORPMPATH/pgdg-redhat-7.3* $k
  cp $REPORPMPATH/pgdg-centos-7.3* $k
  done
done

# 7.4

for i in `find $RPMPATH/7.4/fedora/ -iname "pgdg*.rpm"`
do
 rm -f $i
 for k in `ls -d $RPMPATH/7.4/fedora/*`
 do
  cp $REPORPMPATH/pgdg-fedora-7.4* $k
  done
done

for i in `find $RPMPATH/7.4/redhat/ -iname "pgdg*.rpm"`
do
 rm -f $i
 for k in `ls -d $RPMPATH/7.4/redhat/*`
 do
  cp $REPORPMPATH/pgdg-redhat-7.4* $k
  cp $REPORPMPATH/pgdg-centos-7.4* $k
  done
done

# 8.0

for i in `find $RPMPATH/8.0/fedora/ -iname "pgdg*.rpm"`
do
 rm -f $i
 for k in `ls -d $RPMPATH/8.0/fedora/*`
 do
  cp $REPORPMPATH/pgdg-fedora-8.0* $k
  done
done

for i in `find $RPMPATH/8.0/redhat/ -iname "pgdg*.rpm"`
do
 rm -f $i
 for k in `ls -d $RPMPATH/8.0/redhat/*`
 do
  cp $REPORPMPATH/pgdg-redhat-8.0* $k
  cp $REPORPMPATH/pgdg-centos-8.0* $k
  done
done

# 8.1

for i in `find $RPMPATH/8.1/fedora/ -iname "pgdg*.rpm"`
do
 rm -f $i
 for k in `ls -d $RPMPATH/8.1/fedora/*`
 do
  cp $REPORPMPATH/pgdg-fedora-8.1* $k
  done
done

for i in `find $RPMPATH/8.1/redhat/ -iname "pgdg*.rpm"`
do
 rm -f $i
 for k in `ls -d $RPMPATH/8.1/redhat/*`
 do
  cp $REPORPMPATH/pgdg-redhat-8.1* $k
  cp $REPORPMPATH/pgdg-centos-8.1* $k
  done
done

# 8.2

for i in `find $RPMPATH/8.2/fedora/ -iname "pgdg*.rpm"`
do
 rm -f $i
 for k in `ls -d $RPMPATH/8.2/fedora/*`
 do
  cp $REPORPMPATH/pgdg-fedora-8.2* $k
  done
done

for i in `find $RPMPATH/8.2/redhat/ -iname "pgdg*.rpm"`
do
 rm -f $i
 for k in `ls -d $RPMPATH/8.2/redhat/*`
 do
  cp $REPORPMPATH/pgdg-redhat-8.2* $k
  cp $REPORPMPATH/pgdg-centos-8.2* $k
  done
done

# 8.3

for i in `find $RPMPATH/8.3/fedora/ -iname "pgdg*.rpm"`
do
 rm -f $i
 for k in `ls -d $RPMPATH/8.3/fedora/*`
 do
  cp $REPORPMPATH/pgdg-fedora-8.3* $k
  done
done

for i in `find $RPMPATH/8.3/redhat/ -iname "pgdg*.rpm"`
do
 rm -f $i
 for k in `ls -d $RPMPATH/8.3/redhat/*`
 do
  cp $REPORPMPATH/pgdg-redhat-8.3* $k
  cp $REPORPMPATH/pgdg-centos-8.3* $k
  done
done

