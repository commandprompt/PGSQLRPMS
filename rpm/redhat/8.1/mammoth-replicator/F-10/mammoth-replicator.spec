# CMD MR specific 
%{!?cmdmrssl:%define cmdmrssl 1}
%{!?cmdmrdebug:%define cmdmrdebug 0}
%{?cmdmrdebug:%define __os_install_post /usr/lib/rpm/brp-compress}

# General part

%{!?aconfver:%define aconfver autoconf}

%{!?tcldevel:%define tcldevel 0}
%{!?kerbdir:%define kerbdir "/usr"}
%{!?test:%define test 1}
%{!?pltcl:%define pltcl 0}
%{!?plperl:%define plperl 1}
%{!?pls:%define pls 1}
%{!?ssl:%define ssl 1}
%{!?kerberos:%define kerberos 1}
%{!?nls:%define nls 1}
%{!?pam:%define pam 1}
%{!?xml:%define xml 1}
%{!?pgfts:%define pgfts 0}
%{!?runselftest:%define runselftest 1}

Summary:	Asynchronous Replication for PostgreSQL
Name:		mammoth-replicator
Version:	8.1.13
Release: 	1.8_2CMDMR%{?dist}
License:	BSD
Group:		Applications/Databases
Buildroot: 	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0: 	http://www.commandprompt.com/files/replicator//%{name}-%{version}.tar.bz2
Source3:	%{name}.init
Source4:	Makefile.regress
Source5:	mcp_server.init
Source6: 	README.rpm-dist
Source9:	pg_config.h
Source12: 	http://www.postgresql.org/files/documentation/pdf/8.1/postgresql-8.1-A4.pdf
Source14: 	%{name}.pam
Source15: 	%{name}-bashprofile
Source16: 	filter-requires-perl-Pg.sh
Source18: 	ftp://ftp.pygresql.org/pub/distrib/PyGreSQL-3.8.1.tgz

Patch1: 	rpm-pgsql.patch
Patch2:		%{name}-src-tutorial.patch
Patch3:		%{name}-logging.patch
Patch4:		%{name}-test.patch
Patch6:		%{name}-perl-rpath.patch
Patch8:		%{name}-init-mammoth-database.patch

BuildRequires:	perl glibc-devel bison flex autoconf
Requires:	/sbin/ldconfig initscripts

%if %pltcl
BuildRequires: 	tcl
%endif

%if %tcldevel
BuildRequires: 	tcl-devel
%endif

BuildRequires: 	readline-devel,	zlib-devel >= 1.0.4

%if %ssl
BuildRequires: 	openssl-devel
%endif

%if %kerberos
BuildRequires:	krb5-devel, e2fsprogs-devel
%endif

%if %nls
BuildRequires:	gettext >= 0.10.35
%endif

%if %cmdmrssl
BuildRequires:	openssl-devel
%endif

%if %pam
BuildRequires:	pam-devel
%endif

%if %xml
BuildRequires:	libxml2-devel libxslt-devel
%endif

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
Summary:	The shared libraries required for any PostgreSQL clients.
Group:		Applications/Databases
Provides:	libpq.so
Obsoletes:	postgresql-libs

%description libs
The postgresql-libs package provides the essential shared libraries for any 
PostgreSQL client program or interface. You will need to install this package
to use any other PostgreSQL package or any clients that need to connect to a
PostgreSQL server.

%package replicator
Summary:	The Mammoth Replicator solution for PostgreSQL ORDBMS, by Command Prompt Inc.
Group:		Applications/Databases
Requires:	%{name}-server = %{version}

%description replicator
The replicator package provides the essential software by required for
Mammoth Replicator.

%package server
Summary:	The programs needed to create and run a PostgreSQL server.
Group:		Applications/Databases
Requires:	/usr/sbin/useradd /sbin/chkconfig
Requires:	%{name} = %{version} libpq.so
Obsoletes:	postgresql-server

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
Obsoletes:	postgresql-docs

%description docs
The postgresql-docs package includes the SGML source for the documentation
as well as the documentation in PDF format and some extra documentation.
Install this package if you want to help with the PostgreSQL documentation
project, or if you want to generate printed documentation.

%package contrib
Summary:	Contributed source and binaries distributed with PostgreSQL
Group:		Applications/Databases
Requires:	%{name} = %{version}
Obsoletes:	postgresql-contrib

%description contrib
The postgresql-contrib package contains contributed packages that are
included in the PostgreSQL distribution.

%package devel
Summary: PostgreSQL development header files and libraries
Group: Development/Libraries
Requires:	%{name}-libs = %{version}
Obsoletes:	postgresql-devel

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
Summary:	The PL procedural languages for PostgreSQL.
Group:		Applications/Databases
Requires:	%{name} = %{version}
Requires:	%{name}-server = %{version}
Obsoletes:	postgresql-pl, postgresql-plperl, postgresql-pltcl, postgresql-plpython

%description pl
PostgreSQL is an advanced Object-Relational database management
system.  The postgresql-pl package contains the the PL/Perl, and PL/Python
procedural languages for the backend.  PL/Pgsql is part of the core server package.
%endif

%if %test
%package test
Summary:	The test suite distributed with PostgreSQL.
Group:		Applications/Databases
Requires:	%{name} = %{version}
Requires:	%{name}-server = %{version}
Obsoletes:	postgresql-test

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

#call autoconf 2.53 or greater
%aconfver

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
	--enable-replication \
%if %cmdmrssl
	--with-mcp-openssl \
%endif
%if %cmdmrdebug
	--enable-debug \
%endif
%if %plperl
	--with-perl \
%endif
%if %pltcl
	--with-tcl \
	--with-tclconfig=%[_libdir}/ \
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
	--with-libraries=%{kerbdir}/%{_lib} \
%endif
%if %nls
	--enable-nls \
%endif
%if %pgfts
	--enable-thread-safety \
%endif
	--sysconfdir=/etc/sysconfig/pgsql \
	--datadir=/%{_datadir}/pgsql \
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

# multilib header hack; note pg_config.h is installed in two places!
# we only apply this to known Red Hat multilib arches, per bug #177564
#case `uname -i` in
#	i386 | x86_64 | ppc | ppc64 | s390 | s390x)
#		mv %{buildroot}%{_includedir}/pg_config.h %{buildroot}%{_includedir}/pg_config_`uname -i`.h
#		install -m 644 %{SOURCE9} %{buildroot}%{_includedir}
#		mv %{buildroot}%{_includedir}/pgsql/server/pg_config.h %{buildroot}%{_includedir}/pgsql/server/pg_config_`uname -i`.h
#		install -m 644 %{SOURCE9} %{buildroot}%{_includedir}/pgsql/server/
#    ;;
#  *)
#    ;;
#esac

install -d -m 755 %{buildroot}%{_libdir}/pgsql/tutorial
cp src/tutorial/* %{buildroot}%{_libdir}/pgsql/tutorial

install -m 755 src/backend/mammoth_r/globals/globals-install.sql %{buildroot}%{_datadir}/pgsql

install -d %{buildroot}/etc/rc.d/init.d
sed 's/^PGVERSION=.*$/PGVERSION=%{version}/' <%{SOURCE3} > %{name}.init
install -m 755 mammoth-replicator.init %{buildroot}/etc/rc.d/init.d/%{name}
install -m 755 %{SOURCE5} %{buildroot}/etc/rc.d/init.d/mcp_server

%if %pam
install -d %{buildroot}/etc/pam.d
install -m 644 %{SOURCE14} %{buildroot}/etc/pam.d/mammoth
%endif

# PGDATA needs removal of group and world permissions due to pg_pwd hole.
install -d -m 700 %{buildroot}/var/lib/pgsql/data

# backups of data go here...
install -d -m 700 %{buildroot}/var/lib/pgsql/backups

# postgres' .bash_profile
install -m 644 %{SOURCE15} %{buildroot}/var/lib/pgsql/.bash_profile

# Create the multiple postmaster startup directory
install -d -m 700 %{buildroot}/etc/sysconfig/postgresql

# Install MCP conf files 
install -m 644 src/bin/mammoth/mcp_server.conf %{buildroot}%{_datadir}/pgsql
install -m 644 src/bin/mammoth/mcp_server.conf.sample %{buildroot}%{_datadir}/pgsql
/bin/rm -f %{buildroot}/%{_bindir}/mcp_server.conf*

%if %test
	# tests. There are many files included here that are unnecessary, but include
	# them anyway for completeness. We replace the original
	# Makefiles, however.
	mkdir -p %{buildroot}%{_libdir}/test
	cp -a src/test/regress %{buildroot}%{_libdir}/test
	install -m 0755 contrib/spi/refint.so %{buildroot}%{_libdir}/test/regress
	install -m 0755 contrib/spi/autoinc.so %{buildroot}%{_libdir}/test/regress
	pushd  %{buildroot}%{_libdir}/test/regress/
	strip *.so
	rm -f GNUmakefile Makefile *.o
	popd
	cp %{SOURCE4} %{buildroot}%{_libdir}/test/regress/Makefile
	chmod 0644 %{buildroot}%{_libdir}/test/regress/Makefile
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
groupadd -g 85 -o -r postgres >/dev/null 2>&1 || :
useradd -M -n -g postgres -o -r -d /var/lib/pgsql -s /bin/bash \
	-c "Mammoth Replicator Server" -u 85 postgres >/dev/null 2>&1 || :
touch /var/log/mammoth
chown postgres:postgres /var/log/mammoth
chmod 0700 /var/log/mammoth

%post server
chkconfig --add mammoth
/sbin/ldconfig

%preun server
if [ $1 = 0 ] ; then
	/sbin/service mammoth condstop >/dev/null 2>&1
	chkconfig --del mammoth
fi

%postun server
/sbin/ldconfig 
if [ $1 -ge 1 ]; then
  /sbin/service mammoth condrestart >/dev/null 2>&1
fi
if [ $1 = 0 ] ; then
	userdel postgres >/dev/null 2>&1 || :
	groupdel postgres >/dev/null 2>&1 || : 
fi

%if %pls
%post -p /sbin/ldconfig	pl
%postun -p /sbin/ldconfig pl
%endif

%if %test
%post test
chown -R postgres:postgres %{_libdir}/test >/dev/null 2>&1 || :
%endif

%clean
rm -rf %{buildroot}

# FILES section.

%files -f main.lst
%defattr(-,root,root)
%doc doc/FAQ doc/KNOWN_BUGS doc/MISSING_FEATURES doc/README* 
%doc COPYRIGHT README doc/bug.template
%doc README.rpm-dist
%doc doc/
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
%{_bindir}/reindexdb
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
%{_mandir}/man1/reindexdb.*
%{_mandir}/man1/vacuumdb.*
%{_mandir}/man7/*

%files docs
%defattr(-,root,root)
%doc doc/src/*
#%doc *-A4.pdf
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
%{_libdir}/pgsql/earthdistance.so
%{_libdir}/pgsql/fti.so
%{_libdir}/pgsql/fuzzystrmatch.so
%{_libdir}/pgsql/insert_username.so
%{_libdir}/pgsql/int_aggregate.so
%{_libdir}/pgsql/isbn_issn.so
%{_libdir}/pgsql/lo.so
%{_libdir}/pgsql/ltree.so
%{_libdir}/pgsql/moddatetime.so
%{_libdir}/pgsql/pending.so
%{_libdir}/pgsql/pg_buffercache.so
%{_libdir}/pgsql/pgcrypto.so
%{_libdir}/pgsql/pgstattuple.so
%{_libdir}/pgsql/pg_trgm.so
%{_libdir}/pgsql/refint.so
%{_libdir}/pgsql/seg.so
%{_libdir}/pgsql/tablefunc.so
%{_libdir}/pgsql/timetravel.so
%{_libdir}/pgsql/tsearch2.so
%{_libdir}/pgsql/user_locks.so
%if %xml
%{_libdir}/pgsql/pgxml.so
%endif
%{_datadir}/pgsql/contrib
%{_bindir}/DBMirror.pl
%{_bindir}/clean_pending.pl
%{_bindir}/dbf2pg
%{_bindir}/fti.pl
%{_bindir}/oid2name
%{_bindir}/pgbench
%{_bindir}/vacuumlo
%doc contrib/*/README.* contrib/spi/*.example

%files libs -f libpq.lang
%defattr(-,root,root)
%{_libdir}/libpq.so.*
%{_libdir}/libecpg.so.*
%{_libdir}/libpgtypes.so.*
%{_libdir}/libecpg_compat.so.*

%files replicator
%defattr(-,root,root)
%{_bindir}/mcp_ctl
%{_bindir}/init-mammoth-database
%{_bindir}/mcp_server
%{_bindir}/mcp_stat
%{_datadir}/pgsql/mammoth_pk_indexes.sql
%{_datadir}/pgsql/replicator-functions.sql
%{_datadir}/pgsql/globals-install.sql
%attr(644,postgres,postgres) %config(noreplace) %{_datadir}/pgsql/mcp_server.conf*

%files server -f server.lst
%defattr(-,root,root)
%if %pam
%config(noreplace) /etc/pam.d/mammoth
%endif
%attr (755,root,root) %dir /etc/sysconfig/postgresql
%{_initrddir}/mammoth-replicator
%{_initrddir}/mcp_server
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
%{_datadir}/pgsql/mammoth.bki
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
%{_includedir}/*
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
%{_libdir}/pltcl.so
%{_bindir}/pltcl_delmod
%{_bindir}/pltcl_listmod
%{_bindir}/pltcl_loadmod
%{_datadir}/pgsql/unknown.pltcl
%endif
%endif

%if %test
%files test
%defattr(-,postgres,postgres)
%attr(-,postgres,postgres) %{_libdir}/test/*
%attr(-,postgres,postgres) %dir %{_libdir}/test
%endif

%changelog
* Mon Aug 25 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.1.13-1.8_2
- Use better Obsoletes

* Fri Aug 22 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.1.13-1.8_1
- First open source release.
- Spec file cleanup
