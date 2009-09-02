# build6x usage: define to 1 to build for RHL6.x.  Don't define at all for others.
%{?build6x:%define kerberos 0}
%{?build6x:%define nls 0}
%{?build6x:%define ssl 0}
%{?build6x:%define tcldevel 0}
#work around the undefined or defined to 1 build 6x interaction with the pam stuff
%{!?build6x:%define non6xpamdeps 1}
%{?build6x:%define non6xpamdeps 0}
#build7x, build8, and build9 similar
%{?build8:%define build89 1}
%{?build9:%define build89 1}
%{?build7x:%define kerbdir /usr/kerberos}
%{?build7x:%define tcldevel 0}
%{?build89:%define kerbdir /usr/kerberos}
%{?build8:%define tcldevel 0}
%{?buildrhel3:%define kerbdir /usr/kerberos}

%{!?tcldevel:%define tcldevel 1} 
%{!?kerbdir:%define kerbdir "/usr"} 
%{!?aconfver:%define aconfver autoconf}

%define beta 0

%{?beta:%define __os_install_post /usr/lib/rpm/brp-compress}

%{!?tcl:%define tcl 1}
%{!?tkpkg:%define tkpkg 0}
%{!?jdbc:%define jdbc 1}
%{!?test:%define test 1}
%{!?python:%define python 1}
%{!?pltcl:%define pltcl 1}
%{!?plperl:%define plperl 1}
%{!?pls:%define pls 1}
%{!?ssl:%define ssl 1}
%{!?kerberos:%define kerberos 1}
%{!?nls:%define nls 1}
%{!?pam:%define pam 1}
%{!?pgfts:%define pgfts 1}

# Python major version.
%{expand: %%define pyver %(python -c 'import sys;print(sys.version[0:3])')}
%{expand: %%define pynextver %(python -c 'import sys;print(float(sys.version[0:3])+0.1)')}

Summary: PostgreSQL client programs and libraries
Name: postgresql
Version: 7.4.26

# Conventions for PostgreSQL Global Development Group RPM releases:

# Official PostgreSQL Development Group RPMS have a PGDG after the release number.
# Integer releases are stable -- 0.1.x releases are Pre-releases, and x.y are
# test releases.

# Pre-releases are those that are built from CVS snapshots or pre-release
# tarballs from postgresql.org.  Official beta releases are not 
# considered pre-releases, nor are release candidates, as their beta or
# release candidate status is reflected in the version of the tarball. Pre-
# releases' versions do not change -- the pre-release tarball of 7.0.3, for
# example, has the same tarball version as the final official release of 7.0.3:
# but the tarball is different.

# Test releases are where PostgreSQL itself is not in beta, but certain parts of
# the RPM packaging (such as the spec file, the initscript, etc) are in beta.

# Pre-release RPM's should not be put up on the public ftp.postgresql.org server
# -- only test releases or full releases should be.

Release: 1PGDG%{?dist}
License: BSD
Group: Applications/Databases
Source0: ftp://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.bz2
Source3: postgresql.init
Source5: ftp://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.bz2.md5
Source6: README.rpm-dist
Source8: http://jdbc.postgresql.org/download/pg74.216.jdbc1.jar
Source9: http://jdbc.postgresql.org/download/pg74.216.jdbc2.jar
Source10: http://jdbc.postgresql.org/download/pg74.216.jdbc2ee.jar
Source11: http://jdbc.postgresql.org/download/pg74.216.jdbc3.jar
Source12: http://www.postgresql.org/files/documentation/pdf/7.4/postgresql-7.4.2-A4.pdf
Source15: postgresql-bashprofile
Source16: filter-requires-perl-Pg.sh
Source18: ftp://ftp.pygresql.org/pub/distrib/PyGreSQL-3.8.1.tgz
Patch1: rpm-pgsql-7.4.patch
Patch2: rpm-multilib-7.4.patch
Patch3: postgresql-7.4-tighten.patch
Patch4: postgresql-7.4-getppid.patch
Patch5: postgresql-7.4-plperl.patch
Patch6: postgresql-7.4-src-tutorial.patch
Patch7: postgresql-7.3.4-s390-pic.patch
Patch8: postgresql-7.4-com_err.patch
Patch10: postgresql-7.4-strerror_configure.patch
Patch12: postgresql-7.4-removeautoconfcheck.patch

Buildrequires: perl glibc-devel bison flex
Requires: /sbin/ldconfig initscripts
%if %python
BuildRequires: python-devel
%endif
%if %tcl
BuildRequires: tcl
%if %tcldevel
Buildrequires: tcl-devel
%endif
%endif
%if %tkpkg
BuildRequires: tk
%endif
BuildRequires: readline-devel
BuildRequires: zlib-devel >= 1.0.4
%if %ssl
BuildRequires: openssl-devel
%endif
%if %kerberos
BuildRequires: krb5-devel
BuildRequires: e2fsprogs-devel
%endif
%if %nls
BuildRequires: gettext >= 0.10.35
%endif

%if %pam
%if %non6xpamdeps
BuildRequires: pam-devel
%endif
%endif

Url: http://www.postgresql.org/ 

Obsoletes: postgresql-clients
Obsoletes: postgresql-perl
Obsoletes: postgresql-tk

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# This is the PostgreSQL Global Development Group Official RPMset spec file,
# or a derivative thereof.
# Copyright 2003-2009 Lamar Owen <lowen@pari.edu> <lamar.owen@wgcr.org>
# and others listed.

# Major Contributors:
# ---------------
# Lamar Owen
# Trond Eivind Glomsrd <teg@redhat.com>
# Thomas Lockhart
# Reinhard Max
# Karl DeBisschop
# Peter Eisentraut
# Joe Conway
# Andrew Overholt
# David Jee
# Kaj J. Niemi
# Sander Steffann
# Tom Lane
# and others in the Changelog....

# This spec file and ancilliary files are licensed in accordance with 
# The PostgreSQL license.

# On top of this file you can find the default build package list macros.  These can be overridden by defining
# on the rpm command line:
# rpm --define 'packagename 1' .... to force the package to build.
# rpm --define 'packagename 0' .... to force the package NOT to build.
# The base package, the lib package, the devel package, and the server package always get built.


%description
PostgreSQL is an advanced Object-Relational database management system
(DBMS) that supports almost all SQL constructs (including
transactions, subselects and user-defined types and functions). The
postgresql package includes the client programs and libraries that
you'll need to access a PostgreSQL DBMS server.  These PostgreSQL
client programs are programs that directly manipulate the internal
structure of PostgreSQL databases on a PostgreSQL server. These client
programs can be located on the same machine with the PostgreSQL
server, or may be on a remote machine which accesses a PostgreSQL
server over a network connection. This package contains the docs
in HTML for the whole package, as well as command-line utilities for
managing PostgreSQL databases on a PostgreSQL server. 

If you want to manipulate a PostgreSQL database on a remote PostgreSQL
server, you need this package. You also need to install this package
if you're installing the postgresql-server package.

%package libs
Summary: The shared libraries required for any PostgreSQL clients.
Group: Applications/Databases
Provides: libpq.so

%description libs
The postgresql-libs package provides the essential shared libraries for any 
PostgreSQL client program or interface. You will need to install this package
to use any other PostgreSQL package or any clients that need to connect to a
PostgreSQL server.

%package server
Summary: The programs needed to create and run a PostgreSQL server.
Group: Applications/Databases
Requires: /usr/sbin/useradd /sbin/chkconfig 
Requires: postgresql = %{version} libpq.so
Conflicts: postgresql < 7.4

%description server
The postgresql-server package includes the programs needed to create
and run a PostgreSQL server, which will in turn allow you to create
and maintain PostgreSQL databases.  PostgreSQL is an advanced
Object-Relational database management system (DBMS) that supports
almost all SQL constructs (including transactions, subselects and
user-defined types and functions). You should install
postgresql-server if you want to create and maintain your own
PostgreSQL databases and/or your own PostgreSQL server. You also need
to install the postgresql package.


%package docs
Summary: Extra documentation for PostgreSQL
Group: Applications/Databases
%description docs
The postgresql-docs package includes the SGML source for the documentation
as well as the documentation in PDF format and some extra documentation.
Install this package if you want to help with the PostgreSQL documentation
project, or if you want to generate printed documentation.

%package contrib
Summary: Contributed source and binaries distributed with PostgreSQL
Group: Applications/Databases
Requires: postgresql = %{version}
%description contrib
The postgresql-contrib package contains contributed packages that are
included in the PostgreSQL distribution.


%package devel
Summary: PostgreSQL development header files and libraries
Group: Development/Libraries
Requires: postgresql-libs = %{version}

%description devel
The postgresql-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with a PostgreSQL database management server and the ecpg Embedded C
Postgres preprocessor. You need to install this package if you want to
develop applications which will interact with a PostgreSQL server. If
you're installing postgresql-server, you need to install this
package.

#------------
%if %pls
%package pl
Summary: The PL procedural languages for PostgreSQL.
Group: Applications/Databases
Requires: postgresql = %{version}
Requires: postgresql-server = %{version}

%description pl
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-pl package contains the the PL/Perl, PL/Tcl, and PL/Python
procedural languages for the backend.  PL/Pgsql is part of the core server package.
%endif

#------------
%if %tcl
%package tcl
Summary: A Tcl client library for PostgreSQL.
Group: Applications/Databases
Requires: tcl >= 8.0

%description tcl
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-tcl package contains the libpgtcl client library,
the pg-enhanced pgtclsh,and the pg-enhanced tksh, if so configured at buildtime.
%endif

#------------
%if %python
%package python
Summary: Development module for Python code to access a PostgreSQL DB.
Group: Applications/Databases
Requires: python mx
Conflicts: python < %pyver, python >= %pynextver


%description python
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-python package includes a module for
developers to use when writing Python code for accessing a PostgreSQL
database.
%endif

#----------
%if %jdbc
%package jdbc
Summary: Files needed for Java programs to access a PostgreSQL database.
Group: Applications/Databases

%description jdbc
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-jdbc package includes the .jar file needed for
Java programs to access a PostgreSQL database.
%endif

#------------
%if %test
%package test
Summary: The test suite distributed with PostgreSQL.
Group: Applications/Databases
Requires: postgresql = %{version}
Requires: postgresql-server = %{version}

%description test
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-test package includes the sources and pre-built
binaries of various tests for the PostgreSQL database management
system, including regression tests and benchmarks.
%endif

%define __perl_requires %{SOURCE16}

%prep
%setup -q 
pushd doc
tar zxf postgres.tar.gz
popd
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch10 -p1
%patch12 -p1

#call autoconf 2.53 or greater
%aconfver

pushd doc
tar -zcf postgres.tar.gz *.html stylesheet.css
rm -f *.html stylesheet.css
popd

cp -p %{SOURCE12} .

%if %python
   tar xzf %{SOURCE18}
   PYGRESQLDIR=`basename %{SOURCE18} .tgz`
   mv $PYGRESQLDIR PyGreSQL
 # Some versions of PyGreSQL.tgz contain wrong permissions for docs files
   chmod 644 PyGreSQL/docs/*.txt 
   chmod 755 PyGreSQL/tutorial PyGreSQL/tutorial/*.py

%endif

%build

CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS
%if %kerberos
CPPFLAGS="${CPPFLAGS} -I%{_includedir}/et" ; export CPPFLAGS
CFLAGS="${CFLAGS} -I%{_includedir}/et" ; export CFLAGS
%endif

# Strip out -ffast-math from CFLAGS....

CFLAGS=`echo $CFLAGS|xargs -n 1|grep -v ffast-math|xargs -n 100`
export LIBNAME=%{_lib}
%configure --disable-rpath \
%if %beta
	--enable-debug \
	--enable-cassert \
%endif
%if %plperl
	--with-perl \
%endif
%if %tcl
	--with-tcl \
	--with-tclconfig=%{_libdir} \
%endif
%if %tkpkg
	--with-tkconfig=%{_libdir} \
%else
	--without-tk \
%endif
%if %python
	--with-python \
%endif
%if %ssl
	--with-openssl \
%endif
%if %pam
	--with-pam \
%endif
%if %kerberos
	--with-krb5=%kerbdir \
	--with-includes=%{_includedir}/et \
%endif
%if %nls
	--enable-nls \
%endif
%if %pgfts
	--enable-thread-safety \
%endif
	--sysconfdir=/etc/sysconfig/pgsql \
	--datadir=/usr/share/pgsql \
	--with-docdir=%{_docdir}

make all
make -C contrib all

%if %test
	pushd src/test
	make all
	popd
%endif

%if %python
   PYTHON=/usr/bin/python
   python_version=`${PYTHON} -c "import sys; print sys.version[:3]"`
   python_prefix=`${PYTHON} -c "import sys; print sys.prefix"`
   python_includespec="-I${python_prefix}/include/python${python_version}"

   pushd PyGreSQL

   gcc $CFLAGS -fpic -shared -o _pgmodule.so ${python_includespec} -I../src/interfaces/libpq -I../src/include -I%{kerbdir}/include -L../src/interfaces/libpq -lpq pgmodule.c

   popd
%endif

%install
rm -rf %{buildroot}

make DESTDIR=%{buildroot} install
make -C contrib DESTDIR=%{buildroot} install

# install dev headers.

make DESTDIR=%{buildroot} install-all-headers

# copy over Makefile.global to the include dir....
install -m755 src/Makefile.global %{buildroot}/usr/include/pgsql

%if %jdbc
	# Java/JDBC
	# Red Hat's standard place to put jarfiles is /usr/share/java

	# JDBC jars 
	install -d %{buildroot}/usr/share/java
	install -m 755 %{SOURCE8} %{buildroot}/usr/share/java
	install -m 755 %{SOURCE9} %{buildroot}/usr/share/java
	install -m 755 %{SOURCE10} %{buildroot}/usr/share/java
	install -m 755 %{SOURCE11} %{buildroot}/usr/share/java

%endif

if [ -d /etc/rc.d/init.d ]
then
	install -d %{buildroot}/etc/rc.d/init.d
	sed 's/^PGVERSION=.*$/PGVERSION=%{version}/' <%{SOURCE3} > postgresql.init
	install -m 755 postgresql.init %{buildroot}/etc/rc.d/init.d/postgresql
fi


# PGDATA needs removal of group and world permissions due to pg_pwd hole.
install -d -m 700 %{buildroot}/var/lib/pgsql/data

# backups of data go here...
install -d -m 700 %{buildroot}/var/lib/pgsql/backups

# postgres' .bash_profile
install -m 644 %{SOURCE15} %{buildroot}/var/lib/pgsql/.bash_profile

# Create the multiple postmaster startup directory
install -d -m 700 %{buildroot}/etc/sysconfig/pgsql


%if %test
	# tests. There are many files included here that are unnecessary, but include
	# them anyway for completeness.
	mkdir -p %{buildroot}/usr/lib/pgsql/test
	cp -a src/test/regress %{buildroot}/usr/lib/pgsql/test
	install -m 0755 contrib/spi/refint.so %{buildroot}/usr/lib/pgsql/test/regress
	install -m 0755 contrib/spi/autoinc.so %{buildroot}/usr/lib/pgsql/test/regress
	pushd  %{buildroot}/usr/lib/pgsql/test/regress/
	strip *.so
	popd
%endif

# Fix some more documentation
# gzip doc/internals.ps
cp %{SOURCE6} README.rpm-dist
mv %{buildroot}%{_docdir}/postgresql/html doc
rm -rf %{buildroot}%{_docdir}/postgresql
%if %tkpkg
%else
rm -rf %{buildroot}%{_mandir}/man1/pgtksh.*
%endif
%if %tcl
%else
rm -rf %{buildroot}%{_mandir}/man1/pgtclsh.*
%endif

%if %python
   pushd PyGreSQL
   install -m 0755 -d %{buildroot}%{_libdir}/python%{pyver}/site-packages
   install -m 0755 _pgmodule.so %{buildroot}%{_libdir}/python%{pyver}/site-packages
   install -m 0755 pg.py %{buildroot}%{_libdir}/python%{pyver}/site-packages
   install -m 0755 pgdb.py %{buildroot}%{_libdir}/python%{pyver}/site-packages
   popd
%endif

%find_lang libpq
%find_lang pg_dump
%find_lang postgres
%find_lang psql
%find_lang pg_resetxlog
%find_lang pg_controldata
%find_lang pgscripts

cat libpq.lang > libpq.lst
cat psql.lang pg_dump.lang pgscripts.lang > main.lst
cat postgres.lang pg_resetxlog.lang pg_controldata.lang > server.lst

%post libs -p /sbin/ldconfig 
%postun libs -p /sbin/ldconfig 

%pre server
groupadd -g 26 -o -r postgres >/dev/null 2>&1 || :
useradd -M -n -g postgres -o -r -d /var/lib/pgsql -s /bin/bash \
	-c "PostgreSQL Server" -u 26 postgres >/dev/null 2>&1 || :
touch /var/log/pgsql
chown postgres:postgres /var/log/pgsql
chmod 0700 /var/log/pgsql

%post server
chkconfig --add postgresql
/sbin/ldconfig

%preun server
if [ $1 = 0 ] ; then
	/sbin/service postgresql condstop >/dev/null 2>&1
	chkconfig --del postgresql
fi

%postun server
/sbin/ldconfig 
if [ $1 = 0 ] ; then
	userdel postgres >/dev/null 2>&1 || :
	groupdel postgres >/dev/null 2>&1 || : 
fi

%if %tcl
%post -p /sbin/ldconfig   tcl
%postun -p /sbin/ldconfig   tcl
%endif

%if %pls
%post -p /sbin/ldconfig   pl
%postun -p /sbin/ldconfig   pl
%endif

%if %test
%post test
chown -R postgres:postgres /usr/share/pgsql/test >/dev/null 2>&1 || :
%endif

%clean
rm -rf %{buildroot}

# FILES section.

%files -f main.lst
%defattr(-,root,root)
%doc doc/FAQ doc/KNOWN_BUGS doc/MISSING_FEATURES doc/README* 
%doc COPYRIGHT README HISTORY doc/bug.template
%doc README.rpm-dist
%doc doc/html
%{_bindir}/clusterdb
%{_bindir}/createdb
%{_bindir}/createlang
%{_bindir}/createuser
%{_bindir}/dropdb
%{_bindir}/droplang
%{_bindir}/dropuser
%{_bindir}/pg_dump
%{_bindir}/pg_dumpall
%{_bindir}/pg_encoding
%{_bindir}/pg_id
%{_bindir}/pg_restore
%{_bindir}/psql
%{_bindir}/vacuumdb
%{_mandir}/man1/clusterdb.*
%{_mandir}/man1/createdb.*
%{_mandir}/man1/createlang.*
%{_mandir}/man1/createuser.*
%{_mandir}/man1/dropdb.*
%{_mandir}/man1/droplang.*
%{_mandir}/man1/dropuser.*
%{_mandir}/man1/pg_dump.*
%{_mandir}/man1/pg_dumpall.*
%{_mandir}/man1/pg_restore.*
%{_mandir}/man1/psql.*
%{_mandir}/man1/vacuumdb.*
%{_mandir}/man7/*

%files docs
%defattr(-,root,root)
%doc doc/src/*
%doc *-A4.pdf
%doc src/tutorial

%files contrib
%defattr(-,root,root)
%{_libdir}/pgsql/_int.so
%{_libdir}/pgsql/autoinc.so
%{_libdir}/pgsql/btree_gist.so
%{_libdir}/pgsql/chkpass.so
%{_libdir}/pgsql/cube.so
%{_libdir}/pgsql/dblink.so
%{_libdir}/pgsql/dbsize.so
%{_libdir}/pgsql/earthdistance.so
%{_libdir}/pgsql/fti.so
%{_libdir}/pgsql/fuzzystrmatch.so
%{_libdir}/pgsql/insert_username.so
%{_libdir}/pgsql/int_aggregate.so
%{_libdir}/pgsql/isbn_issn.so
%{_libdir}/pgsql/lo.so
%{_libdir}/pgsql/ltree.so
%{_libdir}/pgsql/misc_utils.so
%{_libdir}/pgsql/moddatetime.so
%{_libdir}/pgsql/noup.so
%{_libdir}/pgsql/pending.so
%{_libdir}/pgsql/pgcrypto.so
%{_libdir}/pgsql/pgstattuple.so
%{_libdir}/pgsql/refint.so
%{_libdir}/pgsql/rserv.so
%{_libdir}/pgsql/rtree_gist.so
%{_libdir}/pgsql/seg.so
%{_libdir}/pgsql/string_io.so
%{_libdir}/pgsql/tablefunc.so
%{_libdir}/pgsql/timetravel.so
%{_libdir}/pgsql/tsearch.so
%{_libdir}/pgsql/tsearch2.so
%{_libdir}/pgsql/user_locks.so
%{_datadir}/pgsql/contrib/
%{_bindir}/dbf2pg
%{_bindir}/findoidjoins
%{_bindir}/make_oidjoins_check
%{_bindir}/fti.pl
%{_bindir}/oid2name
%{_bindir}/pg_dumplo
%{_bindir}/pg_logger
%{_bindir}/pgbench
%{_bindir}/RservTest
%{_bindir}/MasterInit
%{_bindir}/MasterAddTable
%{_bindir}/Replicate
%{_bindir}/MasterSync
%{_bindir}/CleanLog
%{_bindir}/SlaveInit
%{_bindir}/SlaveAddTable
%{_bindir}/GetSyncID
%{_bindir}/PrepareSnapshot
%{_bindir}/ApplySnapshot
%{_bindir}/InitRservTest
%{_bindir}/vacuumlo
%{_bindir}/pg_autovacuum
%doc contrib/*/README.* contrib/spi/*.example

%files libs -f libpq.lang
%defattr(-,root,root)
%{_libdir}/libpq.so.*
%{_libdir}/libecpg.so.*
%{_libdir}/libpgtypes.so.*
%{_libdir}/libecpg_compat.so.*

%files server -f server.lst
%defattr(-,root,root)
/etc/rc.d/init.d/postgresql
%attr (755,root,root) %dir /etc/sysconfig/pgsql
%{_bindir}/initdb
%{_bindir}/initlocation
%{_bindir}/ipcclean
%{_bindir}/pg_controldata
%{_bindir}/pg_ctl
%{_bindir}/pg_resetxlog
%{_bindir}/postgres
%{_bindir}/postmaster
%{_mandir}/man1/initdb.*
%{_mandir}/man1/initlocation.*
%{_mandir}/man1/ipcclean.*
%{_mandir}/man1/pg_controldata.*
%{_mandir}/man1/pg_ctl.*
%{_mandir}/man1/pg_resetxlog.*
%{_mandir}/man1/postgres.*
%{_mandir}/man1/postmaster.*
%{_datadir}/pgsql/postgres.bki
%{_datadir}/pgsql/postgres.description
%{_datadir}/pgsql/*.sample
%{_libdir}/pgsql/plpgsql.so
%dir %{_libdir}/pgsql
%dir %{_datadir}/pgsql
%attr(700,postgres,postgres) %dir /var/lib/pgsql
%attr(700,postgres,postgres) %dir /var/lib/pgsql/data
%attr(700,postgres,postgres) %dir /var/lib/pgsql/backups
%attr(644,postgres,postgres) %config(noreplace) /var/lib/pgsql/.bash_profile
%{_libdir}/pgsql/*_and_*.so
%{_datadir}/pgsql/conversion_create.sql
%{_datadir}/pgsql/information_schema.sql
%{_datadir}/pgsql/sql_features.txt

%files devel
%defattr(-,root,root)
/usr/include/*
%{_bindir}/ecpg
%{_bindir}/pg_config
%{_libdir}/libpq.so
%{_libdir}/libecpg.so
%{_libdir}/libpq.a
%{_libdir}/libecpg.a
%if %tcl
%{_libdir}/libpgtcl.a
%endif
%{_libdir}/libecpg_compat.so
%{_libdir}/libecpg_compat.a
%{_libdir}/libpgtypes.so
%{_libdir}/libpgtypes.a
%{_mandir}/man1/ecpg.*
%{_mandir}/man1/pg_config.*

%if %tcl
%files tcl
%defattr(-,root,root)
%attr(755,root,root) %{_libdir}/libpgtcl.so.*
# libpgtcl.so is not in devel because Tcl scripts may load it by that name.
%{_libdir}/libpgtcl.so
%{_bindir}/pgtclsh
%{_mandir}/man1/pgtclsh.*
%endif
%if %tkpkg
%{_bindir}/pgtksh
%{_mandir}/man1/pgtksh.*
%endif

%if %pls
%files pl
%defattr(-,root,root)
%if %plperl
%{_libdir}/pgsql/plperl.so
%endif
%if %pltcl
%{_libdir}/pgsql/pltcl.so
%{_bindir}/pltcl_delmod
%{_bindir}/pltcl_listmod
%{_bindir}/pltcl_loadmod
%{_datadir}/pgsql/unknown.pltcl
%endif
%if %python
%{_libdir}/pgsql/plpython.so
%endif
%endif

%if %python
%files python
%defattr(-,root,root)
%doc PyGreSQL/tutorial PyGreSQL/docs/*.txt
%{_libdir}/python%{pyver}/site-packages/_pgmodule.so
%{_libdir}/python%{pyver}/site-packages/*.py
%endif

%if %jdbc
%files jdbc
%defattr(-,root,root)
%{_datadir}/java/pg74.216.jdbc1.jar
%{_datadir}/java/pg74.216.jdbc2.jar
%{_datadir}/java/pg74.216.jdbc2ee.jar
%{_datadir}/java/pg74.216.jdbc3.jar
%endif

%if %test
%files test
%defattr(-,postgres,postgres)
%attr(-,postgres,postgres) /usr/lib/pgsql/test/*
%attr(-,postgres,postgres) %dir /usr/lib/pgsql/test
%endif

%changelog
* Thu Sep 3 2009 Devrim GUNDUZ <devrim@commandprompt.com> 7.4.26-1PGDG
- Update to 7.4.26

* Fri Mar 13 2009 Devrim GUNDUZ <devrim@commandprompt.com> 7.4.25-1PGDG
- Update to 7.4.25

* Fri Jan 30 2009 Devrim GUNDUZ <devrim@commandprompt.com> 7.4.24-1PGDG
- Update to 7.4.24

* Sat Nov 1 2008 Devrim GUNDUZ <devrim@commandprompt.com> 7.4.23-1PGDG
- Update to 7.4.23

* Fri Sep 19 2008 Devrim GUNDUZ <devrim@commandprompt.com> 7.4.22-1PGDG
- Update to 7.4.22

* Mon Jun 9 2008 Devrim GUNDUZ <devrim@commandprompt.com> 7.4.21-1PGDG
- Update to 7.4.21 (7.4.20 was skipped by upstream) 

* Thu Jan 3 2008 Devrim GUNDUZ <devrim@commandprompt.com> 7.4.19-1PGDG
- Update to 7.4.19, which also includes security fixes for CVE-2007-4769,
  CVE-2007-4772, CVE-2007-6067, CVE-2007-6600, CVE-2007-6601
- Update copyright date
- Added a patch to disable autoconf version checks in configure.in 

* Wed Oct 10 2007 Devrim GUNDUZ <devrim@commandprompt.com> 7.4.18-2PGDG
- Rebuilt

* Sat Sep 15 2007 Devrim GUNDUZ <devrim@commandprompt.com> 7.4.18-1PGDG
- Update to 7.4.18

* Sat Apr 21 2007 Devrim GUNDUZ <devrim@commandprompt.com> 7.4.17-1PGDG
- Update to 7.4.17

* Sat Feb 3 2007 Devrim GUNDUZ <devrim@commandprompt.com> 7.4.16-1PGDG
- Update to 7.4.16

* Wed Jan 3 2007 Devrim GUNDUZ <devrim@commandprompt.com> 7.4.15-1PGDG
- Update to 7.4.15
- Update buildroot tag
- Use only major version number in patches.

* Fri Oct 06 2006 Devrim GUNDUZ <devrim@commandprompt.com> 7.4.14-1PGDG
- 7.4.14
- Fix some of the rpmlint warnings and errors
- Fix plperl patch name
- fix release number
- Change rpmbuildroot macro

* Tue Jun 06 2006 Devrim GUNDUZ <devrim@commandprompt.com> 7.4.13-2PGDG
- re-fix PyGreSQL filenames
- Updated PyGreSQL from 3.8 to 3.8.1

* Mon May 22 2006 Devrim GUNDUZ <devrim@commandprompt.com> 7.4.13-1PGDG
- Fix PyGreSQL filenames
- Update to 7.4.13

* Sun Feb 19 2006 Devrim GUNDUZ <devrim@commandprompt.com> 7.4.12-2PGDG
- Updated PyGreSQL from 3.7 to 3.8

* Mon Feb 13 2006 Devrim Gunduz <devrim@commandprompt.com> 7.4.12-1PGDG
- Update to 7.4.12

* Mon Jan 9 2006 Devrim Gunduz <devrim@commandprompt.com> 7.4.11-1PGDG
- Update to 7.4.11

* Mon Dec 10 2005 Devrim Gunduz <devrim@commandprompt.com> 7.4.10-2PGDG
- Update PyGreSQL version to 3.7

* Mon Dec 10 2005 Devrim Gunduz <devrim@commandprompt.com> 7.4.10-1PGDG
- Upgrade to 7.4.10
- Updated JDBC jars to build 216
- Update README file
- Re-added PDF documentation
- Added a macro for RHEL 3 kerberos builds.

* Fri May 6 2005 Devrim Gunduz <devrim@gunduz.org> 7.4.8-1PGDG
- Upgrade to 7.4.8-1
- Removed postgresql-7.4.7-security.patch

* Fri Apr 22 2005 Devrim Gunduz <devrim@gunduz.org> 7.4.7-3PGDG
- Updated JDBC from build 215 to 216.
- Updated PyGreSQL version

* Fri Feb 25 2005 Sander Steffann <steffann@nederland.net>
- Merged in patches for building on x86_64 platforms

* Wed Feb 23 2005 Devrim GUNDUZ <devrim@gunduz.org> 7.4.7-2PGDG
- Repair improper error message in init script when PGVERSION doesn't match. (Tom Lane)
- Arrange for auto update of version embedded in init script. (Tom Lane)
- Patch additional buffer overruns in plpgsql (CAN-2005-0247) (Tom Lane)

* Sat Feb 5 2005 Devrim Gunduz <devrim@gunduz.org>
- 7.4.7-1PGDG
- Updated PyGreSQL version

* Mon Oct 25 2004 Devrim Gunduz <devrim@gunduz.org>
- 7.4.6-2PGDG
- Updated kerbdir
- Updated PyGreSQL from 3.4 to 3.5
- Updated doc files for PyGreSQL
- Modified if-endif lines for tcl&tcldevel Requires lines (per Red Hat RPMS)
- Applied getppid.patch as patch #4 (per Red Hat RPMS)
- Updated spec file to correct permissions for PyGreSQL permissions (per Red Hat RPMS)
- Updated preun and postun server scripts, per Red Hat RPMS

* Sat Oct 23 2004 Devrim Gunduz <devrim@gunduz.org>
- 7.4.6-1PGDG
- Update JDBC jars

* Thu Sep 9 2004 Devrim Gunduz <devrim@gunduz.org>
- 7.4.5-2PGDG
- Added tcl support.

* Wed Aug 18 2004 Devrim Gunduz <devrim@gunduz.org>
- 7.4.5-1PGDG

* Tue Aug 17 2004 Devrim Gunduz <devrim@gunduz.org>
- 7.4.4-1PGDG

* Thu Jun 24 2004 Devrim Gunduz <devrim@gunduz.org>
- Updated kerberos define line for rhel3

* Fri Jun 18 2004 David Fetter <david@fetter.org>
- bumped .spec file version

* Wed Jun 16 2004 Devrim Gunduz <devrim@gunduz.org>
- 7.4.3-1PGDG
- Update JDBC jars

* Mon Mar 08 2004 Lamar Owen <lowen@pari.edu>
- 7.4.2-1PGDG
- Merge FC2 changes.
- Proper attrs for /etc/sysconfig/pgsql
- tcl-devel package is not a buildreq for RH8 and before

* Wed Feb 25 2004 Tom Lane <tgl@redhat.com>
- Update to PostgreSQL 7.4.1.
- Rebuilt

* Tue Feb 24 2004 Tom Lane <tgl@redhat.com>
- Fix chown syntax in postgresql.init also.
- Rebuilt

* Mon Feb 23 2004 Tim Waugh <twaugh@redhat.com>
- Use ':' instead of '.' as separator for chown.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jan 9 2004 Lamar Owen <lowen@pari.edu>
- 7.4.1-1PGDG
- Merge Sander Steffann's changes up to 7.4-0.5PGDG
- Proper 7.4.1 JDBC jars this time.
- Patch for no pl/python from Alvaro

* Fri Dec 05 2003 David Jee <djee@redhat.com> 7.4-5
- Rebuild for Perl 5.8.2.

* Mon Dec 01 2003 David Jee <djee@redhat.com> 7.4-4
- Add PyGreSQL patch for deprecated column pg_type.typprtlen [Bug #111263]
- Add headers patch which moves ecpg headers to /usr/include/ecpg
  [Bug #111195]

* Fri Nov 28 2003 David Jee <djee@redhat.com> 7.4-3
- uncomment buildrequires tcl-devel

* Fri Nov 28 2003 David Jee <djee@redhat.com> 7.4-2
- rebuild

* Mon Nov 24 2003 David Jee <djee@redhat.com> 7.4-1
- initial Red Hat build
- move jars to /usr/share/java
- fix rpm-multilib patch to use sysconfig

* Fri Nov 21 2003 Lamar Owen <lowen@pari.edu> <lamar.owen@wgcr.org>
- 7.4-0.1PGDG
- Development JDBC jars in addition to the 7.3 jars; will replace the
- 7.3 jars once 7.4 official jars are released.
- Changed to use the bzip2 source to save a little size.
- Removed some commented out portions of the specfile.
- Removed the 7.3.4 PDF docs.  Will replace with 7.4 PDF's once they
- are ready.

* Tue Nov 18 2003 Kaj J. Niemi <kajtzu@fi.basen.net> 7.4-0.1
- 7.4
- Fixed Patch #1 (now rpm-pgsql-7.4.patch)
- Fixed Patch #2 (now rpm-multilib-7.4.patch):
- Patch #4 is unnecessary (upstream)
- Fixed Patch #6 (now postgresql-7.4-src-tutorial.patch)
- Added Patch #8 (postgresql-7.4-com_err.patch) as com_err()
  is provided by e2fsprogs and CPPFLAGS gets lost somewhere
  inside configure (bad macro?)
- No 7.4 PDF docs available yet (Source #17)
- PyGreSQL is separated from the upstream distribution but
  we include it as usual (Source #18)
- Default to compiling libpq and ECPG as fully thread-safe

- 7.4 Origin.  See previous spec files for previous history. Adapted
- from Red Hat and PGDG's 7.3.4 RPM, directly descended from 
- postgresql-7.3.4-2 as shipped in Fedora Core 1.
