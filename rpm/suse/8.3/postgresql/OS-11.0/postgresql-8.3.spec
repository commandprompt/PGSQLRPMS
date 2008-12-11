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
# Copyright 2008-2009 Devrim GUNDUZ <devrim@gunduz.org> and others listed.
#
# This spec file and ancilliary files are licensed in accordance with
# The PostgreSQL license.

# In this file you can find the default build package list macros.  These can be overridden by defining
# on the rpm command line:
# rpm --define 'packagename 1' .... to force the package to build.
# rpm --define 'packagename 0' .... to force the package NOT to build.
# The base package, the lib package, the devel package, and the server package always get built.

%define beta 0
%{?beta:%define __os_install_post /usr/lib/rpm/brp-compress}

%define pg_minor_version %(echo %version | cut -f1-2 -d.)

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
%{!?uuid:%define uuid 0}
%{!?ldap:%define ldap 1}

Name:		postgresql
Summary:	Basic Clients and Utilities for PostgreSQL
Url:		http://www.postgresql.org/
Version:	8.3.5
Release:	1PGDG%{?dist}
License:	BSD 3-Clause
Group:		Productivity/Databases/Tools
Source0:	ftp://ftp.postgresql.org/pub/source/v%{version}/postgresql-%version.tar.bz2
Source2:	postgresql-README.SuSE.de
Source3:	postgresql-README.SuSE.en
Source8:	postgresql-sysconfig
Source9:	postgresql-init
Source15:	postgresql-bashprofile
Source16:	postgresql-firewall
Source17:	postgresql-rpmlintrc
Patch1:		postgresql-8.3-conf.patch
PreReq:		postgresql-libs = %pg_minor_version
BuildRequires:	bison flex
BuildRequires:	readline-devel zlib-devel
BuildRequires:	ncurses-devel
Provides:	postgresql = %pg_minor_version
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%if %kerberos
BuildRequires:  krb5-devel
%endif

%if %ldap
BuildRequires:  openldap2-devel
%endif

%if %nls
BuildRequires:  gettext-devel
%endif

%if %pam
BuildRequires:  pam-devel
%endif

%if %plpython
BuildRequires:  python-devel
%endif

%if %pltcl
BuildRequires:  tcl-devel
%endif

%if %ssl
BuildRequires:  openssl-devel
%endif

%if %xml
BuildRequires:  libxml2-devel libxslt-devel
%endif

%description
PostgreSQL is an advanced object-relational database management system
that supports an extended subset of the SQL standard, including
transactions, foreign keys, subqueries, triggers, and user-defined
types and functions.

This package contains the basic utility and client programs necessary
to maintain and work with local or remote PostgreSQL databases as well
as manual pages for the SQL commands that PostgreSQL supports. Full
HTML documentation for PostgreSQL can be found in the postgresql-docs
package.

%package libs
License:	BSD 3-Clause
Summary:	Shared Libraries Required for PostgreSQL Clients
Group:		Productivity/Databases/Clients
Provides:	postgresql-libs = %pg_minor_version
PreReq:		sh-utils fileutils

%description libs
PostgreSQL is an advanced object-relational database management system
that supports an extended subset of the SQL standard, including
transactions, foreign keys, subqueries, triggers, user-defined types
and functions.

This package provides the essential shared libraries for (almost) any
PostgreSQL client program or interface. You will need to install this
package in order to use any other PostgreSQL package or any clients
that need to connect to a PostgreSQL server.

%if %plperl
%package plperl
License:	BSD 3-Clause
Summary:	The Perl procedural language for PostgreSQL
Group:		Productivity/Databases/Clients
Provides:	plperl.so
Requires:	postgresql-server = %{version}-%{release}

%description plperl
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-plperl package contains the PL/Perl language
for the backend.
%endif

%if %plpython
%package plpython
License:	BSD 3-Clause
Summary:	The Python procedural language for PostgreSQL
Group:		Productivity/Databases/Clients
Provides:	plpython.so

%description plpython
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-plpython package contains the PL/Python language
for the backend.
%endif

%if %pltcl
%package pltcl
License:	BSD 3-Clause
Summary:	The Tcl procedural language for PostgreSQL
Group:		Productivity/Databases/Clients
Provides:	pltcl.so

%description pltcl
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-pltcl package contains the PL/Tcl language
for the backend.
%endif

%package server
License:	BSD 3-Clause
Summary:	The Programs Needed to Create and Run a PostgreSQL Server
Group:		Productivity/Databases/Servers
PreReq:		%insserv_prereq %fillup_prereq
PreReq:		/usr/sbin/useradd /usr/sbin/groupadd /sbin/chkconfig
PreReq:		/usr/bin/strings /bin/sed
PreReq:		postgresql = %pg_minor_version
Requires:	glibc-locale
Provides:	postgresql-server = %pg_minor_version

%package docs
License:	BSD 3-Clause
Summary:	HTML Documentation for PostgreSQL
Group:		Productivity/Databases/Tools

%description docs
PostgreSQL is an advanced object-relational database management system
that supports an extended subset of the SQL standard, including
transactions, foreign keys, subqueries, triggers, and user-defined
types and functions.

This package contains the HTML documentation for PostgreSQL. The start
page is: file:///usr/share/doc/packages/postgresql/html/index.html .
Manual pages for the PostgreSQL SQL statements can be found in the
postgresql package.

%package contrib
License:	BSD 3-Clause
Summary:	Contributed Extensions and Additions to PostgreSQL
Group:		Productivity/Databases/Tools
Requires:	postgresql-server = %pg_minor_version

%description contrib
PostgreSQL is an advanced object-relational database management system
that supports an extended subset of the SQL standard, including
transactions, foreign keys, subqueries, triggers, and user-defined
types and functions.

The postgresql-contrib package includes extensions and additions that
are distributed along with the PostgreSQL sources, but are not (yet)
officially part of the PostgreSQL core.

Documentation for the modules contained in this package can be found in
/usr/share/doc/packages/postgresql/contrib.

%description server
PostgreSQL is an advanced object-relational database management system
that supports an extended subset of the SQL standard, including
transactions, foreign keys, sub-queries, triggers, and user-defined
types and functions.

This package includes the programs needed to create and run a
PostgreSQL server, which will in turn allow you to create and maintain
PostgreSQL databases.

%package devel
License:	BSD 3-Clause
Summary:	PostgreSQL development header files and libraries
Group:		Productivity/Databases/Tools
Requires:	postgresql-libs = %pg_minor_version

%description devel
PostgreSQL is an advanced object-relational database management system
that supports an extended subset of the SQL standard, including
transactions, foreign keys, subqueries, triggers, and user-defined
types and functions.

This package contains the header files and libraries needed to compile
C applications which will directly interact with a PostgreSQL database
management server and the ECPG Embedded C Postgres preprocessor. You
need to install this package if you want to develop applications in C
which will interact with a PostgreSQL server.

%prep
%setup -q
%patch1

%build
# Use --as-needed to eliminate unnecessary link dependencies.
# Hopefully upstream will do this for itself in some future release.
LDFLAGS="-Wl,--as-needed"; export LDFLAGS

export LIBNAME=%{_lib}
export CFLAGS="%optflags $SP"
# uncomment the following line to enable the stack protector
# CFLAGS="$CFLAGS -fstack-protector"

%configure --disable-rpath \
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
%if %intdatetimes
	--enable-integer-datetimes \
%endif
%if %pgfts
	--enable-thread-safety \
%endif
%if %uuid
	--with-ossp-uuid \
	--with-includes=%_includedir/uuid/
%endif
%if %xml
	--with-libxml \
	--with-libxslt \
%endif
%if %ldap
	--with-ldap \
%endif
	--includedir=%_includedir/pgsql \
	--datadir=%_datadir/postgresql \
	--with-system-tzdata=/usr/share/zoneinfo \
	--with-docdir=%{_docdir}

make %{?jobs:-j%jobs} all
make %{?jobs:-j%jobs} -C contrib all
#
%ifnarch %arm

%check
#
# Run the regression tests.
#
make check || {
  for f in log/* regression.diffs; do
    if test -f $f; then
        echo ==== $f ====================
    fi
  done
  echo ==============================
  exit 1
}
%endif

%install
make DESTDIR=%buildroot install
# Don't ship static libraries.
rm %buildroot/%_libdir/*.a
#
# Install and collect the contrib stuff
#
touch flag; sleep 1 # otherwise we have installed files that are not newer than flag
make DESTDIR=%buildroot -C contrib install
find %buildroot -type f -cnewer flag -printf "/%%P\n" |
     grep -v %_docdir > files.contrib
rm flag
for f in /etc/init.d /var/adm/fillup-templates /usr/sbin \
         /etc/sysconfig/SuSEfirewall2.d/services
do
	install -d %buildroot/$f
done
install -m 755 %{SOURCE9} %buildroot/etc/init.d/postgresql
install -m 644 %{SOURCE8} %buildroot/var/adm/fillup-templates/sysconfig.postgresql
%if 0%suse_version > 1020
install -m 644 %SOURCE16 %buildroot/etc/sysconfig/SuSEfirewall2.d/services/postgresql
%endif
ln -s ../../etc/init.d/postgresql %buildroot/usr/sbin/rcpostgresql
install -d -m 750 %buildroot/var/lib/pgsql
install -d -m 700 %buildroot/var/lib/pgsql/data
install -d -m 700 %buildroot/var/lib/pgsql/backups
sed 's,@LIBDIR@,%_libdir,g' %{SOURCE15} > \
	%buildroot/var/lib/pgsql/.bash_profile
# Backup directory for old version binaries
install -d %buildroot%_libdir/postgresql/backup
cp doc/FAQ doc/KNOWN_BUGS doc/MISSING_FEATURES doc/README* COPYRIGHT \
   README HISTORY doc/bug.template %buildroot%_docdir/postgresql
cp -a %SOURCE2 %buildroot%_docdir/postgresql/README.SuSE.de
cp -a %SOURCE3 %buildroot%_docdir/postgresql/README.SuSE.en

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%if %plperl
%post   -p /sbin/ldconfig       plperl
%postun -p /sbin/ldconfig       plperl
%endif

%if %plpython
%post   -p /sbin/ldconfig       plpython
%postun -p /sbin/ldconfig	plpython
%endif

%if %pltcl
%post   -p /sbin/ldconfig	pltcl
%postun -p /sbin/ldconfig	pltcl
%endif

%post server
%{?fillup_and_insserv:%fillup_and_insserv -s postgresql START_POSTGRES}

%postun server
%{?restart_on_update:%restart_on_update postgresql}
%{?insserv_cleanup:%insserv_cleanup}
exit 0

%preun server
%{?stop_on_removal:%stop_on_removal postgresql}
exit 0

%pre server
groupadd -g 26 -o -r postgres >/dev/null 2>/dev/null || :
useradd -g postgres -o -r -d /var/lib/pgsql -s /bin/bash \
	-c "PostgreSQL Server" -u 26 postgres 2>/dev/null || :
# Need to make a backup of the server binary if this is an upgrade.
# It will be needed to do a dump of the old version's database.
# All output redirected to /dev/null.
umask 022
if [ -f usr/bin/postgres ]
then
  OLD_VERSION=$(strings usr/bin/postgres | 
    /bin/sed -n '/postmaster (PostgreSQL)/s/.* \([0-9]\+\.[0-9]\+\).*/\1/p')
  if [ "$OLD_VERSION" = "" ]
  then
    OLD_VERSION=$(strings usr/bin/postgres |
      /bin/sed -n 's/^PostgreSQL \([0-9]\+\.[0-9]\+\).*/\1/p')
  fi
  MINOR_VERSION=$(echo %version | sed 's/^\([0-9]\+\.[0-9]\+\).*/\1/')
  BACKUP_DIR=usr/%_lib/postgresql/backup/$OLD_VERSION
  if [ "$OLD_VERSION" != "$MINOR_VERSION" -a ! -f "$BACKUP_DIR" ]
  then
    mkdir -p $BACKUP_DIR
    for f in usr/bin/{postmaster,postgres}; do
      test -f $f && cp -a $f $BACKUP_DIR
    done
  fi
fi

%clean
rm -rf %buildroot
rm -f %my_provides

%files
%defattr(-,root,root)
%doc %_mandir/man7/*
%docdir %_docdir/postgresql
%dir %_docdir/postgresql
%_docdir/postgresql/[[:upper:]]*
%_docdir/postgresql/bug.template
%_datadir/locale/*/*/pg_dump.mo
%_datadir/locale/*/*/pgscripts.mo
%_datadir/locale/*/*/psql.mo
# command line tools
%_bindir/createdb
%_bindir/clusterdb
%_bindir/createlang
%_bindir/createuser
%_bindir/dropdb
%_bindir/droplang
%_bindir/dropuser
%_bindir/pg_dump
%_bindir/pg_dumpall
%_bindir/pg_restore
%_bindir/psql
%_bindir/vacuumdb
%_bindir/reindexdb
%doc %_mandir/man1/createdb.1*
%doc %_mandir/man1/clusterdb.1*
%doc %_mandir/man1/createlang.1*
%doc %_mandir/man1/createuser.1*
%doc %_mandir/man1/dropdb.1*
%doc %_mandir/man1/droplang.1*
%doc %_mandir/man1/dropuser.1*
%doc %_mandir/man1/pg_dump.1*
%doc %_mandir/man1/pg_dumpall.1*
%doc %_mandir/man1/pg_restore.1*
%doc %_mandir/man1/psql.1*
%doc %_mandir/man1/vacuumdb.1*
%doc %_mandir/man1/reindexdb.1.*

%files docs
%defattr(-,root,root)
%docdir %_docdir/postgresql
%dir %_docdir/postgresql
%_docdir/postgresql/html

%files contrib -f files.contrib
%defattr(-,root,root)
%docdir %_docdir/postgresql
%dir %_docdir/postgresql
%_docdir/postgresql/contrib
%dir %_libdir/postgresql
%dir %_datadir/postgresql
%dir %_datadir/postgresql/contrib

%files libs
%defattr(-,root,root)
%_libdir/lib*.so.*
%_datadir/locale/*/*/libpq.mo

%files server
%defattr(-,root,root)
%config /etc/init.d/postgresql
%config /var/adm/fillup-templates/sysconfig.postgresql
%if 0%suse_version > 1020
%config /etc/sysconfig/SuSEfirewall2.d/services/postgresql
%endif
%_sbindir/rcpostgresql
%dir %_libdir/postgresql
%_libdir/postgresql/backup
%_libdir/postgresql/dict_snowball.so
%_libdir/postgresql/plpgsql.so
%_libdir/postgresql/tsearch2.so
%_datadir/postgresql/tsearch_data
%_bindir/initdb
%_bindir/ipcclean
%_bindir/pg_ctl
%_bindir/pg_controldata
%_bindir/pg_resetxlog
%_bindir/postgres
%_bindir/postmaster
%doc %_mandir/man1/initdb.1*
%doc %_mandir/man1/ipcclean.1*
%doc %_mandir/man1/pg_ctl.1*
%doc %_mandir/man1/pg_controldata.1*
%doc %_mandir/man1/pg_resetxlog.1*
%doc %_mandir/man1/postgres.1*
%doc %_mandir/man1/postmaster.1*
%dir %_datadir/postgresql
%_datadir/postgresql/timezone*
%_datadir/postgresql/*.*
%_datadir/locale/*/*/initdb.mo
%_datadir/locale/*/*/postgres.mo
%_datadir/locale/*/*/pg_controldata.mo
%_datadir/locale/*/*/pg_ctl.mo
%_datadir/locale/*/*/pg_resetxlog.mo
%_libdir/postgresql/*_and_*.so
%attr(750,postgres,postgres) %dir /var/lib/pgsql
%attr(700,postgres,postgres) %dir /var/lib/pgsql/data
%attr(700,postgres,postgres) %dir /var/lib/pgsql/backups
%attr(640,postgres,postgres) %config(noreplace) /var/lib/pgsql/.bash_profile

%files devel
%defattr(-,root,root)
%_includedir/pgsql
%_bindir/ecpg
%_bindir/pg_config
%_libdir/lib*.so
%_libdir/libpgport.a
%_libdir/postgresql/pgxs
%_datadir/locale/*/*/pg_config.mo
%doc %_mandir/man1/ecpg.1*
%doc %_mandir/man1/pg_config.1*

%if %plperl
%files plperl
%defattr(-,root,root)
%_libdir/postgresql/plperl.so
%endif

%if %pltcl
%files pltcl
%defattr(-,root,root)
%_libdir/postgresql/pltcl.so
%_bindir/pltcl_delmod
%_bindir/pltcl_listmod
%_bindir/pltcl_loadmod
%_datadir/postgresql/unknown.pltcl
%endif

%if %plpython
%files plpython
%defattr(-,root,root)
%_libdir/postgresql/plpython.so
%endif

%changelog
* Thu Dec 11 2008 Devrim GUNDUZ >devrim@commandprompt.com> 8.3.5-1
- Update to 8.3.5
- Trim spec file changelog 
- Add PGDG spec file header text.
- Add all macros that are already used in Fedora'ish distros. Enable
  intdatetimes macro by default, since SuSE always shipped with that.
- Split -pl subpackage into three new packages to minimize dependencies.
- 

* Fri Sep 19 2008 Devrim GUNDUZ >devrim@commandprompt.com> 8.3.4-1
- Update to 8.3.4
- Fix packaging errors
- Cosmetic fixes to spec file.e

