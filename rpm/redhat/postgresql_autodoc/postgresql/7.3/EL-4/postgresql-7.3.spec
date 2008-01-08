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
%{?build7x:%define kerbdir --with-krb5=/usr/kerberos}
%{?build7x:%define tcldevel 0}
%{?build89:%define kerbdir --with-krb5=/usr/kerberos}
%{?build8:%define tcldevel 0}

%{!?tcldevel:%define tcldevel 0}
%{!?kerbdir:%define kerbdir --with-krb5}
%{!?aconfver:%define aconfver autoconf}

%define beta 0

%{?beta:%define __os_install_post /usr/lib/rpm/brp-compress}

%{!?tcl:%define tcl 0}
%{!?tkpkg:%define tkpkg 0}
%{!?jdbc:%define jdbc 1}
%{!?test:%define test 1}
%{!?python:%define python 0}
%{!?pltcl:%define pltcl 0}
%{!?plperl:%define plperl 1}
%{!?pls:%define pls 1}
%{!?ssl:%define ssl 1}
%{!?kerberos:%define kerberos 0}
%{!?nls:%define nls 1}
%{!?pam:%define pam 1}
%{!?pgfts:%define pgfts 1}

# Python major version.
%{expand: %%define pyver %(python -c 'import sys;print(sys.version[0:3])')}
%{expand: %%define pynextver %(python -c 'import sys;print(float(sys.version[0:3])+0.1)')}


Summary: PostgreSQL client programs and libraries
Name: postgresql
Version: 7.3.21

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
Source8: http://jdbc.postgresql.org/download/pg73jdbc1.jar
Source9: http://jdbc.postgresql.org/download/pg73jdbc2.jar
Source10: http://jdbc.postgresql.org/download/pg73jdbc3.jar
Source11: http://jdbc.postgresql.org/download/pg73jdbc2ee.jar
Source15: postgresql-bashprofile
Source16: filter-requires-perl-Pg.sh
Patch1: rpm-pgsql-7.3.patch
Patch2: rpm-multilib-7.3.patch
Patch3: postgresql-7.3-tighten.patch
Patch5: postgresql-7.4-getppid.patch
Patch12: postgresql-7.3-removeautoconfcheck.patch

BuildRequires: perl glibc-devel bison flex
Requires: /sbin/ldconfig initscripts
%if %python
BuildRequires: python-devel
%endif
%if %tcl
BuildRequires: tcl
%if %tcldevel
BuildRequires: tcl-devel
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
Buildroot: %{_tmppath}/%{name}-%{version}-root

# This is the PostgreSQL Global Development Group Official RPMset spec file,
# or a derivative thereof.
# Copyright 2003-2008 Lamar Owen <lamar@postgresql.org> <lamar.owen@wgcr.org>
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
Summary: The shared libraries required for any PostgreSQL clients
Group: Applications/Databases
Provides: libpq.so.2 libpq.so.2.0 libpq.so

%description libs
The postgresql-libs package provides the essential shared libraries for any 
PostgreSQL client program or interface. You will need to install this package
to use any other PostgreSQL package or any clients that need to connect to a
PostgreSQL server.

%package server
Summary: The programs needed to create and run a PostgreSQL server
Group: Applications/Databases
Requires: /usr/sbin/useradd /sbin/chkconfig 
Requires: postgresql = %{version} libpq.so
Conflicts: postgresql < 7.3

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
as well as the documentation in other formats, and some extra documentation.
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
Summary: The PL procedural languages for PostgreSQL
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
Summary: A Tcl client library for PostgreSQL
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
Summary: Development module for Python code to access a PostgreSQL DB
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
Summary: Files needed for Java programs to access a PostgreSQL database
Group: Applications/Databases

%description jdbc
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-jdbc package includes the .jar file needed for
Java programs to access a PostgreSQL database.
%endif

#------------
%if %test
%package test
Summary: The test suite distributed with PostgreSQL
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

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch5 -p1
%patch12 -p1

%aconfver

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
	--with-openssl=/usr/include \
%endif
%if %pam
	--with-pam \
%endif
%if %kerberos
	%kerbdir \
%endif
%if %nls
	--enable-nls \
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

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
make -C contrib DESTDIR=$RPM_BUILD_ROOT install

# install dev headers.

make DESTDIR=$RPM_BUILD_ROOT install-all-headers

# copy over Makefile.global to the include dir....
install -m755 src/Makefile.global $RPM_BUILD_ROOT/usr/include/pgsql

%if %jdbc
	# Java/JDBC
	# Red Hat standardized on /usr/share/java for jars...

	# JDBC jars 
	mkdir -p $RPM_BUILD_ROOT/usr/share/java
	install -m 755 %{SOURCE8} $RPM_BUILD_ROOT/usr/share/java
	install -m 755 %{SOURCE9} $RPM_BUILD_ROOT/usr/share/java
	install -m 755 %{SOURCE10} $RPM_BUILD_ROOT/usr/share/java
	install -m 755 %{SOURCE11} $RPM_BUILD_ROOT/usr/share/java

%endif

if [ -d /etc/rc.d/init.d ]
then
	install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
	install -m 755 %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/postgresql
fi


# PGDATA needs removal of group and world permissions due to pg_pwd hole.
install -d -m 700 $RPM_BUILD_ROOT/var/lib/pgsql/data

# backups of data go here...
install -d -m 700 $RPM_BUILD_ROOT/var/lib/pgsql/backups

# postgres' .bash_profile
install -m 644 %{SOURCE15} $RPM_BUILD_ROOT/var/lib/pgsql/.bash_profile

# Create the multiple postmaster startup directory
install -d -m 700 $RPM_BUILD_ROOT/etc/sysconfig/pgsql


%if %test
	# tests. There are many files included here that are unnecessary, but include
	# them anyway for completeness.
	mkdir -p $RPM_BUILD_ROOT/usr/lib/pgsql/test
	cp -a src/test/regress $RPM_BUILD_ROOT/usr/lib/pgsql/test
	install -m 0755 contrib/spi/refint.so $RPM_BUILD_ROOT/usr/lib/pgsql/test/regress
	install -m 0755 contrib/spi/autoinc.so $RPM_BUILD_ROOT/usr/lib/pgsql/test/regress
	pushd  $RPM_BUILD_ROOT/usr/lib/pgsql/test/regress/
	strip *.so
	popd
%endif

# Fix some more documentation
# gzip doc/internals.ps
cp %{SOURCE6} README.rpm-dist
mv $RPM_BUILD_ROOT%{_docdir}/postgresql/html doc

rm -rf $RPM_BUILD_ROOT%{_docdir}/postgresql
%if %tkpkg
%else
rm -rf $RPM_BUILD_ROOT%{_mandir}/man1/pgtksh.*
%endif
%if %tcl
%else
rm -rf %{buildroot}%{_mandir}/man1/pgtclsh.*
%endif

%find_lang libpq
%find_lang pg_dump
%find_lang postgres
%find_lang psql
%find_lang pg_resetxlog
%find_lang pg_controldata

cat libpq.lang > libpq.lst
cat psql.lang pg_dump.lang > main.lst
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
chown -R postgres:postgres /usr/lib/pgsql/test >/dev/null 2>&1 || :
%endif

%clean
rm -rf $RPM_BUILD_ROOT

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

%files contrib
%defattr(-,root,root)
%{_libdir}/pgsql/_int.so
%{_libdir}/pgsql/array_iterator.so
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
%doc contrib/*/README.* contrib/spi/*.example

%files libs -f libpq.lang
%defattr(-,root,root)
%{_libdir}/libpq.so.*
%{_libdir}/libecpg.so.*

%files server -f server.lst
%defattr(-,root,root)
/etc/rc.d/init.d/postgresql
%attr(755,root,root) %dir /etc/sysconfig/pgsql
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
%if %tkpkg
%{_bindir}/pgtksh
%{_mandir}/man1/pgtksh.*
%endif
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
%doc src/interfaces/python/README src/interfaces/python/tutorial
%{_libdir}/python%{pyver}/site-packages/_pgmodule.so
%{_libdir}/python%{pyver}/site-packages/*.py
%endif

%if %jdbc
%files jdbc
%defattr(-,root,root)
%{_datadir}/java/pg73jdbc1.jar
%{_datadir}/java/pg73jdbc2.jar
%{_datadir}/java/pg73jdbc2ee.jar
%{_datadir}/java/pg73jdbc3.jar
%endif

%if %test
%files test
%defattr(-,postgres,postgres)
%attr(-,postgres,postgres) /usr/lib/pgsql/test/*
%attr(-,postgres,postgres) %dir /usr/lib/pgsql/test
%endif

%changelog
* Thu Jan 3 2008 Devrim GUNDUZ <devrim@commandprompt.com> 7.3.21-1PGDG
- Update to 7.3.21, which also includes security fixes for CVE-2007-4769, 
  CVE-2007-4772, CVE-2007-6067, CVE-2007-6600, CVE-2007-6601
- Update copyright date
- Added a patch to disable autoconf version checks in configure.in

* Wed Oct 10 2007 Devrim GUNDUZ <devrim@commandprompt.com> 7.3.20-2PGDG
- Rebuilt

* Sat Sep 15 2007 Devrim GUNDUZ <devrim@commandprompt.com> 7.3.20-1PGDG
- 7.3.20-1PGDG

* Sat Apr 21 2007 Devrim GUNDUZ <devrim@commandprompt.com> 7.3.19-1PGDG
- 7.3.19-1PGDG

* Sat Feb 3 2007 Devrim GUNDUZ <devrim@commandprompt.com> 7.3.18-1PGDG
- 7.3.18-1PGDG

* Wed Jan 3 2007 Devrim GUNDUZ <devrim@commandprompt.com> 7.3.17-1PGDG
- 7.3.17-1PGDG
- Change patch names so that we only use major version numbers in patches.

* Sun Oct 15 2006 Devrim GUNDUZ <devrim@commandprompt.com> 7.3.16-1PGDG
- 7.3.16-1PGDG
- Fix some of the rpmlint warnings and errors
- Fix spec
- Remove patch #4
- add pgtclsh manpage among installed files

* Mon May 22 2006 Devrim GUNDUZ <devrim@commandprompt.com> 7.3.15-1PGDG
- 7.3.15-1PGDG

* Tue Feb 14 2006 Devrim GUNDUZ <devrim@commandprompt.com> 7.3.14-1PGDG
- 7.3.14-1PGDG

* Mon Jan 09 2006 Devrim GUNDUZ <devrim@commandprompt.com> 7.3.13-1PGDG
- 7.3.13-1PGDG

* Mon Oct 10 2005 Devrim GUNDUZ <devrim@gunduz.org>
- 7.3.11-1PGDG 

* Thu May 12 2005 Devrim GUNDUZ <devrim@gunduz.org>
- 7.3.10-1PGDG 
- Fixed init script (DG)

* Sat Feb 5 2005 Devrim GUNDUZ <devrim@gunduz.org>
- 7.3.9-1PGDG 

* Wed Nov 17 2004 Devrim GUNDUZ <devrim@gunduz.org>
- 7.3.8-3PGDG
- Fixed PGVERSION value in init script.

* Tue Oct 26 2004 Devrim GUNDUZ <devrim@gunduz.org>
- 7.3.8-2PGDG
- Merged changes in 7.4.6-2 
- Updated postgresql.init

* Sat Oct 23 2004 Devrim GUNDUZ <devrim@gunduz.org>
- 7.3.8-1PGDG
- Updated JDBC jars to 7.3 Build 113

* Sat Aug 21 2004 Devrim GUNDUZ <devrim@gunduz.org> 7.3.7-1PGDG
- 7.3.7

* Mon Mar 08 2004 Lamar Owen <lowen@pari.edu> 7.3.6-1PGDG
- 7.3.6
- Least surprise; few changes by design.
- Backport specfile changes from 7.4.2 set for portable building.
- pl/python build patch.
B- /etc/sysconfig/pgsql chmod 755
- JDBC jars in /usr/share/java.

* Mon Jul 28 2003 Lamar Owen <lowen@pari.edu> 7.3.4-1PGDG
- 7.3.4
- Correct JDBC jars

* Tue May 27 2003 Lamar Owen <lamar.owen@wgcr.org> 7.3.3-1PGDG
- Synced up with RawHide.
- 7.3.3
- Eliminate spurious symlink of libpq.so.2.
- Dropped isblank patch; 7.3.3 uses pg_isblank

* Wed Apr 16 2003 Andrew Overholt <overholt@redhat.com> 7.3.2-4
- Obsolete postgresql-perl and postgresql-tk

* Mon Feb 17 2003 Elliot Lee <sopwith@redhat.com> 7.3.2-4
- Add ppc64 patch

* Fri Feb 14 2003 Andrew Overholt <overholt@redhat.com> 7.3.2-3
- Remove pltcl.so from postgresql-tcl and plpython.so from postgresql-server.

* Wed Feb 12 2003 Andrew Overholt <overholt@redhat.com> 7.3.2-2
- Fix typo in pg_hba.conf tighten patch.

* Wed Feb 5 2003 Andrew Overholt <overholt@redhat.com> 7.3.2-1
- Initial 7.3.2 build.
- Add bison and flex to BuildRequires line. 

* Mon Feb 03 2003 Lamar Owen <lamar.owen@ramfordistat.net>
- 7.3.2-1PGDG

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jan 09 2003 Elliot Lee <sopwith@redhat.com> 7.3.1-5
- Rebuild for newer libssl
- Add patch4 (isblank.patch) to make it all build

* Sat Jan  4 2003 Jeff Johnson <jbj@redhat.com> 7.3.1-4
- use internal dep generator.    

* Fri Jan 3 2003 Andrew Overholt <overholt@redhat.com> 7.3.1-3
- Remove spurious Prereq line

* Fri Jan 3 2003 Andrew Overholt <overholt@redhat.com> 7.3.1-2
- Rebuild with new 7.3.1 tarball
- Remove obsoletes postgresql-perl line (should have been postgresql-plperl)
  as we did not have that package previously

* Mon Dec 23 2002 Lamar Owen <lamar.owen@ramifordistat.net>
- 7.3.1-1PGDG
- Fix dependency order for test and pl subpackages.
- Fixed a bug in the initscript for echo_success

* Wed Dec 18 2002 Andrew Overholt <overholt@redhat.com> 7.3.1-1
- Initial 7.3.1 build.

* Tue Dec 17 2002 Nalin Dahyabhai <nalin@redhat.com> 7.3-6
- Make postgresql-pl obsolete postgresql-perl, not postgresql-plperl

* Fri Dec 13 2002 Andrew Overholt <overholt@redhat.com>
- Remove perl(Pg) dependency
- Bash profile PGDATA fix
- Updated initscript to new community version

* Tue Dec 10 2002 Andrew Overholt <overholt@redhat.com>
- Upgrade to 7.3 community spec file.
- Add patch to use with multilib.
- Change explicit path names to use RPM macros (multilib).
- Add security patch.

* Thu Dec 05 2002 Lamar Owen <lamar.owen@ramifordistat.net>
- 7.3-2PGDG
- Fix typo in initscript.  Argh!!

* Wed Dec 04 2002 Lamar Owen <lamar.owen@ramifordistat.net>
- 7.3-0.5PGDG
- Jerk out all perl client stuff and kludgage
- Rename plperl subpackage to a pl subpackage containing all but PL/Pgsql PL's
- Eliminate locale and multibyte explicit enables -- they are both defaults now
- Eliminate pgaccess code; it's not a part of the main tarball anymore
- Eliminate ODBC stuff -- it's also separate now.  Use unixODBC instead.
- Eliminated separate tk client package -- rolled the tk client into the tcl client.
- Moved pltcl into the pl subpackage.
- Added plpython to the pl subpackage.
- /etc/sysconfig/pgsql is sysconfdir for multiple postmaster startup.


* Mon Dec 02 2002 Lamar Owen <lamar.owen@ramifordistat.net>
- 7.3-0.1PGDG (not released)
- Integrate 7.3 jar's courtesy Joe Conway
- Integrate multi-postmaster initscript courtesy Karl DeBisschop
- Some renames and restructures.
- Stripped out the last dregs of the postgresql-dump migration script.
- Conflicts with less than 7.3.
