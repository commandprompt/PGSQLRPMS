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
# Copyright 2003-2010 Devrim GÜNDÜZ <devrim@commandprompt.com>
# and others listed.

# Major Contributors:
# ---------------
# Lamar Owen
# Tom Lane
# Peter Eisentraut
# Alvaro Herrera
# David Fetter
# Greg Smith
# and others in the Changelog....

# This spec file and ancilliary files are licensed in accordance with 
# The PostgreSQL license.

# In this file you can find the default build package list macros.  These can be overridden by defining
# on the rpm command line:
# rpm --define 'packagename 1' .... to force the package to build.
# rpm --define 'packagename 0' .... to force the package NOT to build.
# The base package, the lib package, the devel package, and the server package always get built.

%define beta 0
%{?beta:%define __os_install_post /usr/lib/rpm/brp-compress}

%{!?kerbdir:%define kerbdir "/usr"}

# This is a macro to be used with find_lang and other stuff
%define majorversion 9.0
%define	pgbaseinstdir	/usr/pgsql-%{majorversion}

%{!?test:%define test 1}
%{!?plpython:%define plpython 1}
%{!?pltcl:%define pltcl 1}
%{!?plperl:%define plperl 1}
%{!?ssl:%define ssl 1}
%{!?intdatetimes:%define intdatetimes 1}
%{!?kerberos:%define kerberos 1}
%{!?nls:%define nls 1}
%{!?xml:%define xml 1}
%{!?pam:%define pam 1}
%{!?pgfts:%define pgfts 1}
%{!?runselftest:%define runselftest 1}
%{!?uuid:%define uuid 1}
%{!?ldap:%define ldap 1}

Summary:	PostgreSQL client programs and libraries
Name:		postgresql
Version:	9.0
Release:	alpha3_1PGDG%{?dist}
License:	BSD
Group:		Applications/Databases
Url:		http://www.postgresql.org/ 

Source0:	ftp://ftp.postgresql.org/pub/source/%{version}alpha3/postgresql-%{version}alpha3.tar.bz2
Source3:	postgresql.init
Source4:	Makefile.regress
Source5:	pg_config.h
Source6:	README.rpm-dist
Source7:	ecpg_config.h
Source12:	http://www.postgresql.org/files/documentation/pdf/%{majorversion}/postgresql-%{version}alpha3-A4.pdf
Source14:	postgresql.pam
Source15:	postgresql-bashprofile
Source16:	filter-requires-perl-Pg.sh

Patch1:		rpm-pgsql.patch
Patch3:		postgresql-logging.patch
Patch6:		postgresql-perl-rpath.patch

Buildrequires:	perl glibc-devel bison flex >= 2.5.31
Requires:	/sbin/ldconfig initscripts

%if %plperl
BuildRequires:	perl-ExtUtils-Embed
%endif

%if %plpython
BuildRequires:	python-devel
%endif

%if %pltcl
BuildRequires:	tcl-devel
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

%if %uuid
BuildRequires:	uuid-devel
%endif

%if %ldap
BuildRequires:	openldap-devel
%endif

Requires:	postgresql-libs = %{version}-%{release}

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

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
server over a network connection. This package contains the command-line 
utilities for managing PostgreSQL databases on a PostgreSQL server. 

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
Requires:	postgresql = %{version}-%{release}
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
project, or if you want to generate printed documentation. This package also 
includes HTML version of the documentation.

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
Requires:	postgresql = %{version}-%{release}

%description devel
The postgresql-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with a PostgreSQL database management server and the ecpg Embedded C
Postgres preprocessor. You need to install this package if you want to
develop applications which will interact with a PostgreSQL server. 

%if %plperl
%package plperl
Summary:	The Perl procedural language for PostgreSQL
Group:		Applications/Databases
Requires:	postgresql-server = %{version}-%{release}
%ifarch ppc ppc64
BuildRequires:  perl-devel
%endif
Obsoletes:	postgresql-pl

%description plperl
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-plperl package contains the PL/Perl language
for the backend.
%endif

%if %plpython
%package plpython
Summary:	The Python procedural language for PostgreSQL
Group:		Applications/Databases
Requires:	postgresql = %{version}
Requires:	postgresql-server = %{version}
Obsoletes:	postgresql-pl

%description plpython
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-plpython package contains the PL/Python language
for the backend.
%endif

%if %pltcl
%package pltcl
Summary:	The Tcl procedural language for PostgreSQL
Group:		Applications/Databases
Requires:	postgresql = %{version}
Requires:	postgresql-server = %{version}
Obsoletes:	postgresql-pl

%description pltcl
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-pltcl package contains the PL/Tcl language
for the backend.
%endif

%if %test
%package test
Summary:	The test suite distributed with PostgreSQL
Group:		Applications/Databases
Requires:	postgresql-server = %{version}-%{release}

%description test
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-test package includes the sources and pre-built
binaries of various tests for the PostgreSQL database management
system, including regression tests and benchmarks.
%endif

%define __perl_requires %{SOURCE16}

%prep
%setup -q -n %{name}-%{version}alpha3
%patch1 -p1
%patch3 -p1
# patch5 is applied later
%patch6 -p1

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

# Use --as-needed to eliminate unnecessary link dependencies.
# Hopefully upstream will do this for itself in some future release.
LDFLAGS="-Wl,--as-needed"; export LDFLAGS

export LIBNAME=%{_lib}
./configure --disable-rpath \
	--prefix=%{pgbaseinstdir} \
	--includedir=%{pgbaseinstdir}/include \
	--mandir=%{pgbaseinstdir}/share/man \
	--datadir=%{pgbaseinstdir}/share \
%if %beta
	--enable-debug \
	--enable-cassert \
%endif
%if %plperl
	--with-perl \
%endif
%if %plpython
	--with-python \
%endif
%if %pltcl
	--with-tcl \
	--with-tclconfig=%{_libdir} \
%endif
%if %ssl
	--with-openssl \
%endif
%if %pam
	--with-pam \
%endif
%if %kerberos
	--with-krb5 \
	--with-gssapi \
	--with-includes=%{kerbdir}/include \
	--with-libraries=%{kerbdir}/%{_lib} \
%endif
%if %nls
	--enable-nls \
%endif
%if !%intdatetimes
	--disable-integer-datetimes \
%endif
%if %pgfts
	--enable-thread-safety \
%endif
%if %uuid
	--with-ossp-uuid \
%endif
%if %xml
	--with-libxml \
	--with-libxslt \
%endif
%if %ldap
	--with-ldap \
%endif
	--with-system-tzdata=%{_datadir}/zoneinfo \
	--sysconfdir=/etc/sysconfig/pgsql \
	--with-docdir=%{_docdir}

make %{?_smp_mflags} all
make %{?_smp_mflags} -C contrib all
%if %uuid
make %{?_smp_mflags} -C contrib/uuid-ossp all
%endif

# Have to hack makefile to put correct path into tutorial scripts
sed "s|C=\`pwd\`;|C=%{pgbaseinstdir}/lib/tutorial;|" < src/tutorial/Makefile > src/tutorial/GNUmakefile
make %{?_smp_mflags} -C src/tutorial NO_PGXS=1 all
rm -f src/tutorial/GNUmakefile

%if %runselftest
	pushd src/test/regress
	make all
	cp ../../../contrib/spi/refint.so .
	cp ../../../contrib/spi/autoinc.so .
	make MAX_CONNECTIONS=5 check
	make clean
	popd
%endif

%if %test
	pushd src/test/regress
	make all
	popd
%endif

%install
rm -rf %{buildroot}

make DESTDIR=%{buildroot} install
make -C contrib DESTDIR=%{buildroot} install
%if %uuid
make -C contrib/uuid-ossp DESTDIR=%{buildroot} install
%endif

# multilib header hack; note pg_config.h is installed in two places!
# we only apply this to known Red Hat multilib arches, per bug #177564
case `uname -i` in
	i386 | x86_64 | ppc | ppc64 | s390 | s390x)
		mv %{buildroot}%{pgbaseinstdir}/include/pg_config.h %{buildroot}%{pgbaseinstdir}/include/pg_config_`uname -i`.h
		install -m 644 %{SOURCE5} %{buildroot}%{pgbaseinstdir}/include/
		mv %{buildroot}%{pgbaseinstdir}/include/server/pg_config.h %{buildroot}%{pgbaseinstdir}/include/server/pg_config_`uname -i`.h
		install -m 644 %{SOURCE5} %{buildroot}%{pgbaseinstdir}/include/server/
		mv %{buildroot}%{pgbaseinstdir}/include/ecpg_config.h %{buildroot}%{pgbaseinstdir}/include/ecpg_config_`uname -i`.h
		install -m 644 %{SOURCE7} %{buildroot}%{pgbaseinstdir}/include/
		;;
	*)
	;;
esac

install -d %{buildroot}/etc/rc.d/init.d
sed 's/^PGVERSION=.*$/PGVERSION=%{version}/' <%{SOURCE3} > postgresql.init
install -m 755 postgresql.init %{buildroot}/etc/rc.d/init.d/postgresql-%{majorversion}

%if %pam
install -d %{buildroot}/etc/pam.d
install -m 644 %{SOURCE14} %{buildroot}/etc/pam.d/postgresql
%endif

# PGDATA needs removal of group and world permissions due to pg_pwd hole.
install -d -m 700 %{buildroot}/var/lib/pgsql/%{majorversion}/data

# backups of data go here...
install -d -m 700 %{buildroot}/var/lib/pgsql/%{majorversion}/backups

# postgres' .bash_profile
install -m 644 %{SOURCE15} %{buildroot}/var/lib/pgsql/.bash_profile

# Create the multiple postmaster startup directory
install -d -m 700 %{buildroot}/etc/sysconfig/pgsql/%{majorversion}

%if %test
	# tests. There are many files included here that are unnecessary,
	# but include them anyway for completeness.  We replace the original
	# Makefiles, however.
	mkdir -p %{buildroot}%{pgbaseinstdir}/lib/test
	cp -a src/test/regress %{buildroot}%{pgbaseinstdir}/lib/test
	install -m 0755 contrib/spi/refint.so %{buildroot}%{pgbaseinstdir}/lib/test/regress
	install -m 0755 contrib/spi/autoinc.so %{buildroot}%{pgbaseinstdir}/lib/test/regress
	pushd  %{buildroot}%{pgbaseinstdir}/lib/test/regress
	strip *.so
	rm -f GNUmakefile Makefile *.o
	popd
	cp %{SOURCE4} %{buildroot}%{pgbaseinstdir}/lib/test/regress/Makefile
	chmod 0644 %{buildroot}%{pgbaseinstdir}/lib/test/regress/Makefile
%endif

# Fix some more documentation
# gzip doc/internals.ps
cp %{SOURCE6} README.rpm-dist
mv %{buildroot}%{pgbaseinstdir}/share/doc/html doc
rm -rf %{buildroot}%{_docdir}/pgsql

%find_lang ecpg-%{majorversion}
%find_lang ecpglib6-%{majorversion}
%find_lang initdb-%{majorversion}
%find_lang libpq5-%{majorversion}
%find_lang pg_config-%{majorversion}
%find_lang pg_controldata-%{majorversion}
%find_lang pg_ctl-%{majorversion}
%find_lang pg_dump-%{majorversion}
%find_lang pg_resetxlog-%{majorversion}
%find_lang pgscripts-%{majorversion}
%find_lang plperl-%{majorversion}
%find_lang plpgsql-%{majorversion}
%find_lang plpython-%{majorversion}
%find_lang pltcl-%{majorversion}
%find_lang postgres-%{majorversion}
%find_lang psql-%{majorversion}

cat libpq5-%{majorversion}.lang > pg_libpq5.lst
cat pg_config-%{majorversion}.lang ecpg-%{majorversion}.lang ecpglib6-%{majorversion}.lang > pg_devel.lst
cat initdb-%{majorversion}.lang pg_ctl-%{majorversion}.lang psql-%{majorversion}.lang pg_dump-%{majorversion}.lang pgscripts-%{majorversion}.lang > pg_main.lst
cat postgres-%{majorversion}.lang pg_resetxlog-%{majorversion}.lang pg_controldata-%{majorversion}.lang plpgsql-%{majorversion}.lang > pg_server.lst
cat plperl-%{majorversion}.lang > pg_plperl.lst
cat pltcl-%{majorversion}.lang > pg_pltcl.lst
cat plpython-%{majorversion}.lang > pg_plpython.lst

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
	/sbin/service postgresql-9.0 condstop >/dev/null 2>&1
	chkconfig --del postgresql-9.0
fi

%postun server
/sbin/ldconfig 
if [ $1 -ge 1 ]; then
  /sbin/service postgresql-9.0 condrestart >/dev/null 2>&1
fi

%if %plperl
%post 	-p /sbin/ldconfig	plperl
%postun	-p /sbin/ldconfig 	plperl
%endif

%if %plpython
%post 	-p /sbin/ldconfig	plpython
%postun	-p /sbin/ldconfig 	plpython
%endif

%if %pltcl
%post 	-p /sbin/ldconfig	pltcl
%postun	-p /sbin/ldconfig 	pltcl
%endif

%if %test
%post test
chown -R postgres:postgres /usr/share/pgsql/test >/dev/null 2>&1 || :
%endif

# Create alternatives entries for common binaries:
%post
alternatives --install /usr/bin/psql psql /usr/pgsql-9.0/bin/psql 900
alternatives --install /usr/bin/pg_dump pg_dump /usr/pgsql-9.0/bin/pg_dump 900
alternatives --install /usr/bin/pg_dumpall pg_dumpall /usr/pgsql-9.0/bin/pg_dumpall 900

# Drop alternatives entries for common binaries:
%postun
alternatives --remove psql /usr/pgsql-9.0/bin/psql
alternatives --remove pg_dump /usr/pgsql-9.0/bin/pg_dump
alternatives --remove pg_dumpall /usr/pgsql-9.0/bin/pg_dumpall

%clean
rm -rf %{buildroot}

# FILES section.

%files -f pg_main.lst
%defattr(-,root,root)
%doc doc/KNOWN_BUGS doc/MISSING_FEATURES doc/README* 
%doc COPYRIGHT README doc/bug.template
%doc README.rpm-dist
%{pgbaseinstdir}/bin/clusterdb
%{pgbaseinstdir}/bin/createdb
%{pgbaseinstdir}/bin/createlang
%{pgbaseinstdir}/bin/createuser
%{pgbaseinstdir}/bin/dropdb
%{pgbaseinstdir}/bin/droplang
%{pgbaseinstdir}/bin/dropuser
%{pgbaseinstdir}/bin/pg_dump
%{pgbaseinstdir}/bin/pg_dumpall
%{pgbaseinstdir}/bin/pg_restore
%{pgbaseinstdir}/bin/psql
%{pgbaseinstdir}/bin/reindexdb
%{pgbaseinstdir}/bin/vacuumdb
%{pgbaseinstdir}/share/man/man1/clusterdb.*
%{pgbaseinstdir}/share/man/man1/createdb.*
%{pgbaseinstdir}/share/man/man1/createlang.*
%{pgbaseinstdir}/share/man/man1/createuser.*
%{pgbaseinstdir}/share/man/man1/dropdb.*
%{pgbaseinstdir}/share/man/man1/droplang.*
%{pgbaseinstdir}/share/man/man1/dropuser.*
%{pgbaseinstdir}/share/man/man1/pg_dump.*
%{pgbaseinstdir}/share/man/man1/pg_dumpall.*
%{pgbaseinstdir}/share/man/man1/pg_restore.*
%{pgbaseinstdir}/share/man/man1/psql.*
%{pgbaseinstdir}/share/man/man1/reindexdb.*
%{pgbaseinstdir}/share/man/man1/vacuumdb.*
%{pgbaseinstdir}/share/man/man3/*
%{pgbaseinstdir}/share/man/man7/*

%files docs
%defattr(-,root,root)
%doc doc/src/*
%doc *-A4.pdf
%doc src/tutorial
%doc doc/html

%files contrib
%defattr(-,root,root)
%{pgbaseinstdir}/lib/_int.so
%{pgbaseinstdir}/lib/adminpack.so
%{pgbaseinstdir}/lib/autoinc.so
%{pgbaseinstdir}/lib/auto_explain.so
%{pgbaseinstdir}/lib/btree_gin.so
%{pgbaseinstdir}/lib/btree_gist.so
%{pgbaseinstdir}/lib/chkpass.so
%{pgbaseinstdir}/lib/citext.so
%{pgbaseinstdir}/lib/cube.so
%{pgbaseinstdir}/lib/dblink.so
%{pgbaseinstdir}/lib/earthdistance.so
%{pgbaseinstdir}/lib/euc2004_sjis2004.so
%{pgbaseinstdir}/lib/fuzzystrmatch.so
%{pgbaseinstdir}/lib/insert_username.so
%{pgbaseinstdir}/lib/isn.so
%{pgbaseinstdir}/lib/hstore.so
%{pgbaseinstdir}/lib/passwordcheck.so
%{pgbaseinstdir}/lib/pg_freespacemap.so
%{pgbaseinstdir}/lib/pg_stat_statements.so
%{pgbaseinstdir}/lib/pgrowlocks.so
%{pgbaseinstdir}/lib/plpython2.soo
%{pgbaseinstdir}/lib/sslinfo.so
%{pgbaseinstdir}/lib/lo.so
%{pgbaseinstdir}/lib/ltree.so
%{pgbaseinstdir}/lib/moddatetime.so
%{pgbaseinstdir}/lib/pageinspect.so
%{pgbaseinstdir}/lib/pgcrypto.so
%{pgbaseinstdir}/lib/pgstattuple.so
%{pgbaseinstdir}/lib/pg_buffercache.so
%{pgbaseinstdir}/lib/pg_trgm.so
%{pgbaseinstdir}/lib/refint.so
%{pgbaseinstdir}/lib/seg.so
%{pgbaseinstdir}/lib/tablefunc.so
%{pgbaseinstdir}/lib/timetravel.so
%{pgbaseinstdir}/lib/unaccent.so
%if %xml
%{pgbaseinstdir}/lib/pgxml.so
%endif
%if %uuid
%{pgbaseinstdir}/lib/uuid-ossp.so
%endif
%{pgbaseinstdir}/share/contrib/
%{pgbaseinstdir}/bin/oid2name
%{pgbaseinstdir}/bin/pgbench
%{pgbaseinstdir}/bin/vacuumlo
%{pgbaseinstdir}/bin/pg_standby
%doc %{pgbaseinstdir}/share/doc/contrib/*.example 
%doc %{pgbaseinstdir}/share/contrib/*.sql

%files libs -f pg_libpq5.lst
%defattr(-,root,root)
%{pgbaseinstdir}/lib/libpq.so.*
%{pgbaseinstdir}/lib/libecpg.so*
%{pgbaseinstdir}/lib/libpgtypes.so.*
%{pgbaseinstdir}/lib/libecpg_compat.so.*

%files server -f pg_server.lst
%defattr(-,root,root)
/etc/rc.d/init.d/postgresql-%{majorversion}
%if %pam
%config(noreplace) /etc/pam.d/postgresql
%endif
%attr (755,root,root) %dir /etc/sysconfig/pgsql
%{pgbaseinstdir}/bin/initdb
%{pgbaseinstdir}/bin/pg_controldata
%{pgbaseinstdir}/bin/pg_ctl
%{pgbaseinstdir}/bin/pg_resetxlog
%{pgbaseinstdir}/bin/postgres
%{pgbaseinstdir}/bin/postmaster
%{pgbaseinstdir}/share/man/man1/initdb.*
%{pgbaseinstdir}/share/man/man1/pg_controldata.*
%{pgbaseinstdir}/share/man/man1/pg_ctl.*
%{pgbaseinstdir}/share/man/man1/pg_resetxlog.*
%{pgbaseinstdir}/share/man/man1/postgres.*
%{pgbaseinstdir}/share/man/man1/postmaster.*
%{pgbaseinstdir}/share/postgres.bki
%{pgbaseinstdir}/share/postgres.description
%{pgbaseinstdir}/share/postgres.shdescription
%{pgbaseinstdir}/share/system_views.sql
%{pgbaseinstdir}/share/*.sample
%{pgbaseinstdir}/share/timezonesets/*
%{pgbaseinstdir}/share/tsearch_data/*.affix
%{pgbaseinstdir}/share/tsearch_data/*.dict
%{pgbaseinstdir}/share/tsearch_data/*.ths
%{pgbaseinstdir}/share/tsearch_data/*.rules
%{pgbaseinstdir}/share/tsearch_data/*.stop
%{pgbaseinstdir}/share/tsearch_data/*.syn
%{pgbaseinstdir}/lib/dict_int.so
%{pgbaseinstdir}/lib/dict_snowball.so
%{pgbaseinstdir}/lib/dict_xsyn.so
%{pgbaseinstdir}/lib/plpgsql.so
%{pgbaseinstdir}/lib/test_parser.so
%{pgbaseinstdir}/lib/tsearch2.so

%dir %{pgbaseinstdir}/lib
%dir %{pgbaseinstdir}/share
%attr(700,postgres,postgres) %dir /var/lib/pgsql
%attr(700,postgres,postgres) %dir /var/lib/pgsql/%{majorversion}
%attr(700,postgres,postgres) %dir /var/lib/pgsql/%{majorversion}/data
%attr(700,postgres,postgres) %dir /var/lib/pgsql/%{majorversion}/backups
%attr(644,postgres,postgres) %config(noreplace) /var/lib/pgsql/.bash_profile
%{pgbaseinstdir}/lib/*_and_*.so
%{pgbaseinstdir}/share/conversion_create.sql
%{pgbaseinstdir}/share/information_schema.sql
%{pgbaseinstdir}/share/snowball_create.sql
%{pgbaseinstdir}/share/sql_features.txt

%files devel -f pg_devel.lst
%defattr(-,root,root)
%{pgbaseinstdir}/include/*
%{pgbaseinstdir}/bin/ecpg
%{pgbaseinstdir}/bin/pg_config
%{pgbaseinstdir}/lib/libpq.so
%{pgbaseinstdir}/lib/libecpg.so
%{pgbaseinstdir}/lib/libpq.a
%{pgbaseinstdir}/lib/libecpg.a
%{pgbaseinstdir}/lib/libecpg_compat.so
%{pgbaseinstdir}/lib/libecpg_compat.a
%{pgbaseinstdir}/lib/libpgport.a
%{pgbaseinstdir}/lib/libpgtypes.so
%{pgbaseinstdir}/lib/libpgtypes.a
%{pgbaseinstdir}/lib/pgxs/*
%{pgbaseinstdir}/share/man/man1/ecpg.*
%{pgbaseinstdir}/share/man/man1/pg_config.*

%if %plperl
%files plperl -f pg_plperl.lst
%defattr(-,root,root)
%{pgbaseinstdir}/lib/plperl.so
%endif

%if %pltcl
%files pltcl -f pg_pltcl.lst
%defattr(-,root,root)
%{pgbaseinstdir}/lib/pltcl.so
%{pgbaseinstdir}/bin/pltcl_delmod
%{pgbaseinstdir}/bin/pltcl_listmod
%{pgbaseinstdir}/bin/pltcl_loadmod
%{pgbaseinstdir}/share/unknown.pltcl
%endif

%if %plpython
%files plpython -f pg_plpython.lst
%defattr(-,root,root)
%{pgbaseinstdir}/lib//plpython.so
%endif

%if %test
%files test
%defattr(-,postgres,postgres)
%attr(-,postgres,postgres) %{pgbaseinstdir}/lib/test/*
%attr(-,postgres,postgres) %dir %{pgbaseinstdir}/lib/test
%endif

%changelog
* Tue Dec 29 2009 Devrim GUNDUZ <devrim@commandprompt.com> 8.5alpha3-1PGDG
- Update to 8.5 Alpha3

* Wed Oct 28 2009 Devrim GUNDUZ <devrim@commandprompt.com> 8.5alpha2-1PGDG
- Update to 8.5	Alpha2

* Tue Aug 25 2009 Devrim GUNDUZ <devrim@commandprompt.com> 8.5alpha1-2PGDG
- More fixes for multiple version installation.

* Mon Aug 24 2009 Devrim GUNDUZ <devrim@commandprompt.com> 8.5alpha1-1PGDG
- Initial cut for 8.5 Alpha 1, which supports multiple version installation.
  WARNING: This is for testing only.

* Sat Jun 27 2009 Devrim GUNDUZ <devrim@commandprompt.com> 8.4.0-1PGDG
- Update to 8.4.0

* Tue Jun 23 2009 Devrim GUNDUZ <devrim@commandprompt.com> 8.4rc2-1PGDG
- Update to 8.4 rc2

* Sun Jun 14 2009 Devrim GUNDUZ <devrim@commandprompt.com> 8.4rc1-1PGDG
- Update to 8.4 rc1   

* Sat May 16 2009 Devrim GUNDUZ <devrim@commandprompt.com> 8.4beta2-1PGDG
- Update to 8.4 beta 2

* Fri Apr 10 2009 Devrim GUNDUZ <devrim@commandprompt.com> 8.4beta1-1PGDG
- Update to 8.4 beta1
- Remove buildrhel3 macro

* Fri Mar 27 2009 Devrim GUNDUZ <devrim@commandprompt.com> 8.4devel_20090327-1PGDG
- Update to Mar 27 2009 CVS snapshot

* Tue Mar 10 2009 Devrim GUNDUZ <devrim@commandprompt.com> 8.4devel_20090310-1PGDG
- Update to Mar 10, 2009 CVS snapshot

* Mon Jan 5 2009 Devrim GUNDUZ <devrim@commandprompt.com> 8.4devel_20090105-1PGDG
- Update to Jan 5, 2009 CVS snapshot

* Mon Dec 29 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.4devel_20081229-1PGDG
- Update to Dec 29, 2008 CVS snapshot
- Update spec for new translation layout.
- Update spec for new files.

* Thu Dec 4 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.4devel_20081204-1PGDG
- Update to Dec 04, 2008 CVS snapshot

* Fri Nov 28 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.4devel_20081128-1PGDG
- Update to Nov 28, 2008 CVS snapshot
- We now buildrequire perl-ExtUtils-Embed for plperl.

* Wed Nov 26 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.4devel_20081126-1PGDG
- Update to Nov 26, 2008 CVS snapshot

* Wed Nov 19 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.4devel_20081119-1PGDG
- Update to Nov 19, 2008 CVS snapshot, to test auto-contrib module.

* Tue Nov 18 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.4devel_20081118-1PGDG
- Update to Nov 18, 2008 CVS snapshot, and fix spec file for that.
- Fix version number, so that yum can pick up updates, per Guillaume Smet.

* Thu Nov 13 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.4devel_13112008-1PGDG
- Update to Nov 13  2008 CVS snapshot

* Sat Oct 11 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.4devel_11102008-1PGDG
- Update to Oct 11 2008 CVS snapshot
- Add plpgsql translations.

* Mon Sep 29 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.4devel_29092008-1PGDG
- Update to Sep 29 2008 CVS snapshot

* Mon Sep 15 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.4devel_15092008-1PGDG
- Update to Sep 15 2008 CVS snapshot

* Mon Sep 8 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.4devel_07092008-2PGDG
- Use intdatetimes macro properly.

* Sun Sep 7 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.4devel_07092008-1PGDG
- Update to Sep 7 2008 CVS snapshot 

* Fri Sep 5 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.4devel_03092008-2PGDG
- Enable integer datetimes by default. This is a 8.4+ change.

* Wed Sep 3 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.4devel_03092008-1PGDG
- Initial cut for 8.4devel, Sep 3 2008 CVS snapshot
- Remove patch4, it is already in 8.4
- Update logging patch, so that logs will be rotated weekly.

* Fri Aug 8 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.3.3-2PGDG
- Update pam file -- current file does not work on recent Fedora releases :-(
- Remove patch8 -- it is no longer needed in recent Fedora releases. Per Tom.

* Mon Jun 9 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.3.3-1PGDG
- Update to 8.3.3 (8.3.2 was skipped by upstream)
- Re-enable uuid for F-9

* Thu Mar 13 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.3.1-2PGDG
- Enable LDAP support, per gripe from Bartek Siebab.
- Use -Wl,--as-needed to suppress bogus dependencies for libraries that
  are really only needed by some of the subpackages, per Fedora package.
- Clean up cross-subpackage Requires: to ensure that updating any one
  subpackage brings in the matching versions of others.
  Resolves: #444271, per Fedora spec.

* Thu Mar 13 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.3.1-1PGDG
- Update to 8.3.1

* Tue Feb 5 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.3.0-2PGDG
- Enable the new GSSAPI support in 8.3, per reminder from Tom.

* Fri Feb 1 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.3.0-1PGDG
- Update to 8.3.0 
- Update PDF docs to 8.3.0 
- Set selftest to on by default.
- Fix test routines, per Red Hat spec file.
- Remove RHL 9 calls, and update supported platforms list.
- Make initscript and pam config files be installed unconditionally;
  seems new buildroots don't necessarily have those directories in 
  place, per Red Hat RPMs

* Tue Jan 29 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.3RC2-2PGDG
- Fix xml builds -- it was broken since first 8.3 package was built. 
  Per report from Steve Woodcock.

* Fri Jan 18 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.3RC2-1PGDG
- Update to 8.3 RC2

* Thu Jan 3 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.3RC1-1PGDG
- Update to 8.3 RC1, which also includes security fixes for CVE-2007-4769,
  CVE-2007-4772, CVE-2007-6067, CVE-2007-6600, CVE-2007-6601
- Update copyright date
- Remove autoconf related lines (they are already unused)

* Thu Dec 06 2007 Devrim GUNDUZ <devrim@commandprompt.com> 8.3beta4-2PGDG
- Set uuid default to 0. RHEL 4 does not have uuid package. RHEL 5 has 
  in EPEL repository. 

* Sun Dec 02 2007 Devrim GUNDUZ <devrim@commandprompt.com> 8.3beta4-1PGDG
- Update to beta4
- Fix uuid builds

* Sun Nov 16 2007 Devrim GUNDUZ <devrim@commandprompt.com> 8.3beta3-1PGDG
- Update to beta3
- Trim changelog.

* Sun Nov 04 2007 Devrim GUNDUZ <devrim@commandprompt.com> 8.3beta2-3PGDG
- Added a new macro for --enable-integer-datetimes. It is disabled by default.

* Tue Oct 30 2007 Devrim GUNDUZ <devrim@commandprompt.com> 8.3beta2-2PGDG
- Add a macro for contrib/uuid-ossp and set it to 1

* Sat Oct 26 2007 Devrim GUNDUZ <devrim@commandprompt.com> 8.3beta2-1PGDG
- Update to beta2 and fix spec file for beta2
- Use perl-devel requirement only for ppc* arches (older RHEL releases
  does not have perl-devel, so we needed this workaround)

* Mon Oct 15 2007 Devrim GUNDUZ <devrim@commandprompt.com> 8.3beta1-4PGDG
- Build requires perl-devel, per failure on ppc64 builds.

* Wed Oct 10 2007 Devrim GUNDUZ <devrim@commandprompt.com> 8.3beta1-3PGDG
- Merged latest changes from 8.2 spec file (Synced with Fedora's spec file. 
  All fixes and patches are from Tom Lane) :
   * Fix multilib problem for /usr/include/ecpg_config.h (which is new in 8.2.x)
   * Use nicer solution for tzdata file substitution: upstream discussion
   concluded that hardwiring the path was better than a symlink after all.
   * Don't remove postgres user/group during RPM uninstall, per Fedora
   packaging guidelines
- Added new configuration option: --with-system-tzdata

* Mon Oct 8 2007 Devrim GUNDUZ <devrim@commandprompt.com> 8.3beta1-2PGDG
- Added dist macro 

* Fri Oct 5 2007 Devrim GUNDUZ <devrim@commandprompt.com> 8.3beta1-1PGDG
- Update to 8.3beta1
- Updates to spec file for 8.3 changes

* Tue Jun 5 2007 Devrim GUNDUZ <devrim@commandprompt.com> 8.3devel-1PGDG
- Initial cut for 8.3devel
