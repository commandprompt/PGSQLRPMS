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

# Major Contributors:
# ---------------
# Tom Lane
# Devrim Gunduz

# This spec file and ancilliary files are licensed in accordance with
# The PostgreSQL license.
# In this file you can find the default build package list macros.  These can be overridden by defining
# on 

Name:		postgresql-odbc
Summary:	PostgreSQL ODBC driver
Version:	08.03.0400
Release:	1PGDG%{?dist}
License:	LGPL
Group:		Applications/Databases
Url:		http://pgfoundry.org/projects/psqlodbc/

Source0:	ftp://ftp.postgresql.org/pub/odbc/versions/src/psqlodbc-%{version}.tar.gz
Source1:	acinclude.m4

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	unixODBC-devel
BuildRequires:	libtool automake autoconf postgresql-devel

Requires:	postgresql-libs

# This spec file and ancillary files are licensed in accordance with 
# the psqlodbc license.

%description
This package includes the driver needed for applications to access a
PostgreSQL system via ODBC (Open Database Connectivity).

%prep
%setup -q -n psqlodbc-%{version}

# Some missing macros.  Courtesy Owen Taylor <otaylor@redhat.com>.

cp -p %{SOURCE1} .
aclocal
libtoolize --force
automake
autoconf

%build

# Note: we choose to build only the Unicode version of the driver, which
# we then install under the old library name "psqlodbc.so".  We are not
# adopting the "psqlodbcw.so" naming convention because current upstream
# plans are to revert back to the old name in the next release.  We can
# always track the name change later if they change their minds ...

%configure --with-unixodbc --with-odbcinst=%{_sysconfdir}
make

%install
rm -rf %{buildroot}
%makeinstall

# rename as per above note, and remove the rather useless .la file
pushd %{buildroot}%{_libdir}
	mv psqlodbcw.so psqlodbc.so
	rm psqlodbcw.la
popd
strip %{buildroot}%{_libdir}/*.so

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%attr(755,root,root) %{_libdir}/psqlodbc.so
%doc license.txt readme.txt 

%changelog
* Sun Feb 1 2009 Devrim GUNDUZ <devrim@commandprompt.com> 08.03.0400-1PGDG
- Update to 08.03.0400

* Mon Jun 16 2008 Devrim GUNDUZ <devrim@commandprompt.com> 08.03.0200-1PGDG
- Update to 08.03.0200
- Fix download URL

* Thu Jan 31 2008 Devrim GUNDUZ <devrim@commandprompt.com> 08.03.0100-1PGDG
- Update to 08.03.0100

* Sun Nov 04 2007 Devrim GUNDUZ <devrim@commandprompt.com> 08.02.0500-1PGDG
- Update to 08.02.0500
- Updated project URL
- Fix dist tag
- Use a more proper Requires and Release info

* Mon Sep 3 2007 Devrim GUNDUZ <devrim@commandprompt.com> 08.02.0400-1PGDG
- Update to  08.02.0400
- Add {?dist} to release tag.

* Sat Dec 16 2006 Devrim GUNDUZ <devrim@commandprompt.com> 08.02.0203-1PGDG
- Update to 08.02.0203

* Sun Dec 3 2006 Devrim GUNDUZ <devrim@commandprompt.com> 08.02.0200-1PGDG
- Update to 08.02.0200

* Sat Oct 14 2006 Devrim GUNDUZ <devrim@commandprompt.com> 08.02.0100-2PGDG
- Fix rpmlint warnings and errors.

* Fri Oct 06 2006 Devrim GUNDUZ <devrim@commandprompt.com> 08.02.0100-1
- Update to 08.02.0100
- Fix URL
- Fix spec for new release

* Sat Aug 12 2006 Devrim Gunduz <devrim@commandprompt.com> 08.02.0002-3
- Fixed rpmlint errors and warnings
- Cosmetic cleanup
- Fixed changelog

* Mon Jul 17 2006 Devrim Gunduz <devrim@commandprompt.com> 08.02.0002-2
- Rebuilt for PostgreSQL 8.1

* Mon Jul 10 2006 Devrim Gunduz <devrim@commandprompt.com> 08.01.0200-3
- Initial build for PGDG RPM Set

* Sat Jun 10 2006 Tom Lane <tgl@redhat.com> 08.01.0200-3
- Fix BuildRequires: for mock build environment

* Wed Mar 22 2006 Tom Lane <tgl@redhat.com> 08.01.0200-2
- Change library name back to psqlodbc.so, because it appears that upstream
  will revert to that name in next release; no point in thrashing the name.
- Include documentation files unaccountably omitted before (bug #184158)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 08.01.0200-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 08.01.0200-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb  3 2006 Tom Lane <tgl@redhat.com> 08.01.0200-1
- Update to version 08.01.0200.
- Upstream now calls the library psqlodbcw.so ... add a symlink to avoid
  breaking existing odbc configuration files.

* Wed Dec 14 2005 Tom Lane <tgl@redhat.com> 08.01.0102-1
- Update to version 08.01.0102.
- Add buildrequires postgresql-devel (bz #174505)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov  7 2005 Tom Lane <tgl@redhat.com> 08.01.0100-1
- Update to version 08.01.0100.

* Wed Mar  2 2005 Tom Lane <tgl@redhat.com> 08.00.0100-1
- Update to version 08.00.0100.

* Fri Nov 12 2004 Tom Lane <tgl@redhat.com> 7.3-9
- back-port 64-bit fixes from current upstream (bug #139004)

* Tue Sep 21 2004 Tom Lane <tgl@redhat.com> 7.3-8
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Mar 10 2004 Tom Lane <tgl@redhat.com>
- Correct License: annotation.

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Nov 21 2003 David Jee <djee@redhat.com> 7.3-5
- rebuild

* Wed Nov 05 2003 David Jee <djee@redhat.com> 7.3-4
- import new community version 07.03.0200

* Mon Sep 15 2003 Andrew Overholt <overholt@redhat.com> 7.3-3
- autotools fixes (courtesy Alex Oliva <aoliva@redhat.com> and 
  Owen Taylor <otaylor@redhat.com>)

* Tue Jul 08 2003 Andrew Overholt <overholt@redhat.com> 7.3-3
- allow use with unixODBC (courtesy Troels Arvin) [Bug #97998]

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun 02 2003 Andrew Overholt <overholt@redhat.com> 7.3-1
- sync to new community version (07.03.0100 => v7.3, r1)

* Thu Jan 23 2003 Tim Powers <timp@redhat.com> 1-2
- rebuild

* Tue Jan 14 2003 Andrew Overholt <overholt@redhat.com>
- 1-1
- initial build (just took old package sections)
