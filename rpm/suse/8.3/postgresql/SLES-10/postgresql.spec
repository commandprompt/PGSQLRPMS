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

%define pg_minor_version %(echo %version | cut -f1-2 -d.)

Name:		postgresql
Summary:	Basic Clients and Utilities for PostgreSQL
Url:		http://www.postgresql.org/
Version:	8.3.5
Release:	1
License:	BSD 3-Clause
Group:		Productivity/Databases/Tools
Source0:	postgresql-%version.tar.bz2
Source2:	postgresql-README.SuSE.de
Source3:	postgresql-README.SuSE.en
Source8:	postgresql-sysconfig
Source9:	postgresql-init
Source15:	postgresql-bashprofile
Source16:	postgresql-firewall
Source17:	postgresql-rpmlintrc
Source99:	postgresql-pl.spec
Patch1:		postgresql-8.3-conf.patch
PreReq:		postgresql-libs = %pg_minor_version
BuildRequires:	bison flex gettext-devel krb5-devel libxslt-devel
BuildRequires:	openldap2-devel openssl-devel pam-devel readline-devel zlib-devel
BuildRequires:	ncurses-devel
Provides:	postgresql = %pg_minor_version
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

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


Authors:
--------
    Marc G. Fournier <scrappy@hub.org>
    Tom Lane <tgl@sss.pgh.pa.us>
    Vadim B. Mikheev <vadim4o@yahoo.com>
    Bruce Momjian <pgman@candle.pha.pa.us>
    Jan Wieck <JanWieck@Yahoo.com>

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


%package pl
License:	BSD 3-Clause
Summary:	Procedural Languages for PostgreSQL
Group:		Productivity/Databases/Clients
Provides:	plperl.so plpython.so

%description pl
This package includes procedural language support for PostgreSQL.

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
export CFLAGS="%optflags $SP"
# uncomment the following line to enable the stack protector
# CFLAGS="$CFLAGS -fstack-protector"
./configure \
	--prefix=%_prefix \
	--libdir=%_libdir \
	--bindir=%_bindir \
	--includedir=%_includedir/pgsql \
	--datadir=%_datadir/postgresql \
	--mandir=%_mandir \
	--with-docdir=%_docdir \
	--disable-rpath \
	--enable-nls \
	--enable-thread-safety \
	--enable-integer-datetimes \
	--with-tcl \
	--with-python \
	--with-perl \
	--with-openssl \
	--with-pam \
	--with-ldap \
	--with-libxml \
	--with-libxslt \
	--with-system-tzdata=/usr/share/zoneinfo
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
%_libdir/postgresql/plpgsql.so
%_libdir/postgresql/dict_snowball.so
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
%_libdir/postgresql/pgxs
%_datadir/locale/*/*/pg_config.mo
%doc %_mandir/man1/ecpg.1*
%doc %_mandir/man1/pg_config.1*

%files pl
%defattr(-,root,root)
%_libdir/postgresql/plperl.so
%_libdir/postgresql/plpython.so

%changelog
* Fri Sep 19 2008 Devrim GUNDUZ >devrim@commandprompt.com> 8.3.4-1
- Update to 8.3.4
- Fix packaging errors
- Cosmetic fixes to spec file.

* Mon May 19 2008 schwab@suse.de
- Fix broken configure check.
* Fri May  9 2008 aj@suse.de
- Add baselibs.conf.
* Fri Apr 18 2008 max@suse.de
- Removed static libs from postgresql-devel.
- Removed more old Obsoletes: tags.
- Fixed path to pid file in init script.
- Moved "make check" to %%check section
- Silence some bogus rpmlint warnings
* Thu Apr 10 2008 max@suse.de
- Adopt the 8.3.1 package from Peter Eisentraut's OBS project.
- New features in PostgreSQL 8.3 include:
  * Full text search is integrated into the core database system
  * Support for the SQL/XML standard, including new operators and
    an XML data type
  * Enumerated data types (ENUM)
  * Arrays of composite types
  * Universally Unique Identifier (UUID) data type
  * Add control over whether NULLs sort first or last
  * Updatable cursors
  * Server configuration parameters can now be set on a
    per-function basis
  * User-defined types can now have type modifiers
  * Automatically re-plan cached queries when table definitions
    change or statistics are updated
  * Numerous improvements in logging and statistics collection
  * Support multiple concurrent autovacuum processes, and other
    autovacuum improvements
- Remove old provides/obsoletes tags for way-back package renames.
* Thu Apr 10 2008 ro@suse.de
- added baselibs.conf file to build xxbit packages
  for multilib support
* Thu Jan 10 2008 max@suse.de
- Update to 8.2.6 to fix five security issues:
  - Index Functions Privilege Escalation: CVE-2007-6600
  - Regular Expression Denial-of-Service: CVE-2007-4772,
    CVE-2007-6067, CVE-2007-4769, #329282
  - DBLink Privilege Escalation: CVE-2007-6601, #328403
* Wed Jun  6 2007 max@suse.de
- New version: 8.2.4
- The list of changes between the 8.1 and 8.2 series is too long
  to reproduce here. It can be found under
  /usr/share/doc/packages/postgresql/HISTORY when the postgresql
  package is installed or online at http://www.postgresql.org.
- Splited the postgresql-pl package into individual packages for
  PL/Perl, PL/Python and PL/Tcl.
- Added a config file for SuSEfirewall2 (#247370).
* Thu Mar 29 2007 rguenther@suse.de
- Add bison, flex and zlib-devel BuildRequires.
* Tue Oct 17 2006 max@suse.de
- New patchlevel release: 8.1.5
- Disallow aggregate functions in "UPDATE" commands, except within
  sub-SELECTs. The behavior of such an aggregate was unpredictable,
  and in 8.1.X could cause a crash, so it has been disabled.
- Fix core dump when an untyped literal is taken as ANYARRAY.
- Fix core dump in duration logging for extended query protocol when
  a "COMMIT" or "ROLLBACK" is executed.
- Fix mishandling of AFTER triggers when query contains a SQL function
  returning multiple rows.
- Fix "ALTER TABLE ... TYPE" to recheck NOT NULL for USING clause.
- Fix string_to_array() to handle overlapping matches for the
  separator string.
- Fix to_timestamp() for AM/PM formats.
- Fix autovacuum's calculation that decides whether "ANALYZE" is
  needed.
- Fix corner cases in pattern matching for psql's \d commands.
- Fix index-corrupting bugs in /contrib/ltree.
- Numerous robustness fixes in ecpg.
- Fix backslash escaping in /contrib/dbmirror.
- Minor fixes in /contrib/dblink and /contrib/tsearch2.
- Efficiency improvements in hash tables and bitmap index scans.
* Wed May 24 2006 max@suse.de
- Update to 8.1.4 to fix SQL injection vulnerabilities
  (bug #177931, CVE-2006-2313, CVE-2006-2314).
- Added a new postgresql-SECURITY-NOTICE file with an FAQ that
  explains the issues.
* Mon Feb 13 2006 max@suse.de
- New version: 8.1.3 (#150376).
- Relaxed dependencies between subpackages to simplify future
  updates.
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Fri Jan 13 2006 max@suse.de
- Moved from logrotate to PostgreSQL's own log rotation facility.
- Log files are now located under /var/lib/pgsql/data/pg_log .
- Improved error reporting on test suite failures.
* Thu Dec 22 2005 max@suse.de
- New version: 8.1.1
* Fri Jun 17 2005 max@suse.de
- Removed bogus %%patch3
* Thu Jun  2 2005 max@suse.de
- Added postgresql-CAN-2005-1409-1410-fix.sh for fixing existing
  installations, and referred to it in the SECURITY-NOTICE.
* Tue May 17 2005 max@suse.de
- Added postgresql-SECURITY-NOTICE to describe the manual actions
  that are needed to apply the bugfixes from 8.0.3 to existing
  installations.
* Tue May 10 2005 max@suse.de
- New patch release: 8.0.3
- Fixes bug #82869, CAN-2005-1410, and CAN-2005-1409
- Obsoletes postgresql-CAN-2005-0247.patch
* Mon Apr 11 2005 max@suse.de
- New patch release: 8.0.2
* Mon Apr  4 2005 uli@suse.de
- hardwire thread safety to yes (test may hang QEMU)
* Fri Apr  1 2005 uli@suse.de
- ignore regressions on ARM
* Wed Mar 16 2005 max@suse.de
- Prevent the wrapper libs from ending up in the provides list.
* Mon Mar 14 2005 max@suse.de
- Added postgresql-CAN-2005-0247.patch to fix bug #65692.
* Fri Mar 11 2005 max@suse.de
- Added some wrapper libs so that old postmaster binaries, back
  to at least 8.1/SLES8 can still be started.
- Extended the init script to use the wrapper libs when needed.
- Setting a senseful umask when creating the postmaster backups
  in %%pre.
* Mon Feb  7 2005 max@suse.de
- New patch release: 8.0.1
- Fixes a vulnerability in the LOAD command.
* Wed Jan 19 2005 max@suse.de
- Update to the final 8.0.0 release.
* Wed Dec 22 2004 max@suse.de
- New version: 8.0.0rc2
* Fri Dec 10 2004 max@suse.de
- New version: 8.0.0rc1
- Recoded README.SuSE.de to UTF-8.
* Fri Dec  3 2004 max@suse.de
- New version: 8.0.0beta5
* Thu Nov 18 2004 ro@suse.de
- use kerberos-devel-packages
* Mon Sep  6 2004 max@suse.de
- Created a separate spec file for the postgresql-pl subpackage.
* Fri Aug 20 2004 max@suse.de
- New version: 7.4.5.
* Thu Jul 15 2004 max@suse.de
- New version: 7.4.3.
* Mon May 24 2004 max@suse.de
- Changed dependency of -devel from the main package to -libs
  (Bug #40922).
* Mon Apr  5 2004 max@suse.de
- Added postgresql-regression.patch to prevent test failures
  during summertime/wintertime changes.
* Thu Mar 11 2004 max@suse.de
- New patch release: 7.4.2
* Fri Jan 16 2004 kukuk@suse.de
- Add pam-devel to neededforbuild
* Mon Jan 12 2004 max@suse.de
- New version: 7.4.1
- Write timestamps to /var/log/postgresql by default.
* Thu Dec 18 2003 max@suse.de
- Package the backend headers as well (make install-all-headers),
  because they are needed for server-side modules written in C.
* Tue Nov 18 2003 max@suse.de
- Install pg_config_manual.h and port.h, because they are needed
  by c.h (postgresql-include.patch).
* Mon Nov 17 2003 max@suse.de
- New version: 7.4. For details see
  http://www.postgresql.org/docs/7.4/static/release.html, or
  /usr/share/doc/packages/postgresql/html/release.html
- Overhauled and simplified the spec file.
- Building with Kerberos-Support.
- Building thread-safe client libraries.
- Architecture-dependent tweaks for the testsuite are not needed
  anymore.
- Better detection for embedded Python build options.
* Mon Oct 20 2003 schwab@suse.de
- Fix last change.
* Sat Oct 18 2003 adrian@suse.de
- ignore minor mis-calculation on mips
- build as user
* Tue Sep 23 2003 max@suse.de
- Fixed version detection in the pre script of the server package.
  (#31570)
- Ignore errors from stop_on_removal (#31607).
* Mon Sep 15 2003 max@suse.de
- Activated the patch, that fixes dbf2pg (#27427). The patch was
  added to the package before, but accidentally didn't get applied.
- Improved handling of old versions of the backend (#27114).
- Stopping the server before uninstallation and restarting it
  after update (#29038).
* Fri Aug 29 2003 mcihar@suse.cz
- python bindings require same python version as it was built with
* Thu Aug 14 2003 max@suse.de
- Added ServiceRestart to sysconfig template.
* Thu Aug 14 2003 ro@suse.de
- fixed chown usage in init-script
* Mon Aug  4 2003 max@suse.de
- New version: 7.3.4.
- Adopted postgresql-multilib.patch from the official PostgreSQL
  RPMs. This obsoletes postgresql-lib64.patch.
- Use test-and-set locks for x86_64 instead of slow semaphores.
  (postgresql-x86_64.patch, Bug #27308)
- make use of %%jobs for parallel builds.
- Fix ownership of /etc/logrotate.d/postgresql (Bug #28431).
- Changed the default locale for the server to "C" to avoid a hard
  dependency to glibc-locale (bug #28338).
- Enabled charset conversion for dbf2pg (Bug #27427).
* Wed Jul 16 2003 meissner@suse.de
- fix hanging builds by another rework of the ppc64
  locking. Apparently we need to do exact stcwx. ; bne ; isync
  sequences to stay correct.
* Tue Jun 24 2003 meissner@suse.de
- Fixed the ppc/ppc64 locking, isync was at the wrong
  position. Replaced full sync by lwsync. slock_ts can
  be 32bit on ppc64 too, we just use lwarx/stwcx which
  handle 32bit components.
* Tue Jun  3 2003 max@suse.de
- New version: 7.3.3.
- Remove unpackaged files.
- pg_hba.conf: only allow local connections from the same user
  by default.
* Fri Mar 14 2003 max@suse.de
- Fixed generation of sql files in contrib, and really install the
  contrib stuff instead of just copying over the source tree
  (Bug #25323, postgresql-contrib.patch).
- Fixed the file-list of the server package.
* Wed Mar 12 2003 max@suse.de
- Fixed a typo in the init script (Bug #25115).
* Thu Mar  6 2003 max@suse.de
- Add support for LSB compatible exit codes for start and stop
  to pg_ctl (postgresql-lsb.patch).
- Use pg_ctl instead of startproc/killproc in init script, because
  it waits until the server is completely fired up or shut down.
  (Bug #24395)
- Removed the libpq.so.2.0 link from the package, because it got
  removed by ldconfig after installation anyways (Bug #24557).
* Tue Feb 25 2003 max@suse.de
- Mark manpages as documentation.
- Create the backup directory during install.
* Mon Feb 24 2003 max@suse.de
- Make a backup of the server binaries during update, and use the
  old server as long as the data files are still in the old format.
* Thu Feb  6 2003 max@suse.de
- New patch release 7.3.2 which fixes several serious bugs.
  See HISTORY for details.
* Tue Jan 28 2003 max@suse.de
- Added metadata for the sysconfig editor.
* Mon Jan 20 2003 max@suse.de
- New version: 7.3.1
- Removed old update scripts, because they don't work anymore.
* Thu Jan 16 2003 bg@suse.de
- Changed the expected test results for hppa to the correct files
* Fri Nov 29 2002 max@suse.de
- New version 7.3.
- Compiling with PAM support.
- Client libraries (perl, tcl, odbc, pgeasy, pq++) have been
  taken out of the PostgreSQL core distribution and will be
  built as separate packages in the future.
- The plperl subpackage has been renamed to pl, and now contains
  PL/Perl, PL/Python, and PL/Tcl.
* Fri Sep 13 2002 max@suse.de
- Added circle_poly-overrun.patch to fix a couple of
  buffer overruns.
* Thu Sep 12 2002 max@suse.de
- Corrected symlink /usr/lib/libpq.so.2.0 [#19490].
- Fixed ownership of /var/lib/pgsql [#19523].
* Fri Sep  6 2002 max@suse.de
- Recovered time stamps of source files and patches.
* Mon Sep  2 2002 max@suse.de
- Updated to patch release 7.2.2 which fixes some security holes.
- Essential diff between 7.2.1 and 7.2.2 is included.
* Tue Aug 20 2002 mmj@suse.de
- Correct PreReq
* Mon Aug 19 2002 kukuk@suse.de
- Fix requires egenix-mx-base -> python-egenix-mx-base
* Fri Aug 16 2002 ro@suse.de
- don't chmod 644 to directories
* Wed Aug 14 2002 ro@suse.de
- added "missingok" to logrotate config
* Fri Aug  9 2002 max@suse.de
- Removed sysconfig from neededforbuild.
- Using x-devel-packages instead of xf86.
* Thu Aug  8 2002 max@suse.de
- Removed support for older SuSE versions.
- Moved log file cration from %%post to rcpostgresql.
- Changed group for /etc/logrotate.d/postgresql.
* Mon Aug  5 2002 max@suse.de
- Enabled the plperl subpackage.
* Tue Jul 30 2002 max@suse.de
- Fixed regression tests for ppc64.
* Fri Jul 12 2002 max@suse.de
- Re-enabled the regression tests.
- Running test suite as nobody.
- Adjusted ppc and lib64 patch to the scheme of the other
  platform patches.
- Better test-and-set assembler code for s390 and s390x.
- Creating postgres user and group during RPM installation.
* Tue Jun 18 2002 meissner@suse.de
- use the powerpc assembler tas() for ppc64 too with adjusted assembler
  names.
* Fri May 24 2002 max@suse.de
- New minor release: 7.2.1
- Temporaryly disabled the regression tests due to changes to
  mktime() that caused some tests to fail.
* Fri May 24 2002 ke@suse.de
- postgresql-python requires egenix-mx-base (DateTime) [# 14745].
* Wed May 22 2002 meissner@suse.de
- %%_lib fixes for lib64 architectures. Now fails at the same point as i386.
* Wed Mar 20 2002 max@suse.de
- Changed postgresql package to PreReq postgresql-libs instead of
  postgresql-lib which is obsolete.
* Fri Mar  8 2002 poeml@suse.de
- add missing / before %%_lib, fixing the preinstall script of -libs
  subpackage
* Wed Mar  6 2002 max@suse.de
- Fixed test-and-set assembler code for s390x.
- Made finding of perl and python site-paths more portable.
- Fixed detection of SuSE dist for older releases.
- Some more %%_libdir corrections.
- Using -fPIC for building shared libs on all architectures.
- Leaving out tk and python subpackages if tk and python
  are not OK.
* Mon Mar  4 2002 max@suse.de
- Fixed creation of pkgIndex.tcl
- Removed some python stuff from the spec file that is now part of
  PostgreSQL's build system.
- Removed unneeded executable permissions from a couple of files.
* Wed Feb 13 2002 max@suse.de
- added support for logrotate
- changed sysconfig stuff and init script to run on both
  schemes (<=7.3 and >=8.0).
* Tue Feb  5 2002 max@suse.de
- Updated to 7.2 final.
- See the file /usr/share/doc/packages/postgresql/HISTORY
  for changes and incompatibilities since version 7.1.x.
- Adapted the init script to match the new versions of killproc
  and PostgreSQL.
* Mon Jan 28 2002 max@suse.de
- Updated to 7.2rc2
- Removed temporary header fix.
- Added a patch for autoconf-2.52 (disabled by derfault).
- Added english version of README.SuSE
* Tue Jan 22 2002 max@suse.de
- removed os.h. It's not needed anymore.
- fixed locations of internal header files (temporary).
- postgresql-python now obsoletes pygresql.
- updated the files lists.
* Mon Jan 21 2002 max@suse.de
- New version 7.2b5
* Tue Dec 18 2001 max@suse.de
- Changed spec file to make use of %%{_libdir} where appropriate.
* Mon Dec 17 2001 max@suse.de
- Removed the START_POSTGRES variable from the fillup template
  and changed init script, and spec file to the new scheme.
- Moved the remaining variables from /etc/rc.config to
  /etc/sysconfig/postgresql.
* Wed Sep 12 2001 max@suse.de
- New version (patch release): 7.1.3
  The ChangeLog says:
  - Remove unused WAL segements of large transactions (Tom)
  - Multiaction rule fix (Tom)
  - Pl/pgSQL memory allocation fix (Jan)
  - VACUUM buffer fix (Tom)
  - Regression test fixes (Tom)
  - pg_dump fixes for GRANT/REVOKE/comments on views,
    user-defined types (Tom)
  - Fix subselects with DISTINCT ON or LIMIT (Tom)
  - BEOS fix
  - Disable COPY TO/FROM a view (Tom)
  - Cygwin build (Jason Tishler)
- Fixed bug in init script.
  It needed a file that comes only with postgresql-devel
- Better Patch for PgTcl. It now sets the client encoding to
  UNICODE (PostgreSQL's name for UTF-8) for Tcl versions >= 8.1
  instead of using Tcl's conversion functions to get the correct
  string representation.
- Added README.SuSE (only german, so far)
- Some minor typo fixes in the spec file.
* Mon Aug 27 2001 utuerk@suse.de
- removed postgresql.conf (now provided by susehelp)
* Mon Jul 23 2001 max@suse.de
- Fixed %%pre and %%post scripts for YaST.
* Thu Jul 19 2001 max@suse.de
- fixed regression tests for SPARC32.
- fixed init script to warn about incompatible data files.
- added patch for Pgtcl to use UTF8 for internal string
  representation if compiled with Tcl >= 8.1 .
- added pkgIndex.tcl to allow dynamic loading of Pgtcl using
  Tcl's package mechanism.
* Wed Jul 11 2001 max@suse.de
- fixed regression test to succeed on PPC with glibc-2.2.3 .
* Tue Jul 10 2001 max@suse.de
- new version: 7.1.2
- packages again based on the official PostgreSQL RPMs.
- architecture patches are no longer needed.
- running the regression tests as part of the build process to
  ensure that only correctly built binaries get packed in.
- new subpackages: contrib, doc
- renamed subpackage lib to libs to conform to the official RPMs
- ToDo: (semi)automatic conversion for updates
  from versions prior 7.1.
* Mon May  7 2001 mfabian@suse.de
- bzip2 sources
* Fri Apr 27 2001 max@suse.de
- updated the init script to be more LSB compliant according to
  the current /etc/init.d/skeleton.
* Thu Apr 12 2001 max@suse.de
- fix for deprecated declarations in readline 4.2.
- fixed permissons of some shared objects for the backend.
- recovered timestamps of sources.
* Wed Apr 11 2001 utuerk@suse.de
- added postgresql.conf for susehelp
* Thu Mar 22 2001 ro@suse.de
- added split-aliases as provides
* Thu Mar 22 2001 poeml@suse.de
- 7.0.* does not work on PPC unless compiled with -O0 (7.1 will)
* Wed Mar  7 2001 max@suse.de
- added xshared and xdevel to neededforbuild
  because X is no longer in the default buildsystem.
* Fri Feb 23 2001 ro@suse.de
- added readline/readline-devel to neededforbuild (split from bash)
* Wed Jan 24 2001 max@suse.de
- added missing "Provides:" entries to specfile.
* Mon Jan 15 2001 max@suse.de
- dropping the locale environment vars from the init script
  as workarround for a locale related bug in the backend.
  It shows up when the regression test runs on a backend that
  has e.g. LC_CTYPE=de_DE .
* Wed Nov 29 2000 max@suse.de
- new version: 7.0.3
- spec file is based on Lamar Owen's source RPM of
  PostgreSQL-7.0.3 for SuSE Linux 7.0
- renamed the whole package
    postgres -> postgresql
    pg_lib   -> postgresql-lib
    pg_serv  -> postgresql-serv
    pg_devel -> postgresql-devel
    pg_tcl   -> postgresql-tcl
    pg_tk    -> postgresql-tk
    pg_odbc  -> postgresql-odbc
    pg_jdbc  -> postgresql-jdbc
    pg_pyth  -> postgresql-python
    pg_perl  -> postgresql-perl
    pg_test  -> postgresql-test
- renamed some files and scripts from *postgres* to *postgresql*
- moved to the LSB-compliant init scheme
- moved database initialisation from SuSEconfig.postgres
  into the init script
- changed postgresql-python to use Python2.0 instead of 1.5
* Sat Oct 28 2000 kukuk@suse.de
- Add python-devel to need for build
* Tue Oct 24 2000 bk@suse.de
- integrated change from max:
- changed /sbin/init.d/postgres and SuSEconfig.postgres
  to work arround YaST that quotes the value of POSTGRES_DATADIR
  in /etc/rc.config when it gets changed.
* Mon Sep 11 2000 fober@suse.de
- made postgres run&autobuild on s390:
- src/include/port/linux.h, src/include/storage/s_lock.h:
  s390-assembler test-and-set (thanks to Andreas Jaeger)
- src/template/.similar, src/template/linux_s390:
  created linux_s390-Template from linux_ppc.
  TODO: is -O0 really needed?
- regression test passes (with minor deviations in floating point
  arithmetics)
  TODO: the regression test will not run out of the box as we install
  it.  this is the missing piece, either in postgres-source or in
  .spec
  [#] missing files
  cd $BUILD_ROOT/usr/src/packages/BUILD/postgresql-7.0.2/;
  cp -avP src/backend/*.h $RPM_BUILD_ROOT/usr/lib/pgsql
  cp -avP src/include $RPM_BUILD_ROOT/usr/lib/pgsql
  cp -avP src/Makefile.port $RPM_BUILD_ROOT/usr/lib/pgsql
  cp -avP src/Makefile.global $RPM_BUILD_ROOT/usr/lib/pgsql
  [#] directory structure
  cd $RPM_BUILD_ROOT/usr/lib/pgsql
  mkdir src
  mv test src
  ln -s src/test .
* Mon Aug 28 2000 max@suse.de
- changed installation order to fix bug #3802
* Mon Jul  3 2000 max@suse.de
- Disabled fcntl(F_SETLK) on the postmaster socket to work arround
  a kernel bug in Linux <= 2.2.16.
- New subpackage: pg_lib contains the shared libs for C and C++.
* Thu Jun 29 2000 schwab@suse.de
- Fix spinlocks for ia64.
- Reenable ia64 patch on the other architectures.
* Wed Jun 28 2000 max@suse.de
- disabled the ia64 patch when building for other architectures
- database unload+reload on updates works now
- moved some script and config files out of the diff into
  source files of their own.
- template database creation moved from init script into SuSEconfig
- some minor cleanups
* Tue Jun 20 2000 schwab@suse.de
- Add support for ia64.
* Fri Jun  9 2000 max@suse.de
- New version: 7.0.2.
- Re-made the whole package based on the original PostgreSQL RPM.
- There is still a little work needed for clean updates from
  PostgreSQL 6.x to 7.0.x
- Heavy testing needed before SuSE Linux 7.0.
* Sun Apr  9 2000 bk@suse.de
- added suse update config macro
- added automake to list of packages needed for building postgres
* Thu Feb 10 2000 ke@suse.de
- add more source files from the official PostgreSQL package.
- start to apply patches from there.
- start to cleanup the spec file.
- start to resolve bug #1948.
* Wed Feb  9 2000 ke@suse.de
- add group tag.
- ./configure -> %%build.
- New default for rc.config variable START_POSTGRES ("no").
* Fri Dec 10 1999 ke@suse.de
- update: version 6.5.3.
- startup script: use -S to remove the socket.
* Tue Oct 12 1999 ro@suse.de
- added tcld to neededforbuild
* Mon Sep 13 1999 bs@suse.de
- ran old prepare_spec on spec file to switch to new prepare_spec.
* Mon Aug  2 1999 ke@suse.de
- postgresql init script: remove the socket in /tmp before trying to
  start the postmaster.
* Thu Jul 29 1999 ke@suse.de
- update: version 6.5.1.
* Tue Jul 20 1999 ke@suse.de
- remove MANPATH setting from /etc/postgres.{sh,csh} and from
  /etc/pg_ifa.{sh,csh}.
- provide manpage links at /usr/share/man:
    /usr/lib/pgsql/man/man?/*.?.gz -> /urs/share/man/man?/*.?.pgsql.gz
- now, you'll find all manpage in "pg_ifa".
* Thu Mar 18 1999 ke@suse.de
- compile an install "spi" (on popular demand...).
* Wed Feb 10 1999 ke@suse.de
- security fix: don't create pg_pwd with mode 666 (thanks to mt).
* Mon Feb  1 1999 ke@suse.de
- fix permissions of libs (thanks to mt).
* Fri Jan  8 1999 ke@suse.de
- update: version 6.4.2.
* Tue Dec  1 1998 ke@suse.de
- add /etc/profile.d/{postgres,pg_ifa}.csh (thanks to werner).
- new bootscript (thanks to werner).
* Fri Nov 27 1998 ke@suse.de
- link libpgtcl against libcrypt.
* Thu Nov 12 1998 bs@suse.de
- fixed spec file for new rpm.
* Fri Oct 30 1998 ke@suse.de
- update: version 6.4-BETA4.
* Sun Sep 27 1998 ke@suse.de
- update: version pre6.4 (snapshot 1998-09-27).
- remove pgaccess (it's a separate package now).
- all libraries and binaries are under the separate hierarchy
  /usr/lib/pgsql (on customers' request...).
- provide /etc/profile.d/{postgres,pg_ifa}.sh; .csh files are still
  missing.
* Mon Aug 24 1998 ke@suse.de
- shut down the postmaster before uninstalling.
* Tue Aug 18 1998 ke@suse.de
- add pgaccess' GIFs (HTML documentation).
* Sat Jul 25 1998 ke@suse.de
- Use `-n postgres' to make the `%%post' script available.
* Mon Jul 13 1998 ke@suse.de
- update pgaccess: version 0.88.
* Thu May 28 1998 ke@suse.de
- New package split: rip out the base interfaces (libraries and database
  tools); the new package is called pg_ifa (subpackage).
- update pgaccess: version 0.87.
* Fri May 22 1998 ke@suse.de
- update: version 6.3.2
- package split to ease maintainability and user updates; now, we've the
  following packages:
  postgres : base packages, essential interfaces included (libpq,
  libpq++, libpqtcl and PgAccess).
  pg_datab : initial database (needed only for the first
  installation or in case of major number updates); if
  not installed, the user has to invoke `initdb'
  manually.
  pg_iface : PostgreSQL interfaces (Perl, JDBC, more to come...).
* Thu May  7 1998 fehr@suse.de
- add library -lXp for Motif 2.1
* Wed Feb 11 1998 fehr@suse.de
- added the perl interface
* Wed Dec 10 1997 ro@suse.de
- build static and dynamic version of dbbrowser and mpsql
* Wed Dec  3 1997 ro@suse.de
- fixed /sbin/init.d/postgres (path, db-path, read rc.config)
  moved logfile to /var/log
* Tue Nov 18 1997 bs@suse.de
- skipped man3/abort.3.gz
* Tue Nov  4 1997 fehr@suse.de
- changed to version 6.2.1 of the new postgresSQL
- changed to version 1.5 of mpsql
- changed to version 0.2 of AppGEN
- added version 0.9 if dbbrowser
- prepare package for automatic build
- home Directory of postgrs user must now be /var/lib/postgres
- this Change is a major step since postgres95 it is possible
  that some changes are incompatible with the previos postgres
  versions.
* Mon Jun  9 1997 fehr@suse.de
- make symbolic link in /usr/doc/packages relative
* Sun Jun  1 1997 bs@suse.de
- moved fillup stuff to var/adm/fillup-templates
* Mon May 12 1997 fehr@suse.de
- added startup-script for /sbin/init.d
- added fillup for /etc/rc.config START_POSTGRES
