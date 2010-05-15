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

%define beta 0

%{?beta:%define __os_install_post /usr/lib/rpm/brp-compress}

%{!?test:%define test 1}
%{!?pltcl:%define pltcl 1}
%{!?plperl:%define plperl 1}
%{!?pls:%define pls 1}
%{!?ssl:%define ssl 1}
%{!?kerberos:%define kerberos 1}
%{!?nls:%define nls 1}
%{!?pam:%define pam 1}
%{!?xml:%define xml 1}
%{!?pgfts:%define pgfts 0}
%{!?runselftest:%define runselftest 0}

Summary:   PostgreSQL client programs and libraries
Name:      postgresql
Version:   8.0.25

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
%define dist .fc12
Release:    1PGDG%{?dist}
License:   BSD
Group:      Applications/Databases
Source0:    ftp://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.bz2
Source3:    postgresql.init
Source4:    Makefile.regress
Source6:    README.rpm-dist
Source12:    http://www.postgresql.org/files/documentation/pdf/8.0/postgresql-8.0-A4.pdf
Source14:    postgresql.pam
Source15:    postgresql-bashprofile
Source16:    filter-requires-perl-Pg.sh
Source18:    ftp://ftp.pygresql.org/pub/distrib/PyGreSQL-3.8.1.tgz

Patch1:    rpm-pgsql.patch
Patch2:      postgresql-src-tutorial.patch
Patch3:      postgresql-logging.patch
Patch4:      postgresql-test.patch
Patch6:      postgresql-perl-rpath.patch

BuildRequires:   perl glibc-devel bison flex
Requires:   /sbin/ldconfig initscripts

%if %pltcl
BuildRequires:    tcl
%endif
%if %tcldevel
BuildRequires:    tcl-devel
%endif

BuildRequires:    readline-devel
BuildRequires:    zlib-devel >= 1.0.4

%if %ssl
BuildRequires:    openssl-devel
%endif

%if %kerberos
BuildRequires:   krb5-devel
BuildRequires:   e2fsprogs-devel
%endif

%if %nls
BuildRequires:   gettext >= 0.10.35
%endif

%if %pam
%if %non6xpamdeps
BuildRequires:   pam-devel
%endif
%endif

%if %xml
BuildRequires:   libxml2-devel libxslt-devel
%endif

Url:      http://www.postgresql.org/ 

Buildroot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

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

%if %pls
%package pl
Summary: The PL procedural languages for PostgreSQL.
Group: Applications/Databases
Requires: postgresql = %{version}
Requires: postgresql-server = %{version}

%description pl
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-pl package contains the the PL/Perl, and PL/Python
procedural languages for the backend.  PL/Pgsql is part of the core server package.
%endif

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
# patch5 is applied later
%patch6 -p1

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
%configure --disable-rpath \
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
   --datadir=/usr/share/pgsql \
   --with-docdir=%{_docdir}

make %{?_smp_mflags} all
make %{?_smp_mflags} -C contrib all
%if %xml
make %{?_smp_mflags} -C contrib/xml2 all
%endif

# Have to hack makefile to put correct path into tutorial scripts
sed "s|C=\`pwd\`;|C=%{_libdir}/pgsql/tutorial;|" < src/tutorial/Makefile > src/tutorial/GNUmakefile
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

install -d -m 755 %{buildroot}%{_libdir}/pgsql/tutorial
cp src/tutorial/* %{buildroot}%{_libdir}/pgsql/tutorial


if [ -d /etc/rc.d/init.d ]
then
   install -d %{buildroot}/etc/rc.d/init.d
   sed 's/^PGVERSION=.*$/PGVERSION=%{version}/' <%{SOURCE3} > postgresql.init
   install -m 755 postgresql.init %{buildroot}/etc/rc.d/init.d/postgresql
fi

%if %pam
if [ -d /etc/pam.d ]
then
   install -d %{buildroot}/etc/pam.d
   install -m 644 %{SOURCE14} %{buildroot}/etc/pam.d/postgresql
fi
%endif

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
   rm -f GNUmakefile Makefile
   popd
   cp %{SOURCE4} %{buildroot}/usr/lib/pgsql/test/regress/Makefile
   chmod 0644 %{buildroot}/usr/lib/pgsql/test/regress/Makefile
%endif

# Fix some more documentation
# gzip doc/internals.ps
cp %{SOURCE6} README.rpm-dist
mv %{buildroot}%{_docdir}/pgsql/html doc
rm -rf %{buildroot}%{_docdir}/pgsql

%find_lang libpq
%find_lang initdb
%find_lang pg_config
%find_lang pg_ctl
%find_lang pg_dump
%find_lang postgres
%find_lang psql
%find_lang pg_resetxlog
%find_lang pg_controldata
%find_lang pgscripts

cat libpq.lang > libpq.lst
cat pg_config.lang > pg_config.lst
cat initdb.lang pg_ctl.lang psql.lang pg_dump.lang pgscripts.lang > main.lst
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
if [ $1 -ge 1 ]; then
  /sbin/service postgresql condrestart >/dev/null 2>&1
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
%{_libdir}/pgsql/tutorial/

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
%{_libdir}/pgsql/pg_trgm.so
%{_libdir}/pgsql/refint.so
%{_libdir}/pgsql/rtree_gist.so
%{_libdir}/pgsql/seg.so
%{_libdir}/pgsql/string_io.so
%{_libdir}/pgsql/tablefunc.so
%{_libdir}/pgsql/timetravel.so
%{_libdir}/pgsql/tsearch.so
%{_libdir}/pgsql/tsearch2.so
%{_libdir}/pgsql/user_locks.so
%if %xml
%{_libdir}/pgsql/pgxml.so
%endif
%{_datadir}/pgsql/contrib/

%{_bindir}/DBMirror.pl
%{_bindir}/clean_pending.pl
%{_bindir}/my2pg.pl
%{_bindir}/mysql2pgsql
%{_bindir}/dbf2pg
%{_bindir}/findoidjoins
%{_bindir}/make_oidjoins_check
%{_bindir}/fti.pl
%{_bindir}/oid2name
%{_bindir}/pg_dumplo
%{_bindir}/pgbench
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
%if %pam
%config(noreplace) /etc/pam.d/postgresql
%endif
%attr (755,root,root) %dir /etc/sysconfig/pgsql
%attr (755,root,root) %dir /etc/sysconfig/pgsql/tsearch_data
%attr (755,root,root) %dir /etc/sysconfig/pgsql/timezonesets
%{_bindir}/initdb
%{_bindir}/ipcclean
%{_bindir}/pg_controldata
%{_bindir}/pg_ctl
%{_bindir}/pg_resetxlog
%{_bindir}/postgres
%{_bindir}/postmaster
%{_mandir}/man1/initdb.*
%{_mandir}/man1/ipcclean.*
%{_mandir}/man1/pg_controldata.*
%{_mandir}/man1/pg_ctl.*
%{_mandir}/man1/pg_resetxlog.*
%{_mandir}/man1/postgres.*
%{_mandir}/man1/postmaster.*
%{_datadir}/pgsql/postgres.bki
%{_datadir}/pgsql/postgres.description
%{_datadir}/pgsql/system_views.sql
%{_datadir}/pgsql/*.sample
%{_datadir}/pgsql/timezone/
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

%files devel -f pg_config.lst
%defattr(-,root,root)
/usr/include/*
%{_bindir}/ecpg
%{_bindir}/pg_config
%{_libdir}/libpq.so
%{_libdir}/libecpg.so
%{_libdir}/libpq.a
%{_libdir}/libecpg.a
%{_libdir}/libecpg_compat.so
%{_libdir}/libecpg_compat.a
%{_libdir}/libpgport.a
%{_libdir}/libpgtypes.so
%{_libdir}/libpgtypes.a
%{_libdir}/pgsql/pgxs/*
%{_mandir}/man1/ecpg.*
%{_mandir}/man1/pg_config.*

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
%endif

%if %test
%files test
%defattr(-,postgres,postgres)
%attr(-,postgres,postgres) /usr/lib/pgsql/test/*
%attr(-,postgres,postgres) %dir /usr/lib/pgsql/test
%endif

%changelog
* Sat May 15 2010 CMD RPM Packagers <packages@commandprompt.com> 8.0.25-1PGDG
- Update to 8.0.25

* Sun Mar 14 2010 CMD RPM Packagers <packages@commandprompt.com> 8.0.24-1PGDG
- Update to 8.0.24

* Thu Dec 10 2009 Devrim GUNDUZ <devrim@commandprompt.com> 8.0.23-1PGDG
- Update to 8.0.23, for various fixes described at
  http://www.postgresql.org/docs/8.0/static/release.html#RELEASE-8-0-23

* Wed Sep 09 2009 Devrim GUNDUZ <devrim@commandprompt.com> - 8.0.22-2PGDG
- Fix init script

* Thu Sep 3 2009 Devrim GUNDUZ <devrim@commandprompt.com> 8.0.22-1PGDG
- Update to 8.0.22

* Fri Mar 13 2009 Devrim GUNDUZ <devrim@commandprompt.com> 8.0.21-1PGDG
- Update to 8.0.21

* Fri Jan 30 2009 Devrim GUNDUZ <devrim@commandprompt.com> 8.0.20-1PGDG
- Update to 8.0.20

* Sat Nov 1 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.0.19-1PGDG
- Update to 8.0.19

* Fri Sep 19 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.0.18-1PGDG
- Update to 8.0.18

* Fri Aug 8 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.0.17-2PGDG
- Update pam file -- current file does not work on recent Fedora releases :-(

* Mon Jun 9 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.0.17-1PGDG
- Update to 8.0.17 (8.0.16 was skipped by upstream)

* Thu Jan 3 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.0.15-1PGDG
- Update to 8.0.15, which also includes security fixes for CVE-2007-4769, 
  CVE-2007-4772, CVE-2007-6067, CVE-2007-6600, CVE-2007-6601
- Update copyright date
- Remove autoconf calls

* Wed Oct 10 2007 Devrim GUNDUZ <devrim@commandprompt.com> 8.0.14-2PGDG
- Rebuilt

* Sat Sep 15 2007 Devrim GUNDUZ <devrim@commandprompt.com> 8.0.14-1PGDG
- Update to 8.0.14

* Sat Apr 21 2007 Devrim GUNDUZ <devrim@commandprompt.com> 8.0.13-1PGDG
- Update to 8.0.13

* Wed Feb 7 2007 Devrim GUNDUZ <devrim@commandprompt.com> 8.0.12-1PGDG
- Update to 8.0.12

* Sat Feb 3 2007 Devrim GUNDUZ <devrim@commandprompt.com> 8.0.11-1PGDG
- Update to 8.0.11

* Wed Jan 3 2007 Devrim GUNDUZ <devrim@commandprompt.com> 8.0.10-1PGDG
- Update to 8.0.10

* Fri Oct 14 2006 Devrim GUNDUZ <devrim@commandprompt.com> 8.0.9-3PGDG
- Remove Obsoletes
- Fixed rpmlint warnings and some of the errors
- Cosmetic cleanup
- Splitted python into a seperate rpm

* Fri Oct 06 2006 Devrim GUNDUZ <devrim@commandprompt.com> 8.0.9-2PGDG
- Splitted jdbc into a seperate rpm
- Splitted tcl into a seperate rpm

* Fri Oct 06 2006 Devrim GUNDUZ <devrim@commandprompt.com> 8.0.9-1PGDG
- Update to 8.0.9

* Tue Jun 06 2006 Devrim GUNDUZ <devrim@commandprompt.com> 8.0.8-2PGDG
- re-fix PyGreSQL filenames
- Updated JDBC jars to build 317
- Updated PyGreSQL from 3.8 to 3.8.1

* Mon May 22 2006 Devrim GUNDUZ <devrim@commandprompt.com> 8.0.8-1PGDG
- Updated JDBC jars to build 316
- Fix PyGreSQL filenames
- Update to 8.0.8

* Sun Feb 19 2006 Devrim GUNDUZ <devrim@commandprompt.com> 8.0.7-2PGDG
- Updated PyGreSQL from 3.7 to 3.8

* Mon Feb 13 2006 Devrim GUNDUZ <devrim@commandprompt.com> 8.0.7-1PGDG
- Update to 8.0.7

* Thu Feb 09 2006 Devrim GUNDUZ <devrim@commandprompt.com> 8.0.6-2PGDG
- Updated JDBC jars to build 315.

* Mon Jan 09 2006 Devrim GUNDUZ <devrim@commandprompt.com> 8.0.6-1PGDG
- 8.0.6-1

* Sun Dec 11 2005 Devrim GUNDUZ <devrim@commandprompt.com> 8.0.5-1PGDG
- 8.0.5-1
- Removed postgresql-elog.patch
- Re-added PDF documentation into RPM.

* Thu Dec 5 2005 Devrim GUNDUZ <devrim@PostgreSQL.org> 8.0.4-6PGDG
- 8.0.4-6
- Fix changelog
- Updated JDBC jars to build 314.
- Enabled tcl builds by default.

* Thu Dec 1 2005 Devrim GUNDUZ <devrim@PostgreSQL.org> 8.0.4-5PGDG
- 8.0.4-5
- Added a macro for RHEL 3 kerberos builds.

* Tue Oct 19 2005 Devrim GUNDUZ <devrim@PostgreSQL.org> 8.0.4-4PGDG
- 8.0.4-4
- Fixed postgresql.pam file
- Fixed bug #167040, part 2

* Tue Oct 4 2005 Devrim GUNDUZ <devrim@PostgreSQL.org> 8.0.4-3PGDG
- 8.0.4-3

* Tue Oct 4 2005 Devrim GUNDUZ <devrim@PostgreSQL.org> 8.0.4-2PGDG
- 8.0.4-2
- Add rpath to plperl.so (bug #162198 , Tom Lane)
- Adjust pgtcl link command to ensure it binds to correct libpq (bug #166665 , Tom Lane)
- Remove obsolete Conflicts: against other python versions (bug #166754 , Tom Lane)
- Add /etc/pam.d/postgresql (bug #167040 , Tom Lane)
- Include contrib/xml2 in build (bug #167492, Tom Lane)

* Tue Oct 4 2005 Devrim GUNDUZ <devrim@PostgreSQL.org> 8.0.4-1PGDG
- Update to 8.0.4-1 .
- Updated JDBC jars to build 312 .
- Updated PyGreSQL from 3.6.2 to 3.7 .

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
