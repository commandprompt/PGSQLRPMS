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
# This is the PostgreSQL Global Development Group Official RPMset spec file,
# or a derivative thereof.
# Copyright 2003 Lamar Owen <lowen@pari.edu> <lamar.owen@wgcr.org>
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

# In this file you can find the default build package list macros.  These can be overridden by defining
# on the rpm command line:
# rpm --define 'packagename 1' .... to force the package to build.
# rpm --define 'packagename 0' .... to force the package NOT to build.
# The base package, the lib package, the devel package, and the server package always get built.

%{?build9:%define kerbdir %{_usr}/kerberos}
%{?build9:%define build9 1}
%{?buildrhel3:%define kerbdir %{_usr}/kerberos}

%define beta 0
%{?beta:%define __os_install_post /usr/lib/rpm/brp-compress}

%{expand: %%define majorversion 8.1}

%{!?aconfver:%define aconfver autoconf}
%{!?kerbdir:%define kerbdir "%{_usr}"}

%{!?tcldevel:%define tcldevel 1}
%{!?test:%define test 1}
%{!?python:%define python 1}
%{!?pltcl:%define pltcl 1}
%{!?plperl:%define plperl 1}
%{!?pls:%define pls 1}
%{!?ssl:%define ssl 1}
%{!?kerberos:%define kerberos 1}
%{!?nls:%define nls 1}
%{!?xml:%define xml 1}
%{!?pam:%define pam 1}
%{!?pgfts:%define pgfts 0}
%{!?runselftest:%define runselftest 0}

Summary:	PostgreSQL client programs and libraries
Name:		postgresql
Version:	8.1.5
Release:	7MPGDG
License:	BSD
Group:		Applications/Databases
Url:		http://www.postgresql.org/ 

Source0:	ftp://ftp.postgresql.org/pub/source/v%{version}/%{name}-%{version}.tar.bz2
Source3:	%{name}.init-multiple
Source4:	Makefile.regress
Source5:	pg_config.h
Source6:	README.rpm-dist
Source8:        pgsql-%{majorversion}.conf
Source12:	http://www.postgresql.org/files/documentation/pdf/8.1/%{name}-8.1-A4.pdf
Source14:	%{name}.pam
Source15:	%{name}-bashprofile
Source16:	filter-requires-perl-Pg.sh

Patch1:		rpm-pgsql.patch
Patch2:		postgresql-src-tutorial.patch
Patch3:		postgresql-logging.patch
Patch4:		postgresql-test.patch
Patch6:		postgresql-perl-rpath.patch
Patch8:         postgresql-multiple-locale.patch

BuildRequires:	perl glibc-devel bison flex autoconf
Requires:	/sbin/ldconfig initscripts

%if %python
BuildPrereq:	python-devel
%endif

%if %pltcl
BuildRequires:	tcl
%endif

%if %tcldevel
Buildrequires:	tcl-devel
%endif

BuildRequires:	readline-devel
BuildRequires:	zlib-devel >= 1.0.4

%if %ssl
BuildRequires:	openssl-devel
%endif

%if %kerberos
BuildRequires:	krb5-devel
BuildRequires:	e2fsprogs-devel
%endif

%if %nls
BuildRequires:	gettext >= 0.10.35
%endif

%if %xml
BuildRequires:	libxml2-devel libxslt-devel
%endif

%if %pam
BuildRequires:	pam-devel
%endif

Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

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

If you want to manipulate a PostgreSQL database on a local or remote PostgreSQL
server, you need this package. You also need to install this package
if you're installing the postgresql-server package.

%package libs
Summary:	The shared libraries required for any PostgreSQL clients
Group:		Applications/Databases
Provides:	libpq.so

%description libs
The postgresql-libs package provides the essential shared libraries for any 
PostgreSQL client program or interface. You will need to install this package
to use any other PostgreSQL package or any clients that need to connect to a
PostgreSQL server.

%package server
Summary:	The programs needed to create and run a PostgreSQL server
Group:		Applications/Databases
Requires:	/usr/sbin/useradd /sbin/chkconfig 
Requires:	postgresql = %{version} libpq.so
Conflicts:	postgresql < 7.4

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
Summary:	Extra documentation for PostgreSQL
Group:		Applications/Databases

%description docs
The postgresql-docs package includes the SGML source for the documentation
as well as the documentation in PDF format and some extra documentation.
Install this package if you want to help with the PostgreSQL documentation
project, or if you want to generate printed documentation.

%package lang
Summary:	The translated files for PostgreSQL
Group:		Applications/Databases
Requires:	postgresql = %{version} postgresql-libs = %{version}
Requires:	postgresql-server = %{version} postgresql-devel = %{version}

%description lang
The postgresql-lang package provides the essential files that
are needed to use PostgreSQL in languages other than English. You
will need to install base, libs, devel and server packages before
installing this package.

%package contrib
Summary:	Contributed source and binaries distributed with PostgreSQL
Group:		Applications/Databases
Requires:	postgresql = %{version}

%description contrib
The postgresql-contrib package contains contributed packages that are
included in the PostgreSQL distribution.

%package devel
Summary:	PostgreSQL development header files and libraries
Group:		Development/Libraries
Requires:	postgresql-libs = %{version}
Requires:	postgresql = %{version}

%description devel
The postgresql-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with a PostgreSQL database management server and the ecpg Embedded C
Postgres preprocessor. You need to install this package if you want to
develop applications which will interact with a PostgreSQL server. 

%if %pls
%package	pl
Summary:	The PL procedural languages for PostgreSQL
Group:		Applications/Databases
Requires:	postgresql = %{version}
Requires:	postgresql-server = %{version}

%description pl
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-pl package contains the the PL/Perl, and PL/Python
procedural languages for the backend where PL/Pgsql is part of the core server package.
%endif

%if %test
%package test
Summary:	The test suite distributed with PostgreSQL
Group:		Applications/Databases
Requires:	postgresql = %{version}
Requires:	postgresql-server = %{version}

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
# patch5 is applied later
%patch6 -p1
%patch8 -p1

pushd doc
tar -zcf postgres.tar.gz *.html stylesheet.css
rm -f *.html stylesheet.css
popd

cp -p %{SOURCE12} .

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
%configure \
	--disable-rpath \
	--libdir=%{_libdir}/pgsql/%{majorversion} \
	--includedir=%{_includedir}/pgsql/%{majorversion} \
	--bindir=%{_bindir}/pgsql/%{majorversion} \
	--mandir=%{_mandir}/pgsql/%{majorversion} \
%if %beta
	--enable-debug \
	--enable-cassert \
%endif
%if %plperl
	--with-perl \
%endif
%if %pltcl
	--with-tcl \
	--with-tclconfig=%{_libdir} \
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
	--with-krb5 \
	--with-includes=%{kerbdir}/include \
	--with-libraries=%{kerbdir}/lib \
%endif
%if %nls
	--enable-nls \
%endif
%if %pgfts
	--enable-thread-safety \
%endif
	--sysconfdir=/etc/sysconfig/pgsql \
	--datadir=/usr/share/pgsql/%{majorversion} \
	--with-docdir=%{_docdir}

make %{?_smp_mflags} all
make %{?_smp_mflags} -C contrib all
%if %xml
	make %{?_smp_mflags} -C contrib/xml2 all
%endif
                              
# Have to hack makefile to put correct path into tutorial scripts
sed "s|C=\`pwd\`;|C=%{_libdir}/pgsql/%{majorversion}/tutorial;|" < src/tutorial/Makefile > src/tutorial/GNUmakefile
make %{?_smp_mflags} -C src/tutorial NO_PGXS=1 all
rm -f src/tutorial/GNUmakefile

%if %runselftest
	pushd src/test/regress
	make all
	make MAX_CONNECTIONS=5 check
	make clean
	popd
%endif

%if %test
	pushd src/test/regress
	make RPMTESTING=1 all
	popd
%endif

%install
rm -rf %{buildroot}

make DESTDIR=%{buildroot} install
make -C contrib DESTDIR=%{buildroot} install

%if %xml
	make -C contrib/xml2 DESTDIR=%{buildroot} install
%endif

# multilib header hack; note pg_config.h is installed in two places!
# we only apply this to known Red Hat multilib arches, per bug #177564
#case `uname -i` in
#	i386 | x86_64 | ppc | ppc64 | s390 | s390x)
#		mv %{buildroot}%{_includedir}/pg_config.h %{buildroot}%{_includedir}/pg_config_`uname -i`.h
#		install -m 644 %{SOURCE5} %{buildroot}%{_includedir}/pgsql/%{majorversion}
#		mv %{buildroot}%{_includedir}/pgsql/server/pg_config.h %{buildroot}%{_includedir}/pgsql/%{majorversion}server/pg_config_`uname -i`.h
#		install -m 644 %{SOURCE5} %{buildroot}%{_includedir}/pgsql/%{majorversion}/server/
#    ;;
#  *)
#    ;;
#esac

install -d -m 755 %{buildroot}%{_libdir}/pgsql/tutorial
cp src/tutorial/* %{buildroot}%{_libdir}/pgsql/tutorial

if [ -d /etc/rc.d/init.d ]
then
	install -d %{buildroot}%{_sysconfdir}/rc.d/init.d
	sed 's/^PGVERSION=.*$/PGVERSION=%{version}/' <%{SOURCE3} > postgresql.init
	install -m 755 postgresql.init %{buildroot}%{_sysconfdir}/rc.d/init.d/postgresql-%{majorversion}
fi

if [ -d /etc/ld.so.conf.d ]
then
	install -d %{buildroot}%{_sysconfdir}/ld.so.conf.d
	install -m 755 %{SOURCE8} %{buildroot}/etc/ld.so.conf.d/
fi

%if %pam
if [ -d /etc/pam.d ]
then
	install -d %{buildroot}%{_sysconfdir}/pam.d
	install -m 644 %{SOURCE14} %{buildroot}%{_sysconfdir}/pam.d/postgresql
fi
%endif

# PGDATA needs removal of group and world permissions due to pg_pwd hole.
install -d -m 700 %{buildroot}/var/lib/pgsql/%{majorversion}/data

# backups of data go here...
install -d -m 700 %{buildroot}/var/lib/pgsql/%{majorversion}/backups

# postgres' .bash_profile
install -m 644 %{SOURCE15} %{buildroot}/var/lib/pgsql/.bash_profile

# Create the multiple postmaster startup directory
install -d -m 700 %{buildroot}%{_sysconfdir}/sysconfig/pgsql

%if %test
	# tests. There are many files included here that are unnecessary, but include
	# them anyway for completeness.
	mkdir -p %{buildroot}%{_libdir}/pgsql/%{majorversion}/test
	cp -a src/test/regress %{buildroot}%{_libdir}/pgsql/%{majorversion}/test
	install -m 0755 contrib/spi/refint.so %{buildroot}%{_libdir}/pgsql/%{majorversion}/test/regress
	install -m 0755 contrib/spi/autoinc.so %{buildroot}%{_libdir}/pgsql/%{majorversion}/test/regress
	pushd  %{buildroot}%{_libdir}/pgsql/%{majorversion}/test/regress/
	strip *.so
	rm -f GNUmakefile Makefile
	popd
	cp %{SOURCE4} %{buildroot}%{_libdir}/pgsql/%{majorversion}/test/regress/Makefile
	chmod 0644 %{buildroot}%{_libdir}/pgsql/%{majorversion}/test/regress/Makefile
%endif

# Fix some more documentation
# gzip doc/internals.ps
cp %{SOURCE6} README.rpm-dist
mv %{buildroot}%{_docdir}/pgsql/html doc
rm -rf %{buildroot}%{_docdir}/pgsql

%post libs -p /sbin/ldconfig 
%postun libs -p /sbin/ldconfig 

%pre server
groupadd -g 26 -o -r postgres >/dev/null 2>&1 || :
useradd -M -n -g postgres -o -r -d /var/lib/pgsql -s /bin/bash \
	-c "PostgreSQL Server" -u 26 postgres >/dev/null 2>&1 || :
touch /var/log/pgsql-%{majorversion}
chown postgres:postgres /var/log/pgsql-%{majorversion}
chmod 0700 /var/log/pgsql-%{majorversion}

%post server
chkconfig --add postgresql-%{majorversion}
/sbin/ldconfig

%preun server
if [ $1 = 0 ] ; then
	/sbin/service postgresql-%{majorversion} condstop >/dev/null 2>&1
	chkconfig --del postgresql-%{majorversion}
fi

%postun server
/sbin/ldconfig 
if [ $1 -ge 1 ]; then
	/sbin/service postgresql-%{majorversion} condrestart >/dev/null 2>&1
fi
if [ $1 = 0 ] ; then
	userdel postgres >/dev/null 2>&1 || :
	groupdel postgres >/dev/null 2>&1 || : 
fi

%if %pls
	%post -p /sbin/ldconfig   pl
	%postun -p /sbin/ldconfig   pl
%endif

%if %test
	%post test
	chown -R postgres:postgres /usr/share/pgsql/%{majorversion}/test >/dev/null 2>&1 || :
%endif

%clean
rm -rf %{buildroot}

# FILES section.

%files
%defattr(-,root,root)
%doc doc/FAQ doc/KNOWN_BUGS doc/MISSING_FEATURES doc/README* 
%doc COPYRIGHT README HISTORY doc/bug.template
%doc README.rpm-dist
%doc doc/html
%{_bindir}/pgsql/%{majorversion}/clusterdb
%{_bindir}/pgsql/%{majorversion}/createdb
%{_bindir}/pgsql/%{majorversion}/createlang
%{_bindir}/pgsql/%{majorversion}/createuser
%{_bindir}/pgsql/%{majorversion}/dropdb
%{_bindir}/pgsql/%{majorversion}/droplang
%{_bindir}/pgsql/%{majorversion}/dropuser
%{_bindir}/pgsql/%{majorversion}/pg_dump
%{_bindir}/pgsql/%{majorversion}/pg_dumpall
%{_bindir}/pgsql/%{majorversion}/pg_restore
%{_bindir}/pgsql/%{majorversion}/psql
%{_bindir}/pgsql/%{majorversion}/reindexdb
%{_bindir}/pgsql/%{majorversion}/vacuumdb
%{_mandir}/pgsql/%{majorversion}/man1/clusterdb.*
%{_mandir}/pgsql/%{majorversion}/man1/createdb.*
%{_mandir}/pgsql/%{majorversion}/man1/createlang.*
%{_mandir}/pgsql/%{majorversion}/man1/createuser.*
%{_mandir}/pgsql/%{majorversion}/man1/dropdb.*
%{_mandir}/pgsql/%{majorversion}/man1/droplang.*
%{_mandir}/pgsql/%{majorversion}/man1/dropuser.*
%{_mandir}/pgsql/%{majorversion}/man1/pg_dump.*
%{_mandir}/pgsql/%{majorversion}/man1/pg_dumpall.*
%{_mandir}/pgsql/%{majorversion}/man1/pg_restore.*
%{_mandir}/pgsql/%{majorversion}/man1/psql.*
%{_mandir}/pgsql/%{majorversion}/man1/reindexdb.*
%{_mandir}/pgsql/%{majorversion}/man1/vacuumdb.*
%{_mandir}/pgsql/%{majorversion}/man7/*

%files docs
%defattr(-,root,root)
%doc doc/src/*
%doc *-A4.pdf
%{_libdir}/pgsql/tutorial/

%files contrib
%defattr(-,root,root)
%{_libdir}/pgsql/%{majorversion}/_int.so
%{_libdir}/pgsql/%{majorversion}/autoinc.so
%{_libdir}/pgsql/%{majorversion}/btree_gist.so
%{_libdir}/pgsql/%{majorversion}/chkpass.so
%{_libdir}/pgsql/%{majorversion}/cube.so
%{_libdir}/pgsql/%{majorversion}/dblink.so
%{_libdir}/pgsql/%{majorversion}/earthdistance.so
%{_libdir}/pgsql/%{majorversion}/fti.so
%{_libdir}/pgsql/%{majorversion}/fuzzystrmatch.so
%{_libdir}/pgsql/%{majorversion}/insert_username.so
%{_libdir}/pgsql/%{majorversion}/int_aggregate.so
%{_libdir}/pgsql/%{majorversion}/isbn_issn.so
%{_libdir}/pgsql/%{majorversion}/lo.so
%{_libdir}/pgsql/%{majorversion}/ltree.so
%{_libdir}/pgsql/%{majorversion}/moddatetime.so
%{_libdir}/pgsql/%{majorversion}/pending.so
%{_libdir}/pgsql/%{majorversion}/pgcrypto.so
%{_libdir}/pgsql/%{majorversion}/pgstattuple.so
%{_libdir}/pgsql/%{majorversion}/pg_buffercache.so
%{_libdir}/pgsql/%{majorversion}/pg_trgm.so
%{_libdir}/pgsql/%{majorversion}/refint.so
%{_libdir}/pgsql/%{majorversion}/seg.so
%{_libdir}/pgsql/%{majorversion}/tablefunc.so
%{_libdir}/pgsql/%{majorversion}/timetravel.so
%{_libdir}/pgsql/%{majorversion}/tsearch2.so
%{_libdir}/pgsql/%{majorversion}/user_locks.so
%if %xml
%{_libdir}/pgsql/%{majorversion}/pgxml.so
%endif
%{_datadir}/pgsql/%{majorversion}/contrib/
%{_bindir}/pgsql/%{majorversion}/DBMirror.pl
%{_bindir}/pgsql/%{majorversion}/clean_pending.pl
%{_bindir}/pgsql/%{majorversion}/dbf2pg
%{_bindir}/pgsql/%{majorversion}/fti.pl
%{_bindir}/pgsql/%{majorversion}/oid2name
%{_bindir}/pgsql/%{majorversion}/pgbench
%{_bindir}/pgsql/%{majorversion}/vacuumlo
%doc contrib/*/README.* contrib/spi/*.example

%files libs
%defattr(-,root,root)
%{_sysconfdir}/ld.so.conf.d/pgsql-%{majorversion}.conf
%{_libdir}/pgsql/%{majorversion}/libpq.so.*
%{_libdir}/pgsql/%{majorversion}/libecpg.so.*
%{_libdir}/pgsql/%{majorversion}/libpgtypes.so.*
%{_libdir}/pgsql/%{majorversion}/libecpg_compat.so.*

%files lang
%defattr(-,root,root)
%{_datadir}/pgsql/locale/%{majorversion}/*/LC_MESSAGES/initdb.mo
%{_datadir}/pgsql/locale/%{majorversion}/*/LC_MESSAGES/pg_ctl.mo
%{_datadir}/pgsql/locale/%{majorversion}/*/LC_MESSAGES/pg_dump.mo
%{_datadir}/pgsql/locale/%{majorversion}/*/LC_MESSAGES/pgscripts.mo
%{_datadir}/pgsql/locale/%{majorversion}/*/LC_MESSAGES/psql.mo
%{_datadir}/pgsql/locale/%{majorversion}/*/LC_MESSAGES/libpq.mo
%{_datadir}/pgsql/locale/%{majorversion}/*/LC_MESSAGES/pg_config.mo
%{_datadir}/pgsql/locale/%{majorversion}/*/LC_MESSAGES/pg_controldata.mo
%{_datadir}/pgsql/locale/%{majorversion}/*/LC_MESSAGES/pg_resetxlog.mo
%{_datadir}/pgsql/locale/%{majorversion}/*/LC_MESSAGES/postgres.mo

%files server
%defattr(-,root,root)
/etc/rc.d/init.d/postgresql-%{majorversion}
%if %pam
%config(noreplace) /etc/pam.d/postgresql
%endif
%attr (755,root,root) %dir /etc/sysconfig/pgsql
%{_bindir}/pgsql/%{majorversion}/initdb
%{_bindir}/pgsql/%{majorversion}/ipcclean
%{_bindir}/pgsql/%{majorversion}/pg_controldata
%{_bindir}/pgsql/%{majorversion}/pg_ctl
%{_bindir}/pgsql/%{majorversion}/pg_resetxlog
%{_bindir}/pgsql/%{majorversion}/postgres
%{_bindir}/pgsql/%{majorversion}/postmaster
%{_mandir}/pgsql/%{majorversion}/man1/initdb.*
%{_mandir}/pgsql/%{majorversion}/man1/ipcclean.*
%{_mandir}/pgsql/%{majorversion}/man1/pg_controldata.*
%{_mandir}/pgsql/%{majorversion}/man1/pg_ctl.*
%{_mandir}/pgsql/%{majorversion}/man1/pg_resetxlog.*
%{_mandir}/pgsql/%{majorversion}/man1/postgres.*
%{_mandir}/pgsql/%{majorversion}/man1/postmaster.*
%{_datadir}/pgsql/%{majorversion}/postgres.bki
%{_datadir}/pgsql/%{majorversion}/postgres.description
%{_datadir}/pgsql/%{majorversion}/system_views.sql
%{_datadir}/pgsql/%{majorversion}/*.sample
%{_datadir}/pgsql/%{majorversion}/timezone/
%{_libdir}/pgsql/%{majorversion}/plpgsql.so
%dir %{_libdir}/pgsql/%{majorversion}
%dir %{_datadir}/pgsql/%{majorversion}
%attr(700,postgres,postgres) %dir /var/lib/pgsql
%attr(700,postgres,postgres) %dir /var/lib/pgsql/%{majorversion}
%attr(700,postgres,postgres) %dir /var/lib/pgsql/%{majorversion}/data
%attr(700,postgres,postgres) %dir /var/lib/pgsql/%{majorversion}/backups
%attr(644,postgres,postgres) %config(noreplace) /var/lib/pgsql/.bash_profile
%{_libdir}/pgsql/%{majorversion}/*_and_*.so
%{_datadir}/pgsql/%{majorversion}/conversion_create.sql
%{_datadir}/pgsql/%{majorversion}/information_schema.sql
%{_datadir}/pgsql/%{majorversion}/sql_features.txt

%files devel
%defattr(-,root,root)
/usr/include/*
%{_bindir}/pgsql/%{majorversion}/ecpg
%{_bindir}/pgsql/%{majorversion}/pg_config
%{_libdir}/pgsql/%{majorversion}/libpq.so
%{_libdir}/pgsql/%{majorversion}/libecpg.so
%{_libdir}/pgsql/%{majorversion}/libpq.a
%{_libdir}/pgsql/%{majorversion}/libecpg.a
%{_libdir}/pgsql/%{majorversion}/libecpg_compat.so
%{_libdir}/pgsql/%{majorversion}/libecpg_compat.a
%{_libdir}/pgsql/%{majorversion}/libpgport.a
%{_libdir}/pgsql/%{majorversion}/libpgtypes.so
%{_libdir}/pgsql/%{majorversion}/libpgtypes.a
%{_libdir}/pgsql/%{majorversion}/pgxs/*
%{_mandir}/pgsql/%{majorversion}/man1/ecpg.*
%{_mandir}/pgsql/%{majorversion}/man1/pg_config.*

%if %pls
%files pl
%defattr(-,root,root)
%if %plperl
%{_libdir}/pgsql/%{majorversion}/plperl.so
%endif
%if %pltcl
%{_libdir}/pgsql/%{majorversion}/pltcl.so
%{_bindir}/pgsql/%{majorversion}/pltcl_delmod
%{_bindir}/pgsql/%{majorversion}/pltcl_listmod
%{_bindir}/pgsql/%{majorversion}/pltcl_loadmod
%{_datadir}/pgsql/%{majorversion}/unknown.pltcl
%endif
%if %python
%{_libdir}/pgsql/%{majorversion}/plpython.so
%endif
%endif

%if %test
%files test
%defattr(-,postgres,postgres)
%attr(-,postgres,postgres) %{_libdir}/pgsql/%{majorversion}/test/*
%attr(-,postgres,postgres) %dir %{_libdir}/pgsql/%{majorversion}/test
%endif

%changelog
* Mon Oct 30 2006 Devrim GUNDUZ <devrim@commandprompt.com> 8.1.5-7MPGDG
- Multiple postmaster - first cut

* Mon Oct 30 2006 Devrim GUNDUZ <devrim@commandprompt.com> 8.1.5-6PGDG
- Fixed homedir of postgres user, per report from Tatsuhito Kasahara

* Sat Oct 28 2006 Devrim GUNDUZ <devrim@commandprompt.com> 8.1.5-5PGDG
- Fixed 64 bit builds.
- Fixed changelog

* Fri Oct 27 2006 Devrim GUNDUZ <devrim@commandprompt.com> 8.1.5-4PGDG
- Added pl/python related parts again.

* Tue Oct 17 2006 Devrim GUNDUZ <devrim@commandprompt.com> 8.1.5-3PGDG
- Fix dependency bug, per Stig Erikson

* Fri Oct 6 2006 Devrim GUNDUZ <devrim@commandprompt.com> 8.1.5-2PGDG
- Cleanup for python

* Fri Oct 6 2006 Devrim GUNDUZ <devrim@commandprompt.com> 8.1.5-1PGDG
- Update to 8.1.5

* Sat Aug 16 2006 Devrim GUNDUZ <devrim@commandprompt.com> 8.1.4-8PGDG
- Splitted python into a seperate RPM
- Splitted tcl into a seperate RPM

* Sat Aug 12 2006 Devrim GUNDUZ <devrim@commandprompt.com> 8.1.4-7PGDG
- Splitted jdbc into a seperate rpm
- Removed build7,build8 tags. Did not remove build9 since we have still
  some Red Hat 9 users around.

* Sun Jul 23 2006 Devrim GUNDUZ <devrim@commandprompt.com> 8.1.4-6PGDG
- Change buildroot macro

* Wed Jul 12 2006 Devrim GUNDUZ <devrim@commandprompt.com> 8.1.4-5PGDG
- Fix tutorial location bug in spec file.

* Mon Jul 10 2006 Devrim GUNDUZ <devrim@commandprompt.com> 8.1.4-4PGDG
- Make pg_config.h architecture-independent for multilib installs;
  put the original pg_config.h into pg_config_$ARCH.h (Per Red Hat RPMS, Tom Lane)
- Suppress noise from chcon, per bugzila bug #187744 (Per Red Hat RPMS, Tom Lane)
- Modify multilib header hack to not break non-RH arches, per bug #177564

* Tue Jun 06 2006 Devrim GUNDUZ <devrim@commandprompt.com> 8.1.4-3PGDG
- Updated PyGreSQL from 3.8 to 3.8.1

* Sat May 27 2006 Devrim GUNDUZ <devrim@commandprompt.com> 8.1.4-2PGDG
- Fix tcl builds, patch from Tom Lane.
- Update JDBC jars to build 407

* Mon May 22 2006 Devrim GUNDUZ <devrim@commandprompt.com> 8.1.4-1PGDG
- Temporarily disable tcl builds, until they or we fix the problem.
- Update JDBC jars to build 406
- Fix PyGreSQL filenames
- Update to 8.1.4

* Sun Feb 19 2006 Devrim GUNDUZ <devrim@commandprompt.com> 8.1.3-2PGDG
- Updated PyGreSQL from 3.7 to 3.8

* Mon Feb 13 2006 Devrim GUNDUZ <devrim@commandprompt.com> 8.1.3-1PGDG
- Update to 8.1.3

* Thu Feb 09 2006 Devrim GUNDUZ <devrim@commandprompt.com> 8.1.2-2PGDG
- Update JDBC jars to build 405

* Tue Jan 10 2006 Devrim GUNDUZ <devrim@commandprompt.com> 8.1.2-1PGDG
- Update to  8.1.2

* Sat Dec 10 2005 Devrim GUNDUZ <devrim@commandprompt.com> 8.1.1-2PGDG
- Re-added PDF documentation into RPM.

* Sat Dec 10 2005 Devrim GUNDUZ <devrim@commandprompt.com> 8.1.1-1PGDG
- 8.1.1

* Thu Dec 5 2005 Devrim GUNDUZ <devrim@PostgreSQL.org> 8.1.0-5PGDG
- Enabled tcl builds by default.

* Thu Dec 01 2005 Devrim GUNDUZ <devrim@PostgreSQL.org> 8.1.0-4PGDG
- Added a macro for RHEL 3 kerberos builds.

* Sun Nov 27 2005 Devrim GUNDUZ <devrim@PostgreSQL.org> 8.1.0-3PGDG
- re-added aconfver macro definition 

* Sun Nov 06 2005 Devrim GUNDUZ <devrim@PostgreSQL.org> 8.1.0-2PGDG
- Update JDBC jars to stable version 

* Sat Nov 05 2005 Devrim GUNDUZ <devrim@PostgreSQL.org> 8.1.0-1PGDG
- Update to 8.1.0 
- Updated JDBC jars
- Updated README.rpm-dist for 8.1
- added man1/reindexdb to files list.

* Sun Oct 30 2005 Devrim GUNDUZ <devrim@PostgreSQL.org> 8.1RC1-1PGDG 
- Update to 8.1RC1

* Thu Oct 19 2005 Devrim GUNDUZ <devrim@PostgreSQL.org> 8.1beta4-1PGDG 
- Update to 8.1beta4

* Thu Oct 19 2005 Devrim GUNDUZ <devrim@PostgreSQL.org> 8.1beta3-2PGDG 
- Fixed postgresql.pam file
- Fixed bug #167040, part 2

* Thu Oct 13 2005 Devrim GUNDUZ <devrim@PostgreSQL.org> 8.1beta3-1PGDG 
- Update to 8.1beta3
- Updated JDBC jars
- Updated rpm-pgsql.patch
- Include contrib/xml2 in build (bug #167492, Tom Lane)
- Add /etc/pam.d/postgresql (bug #167040 , Tom Lane)
- Add rpath to plperl.so (bug #162198 , Tom Lane)
- Adjust pgtcl link command to ensure it binds to correct libpq (bug #166665 , Tom Lane)

* Sun Sep 18 2005 Devrim GUNDUZ <devrim@PostgreSQL.org> 8.1beta2-1PGDG 
- Update to 8.1beta2

* Thu Sep 08 2005 Devrim GUNDUZ <devrim@PostgreSQL.org> 8.1beta1-6PGDG 
- Updated PyGreSQL from 3.6.2 to 3.7

* Sun Aug 28 2005 Devrim GUNDUZ <devrim@PostgreSQL.org> 8.1beta1-1..5PGDG
- Update to 8.1beta1
- Updated JDBC jars
- Updated postgresql-logging.patch
- Removed deprecated contrib entries
- Added old contrib entries that are moved to the core.
- Removed Python conflict check (bz#166754)
- Removed autoconf call

* Fri May 6 2005 Devrim GUNDUZ <devrim@PostgreSQL.org> 8.0.3-1PGDG
- Update to 8.0.3-1

* Tue Apr 19 2005 Devrim GUNDUZ <devrim@PostgreSQL.org> 8.0.2-2PGDG
- Update to 8.0.2-2
- Updated JDBC jars
- Updated PyGreSQL from 3.6.1 to 3.6.2.  

* Fri Apr 08 2005 Devrim GUNDUZ <devrim@PostgreSQL.org> 8.0.2-1PGDG
- Update to 8.0.2

* Mon Mar 28 2005 Devrim GUNDUZ <devrim@PostgreSQL.org> 8.0.2beta1-1PGDG
- Update to 8.0.2beta1
- Updated PyGreSQL from 3.6.1 to 3.6.2

* Wed Feb 23 2005 Devrim GUNDUZ <devrim@gunduz.org> 8.0.1-2PGDG
- Repair improper error message in init script when PGVERSION doesn't match. (Tom Lane)
- Arrange for auto update of version embedded in init script. (Tom Lane)
- Update JDBC jars

* Mon Jan 31 2005 Devrim GUNDUZ <devrim@gunduz.org> 8.0.1-1PGDG
- Added dependency for e2fsprogs-devel for krb5 builds (David Zambonini)
- Fix tcl build problems on Red Hat 8.0 (David Zambonini)
- Fixed krb5 builds (David Zambonini)
- Update to 8.0.1-1

* Tue Jan 18 2005 Devrim GUNDUZ <devrim@gunduz.org> 8.0.0-1PGDG
- Update to 8.0.0-1
- Updated JDBC Jars

* Sun Jan 16 2005 Devrim GUNDUZ <devrim@gunduz.org> 8.0.0rc5-4PGDG
- rc5
- Updated PyGreSQL from 3.6 to 3.6.1
- pgtcl 1.5.2 (per Tom Lane)
- Regression tests are run during RPM build (disabled by default) (Tom Lane)
- Postmaster stderr goes someplace useful, not /dev/null (bz#76503, #103767) (Tom Lane)
- Make init script return a useful exit status (bz#80782) (Tom Lane)
- Move docs' tutorial directory to %%{_libdir}/pgsql/tutorial, since it includes .so files that surely do not belong under /usr/share. (Tom Lane)

* Tue Jan 11 2005 Devrim GUNDUZ <devrim@gunduz.org> 8.0.0rc5-2PGDG
- pre-rc5
- Updated PyGreSQL from 3.5 to 3.6

* Fri Dec 03 2004 Devrim GUNDUZ <devrim@gunduz.org> 8.0.0rc1-2PGDG
- rc1-2PGDG
- Tag for PGDG
- Updated kerbdir
- Updated PyGreSQL from 3.4 to 3.5
- Updated doc files for PyGreSQL
- Modified if-endif lines for tcl&tcldevel prereq lines (per Red Hat RPMS)
- Applied getppid.patch as patch #4 (per Red Hat RPMS)
- Updated spec file to correct permissions for PyGreSQL permissions (per Red Hat RPMS)
- Updated preun and postun server scripts, per Red Hat RPMS


* Fri Dec 03 2004 Joe Conway <mail@joeconway.com> 8.0.0rc1-1JEC
- Updated for rc1
- Updated jdbc to latest beta (pg80b1.308*)

* Tue Nov 30 2004 Joe Conway <mail@joeconway.com> 8.0.0beta5-2JEC
- Fix init script to reflect version 8.0

* Mon Nov 22 2004 Joe Conway <mail@joeconway.com> 8.0.0beta5-1JEC
- Updated/adjusted for beta5
- Renamed to 8.0.0beta5-1JEC to avoid confusion with PGDG official releases

* Wed Aug 18 2004 Joe Conway <mail@joeconway.com> 8.0.0beta1-4PGDG
- Added back jdbc, per disscussion on HACKERS mailing list

* Tue Aug 17 2004 Joe Conway <mail@joeconway.com> 8.0.0beta1-3PGDG
- Fix init script; check for version 8.0, not 7.4

* Mon Aug 16 2004 Joe Conway <mail@joeconway.com> 8.0.0beta1-2PGDG
- Install missing file needed by initdb

* Sat Aug 14 2004 Joe Conway <mail@joeconway.com>
- 8.0.0beta1-1PGDG
- Update for 8.0.0beta1
- removed jdbc and tcl options

