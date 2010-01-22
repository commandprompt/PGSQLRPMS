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
# Devrim Gunduz

# This spec file and ancilliary files are licensed in accordance with
# The PostgreSQL license.
# In this file you can find the default build package list macros.  These can be overridden by defining
# on the rpm command line

%{!?aconfver:%define aconfver autoconf}

Summary:	Tcl client library for PostgreSQL
Name:		postgresql-tcl
Version:	1.6.2
Release:	2PGDG%{?dist}
Epoch:		0
License:	BSD
Group:		Applications/Databases
URL:		http://pgfoundry.org/projects/pgtclng
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	http://pgfoundry.org/frs/download.php/1545/pgtcl1.6.2.tar.gz
Source1:	http://pgfoundry.org/frs/download.php/1228/pgtcldocs-20070115.zip

Patch0:		pgtcl-no-rpath.patch

BuildRequires:	tcl-devel postgresql-devel
Requires:	libpq.so tcl >= 8.5

%description
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-tcl package contains the Pgtcl client library
and its documentation.

%prep
%setup -c -q

tar xzf %{SOURCE0}
PGTCLDIR=`basename %{SOURCE0} .tar.gz`
mv $PGTCLDIR Pgtcl
unzip %{SOURCE1}
PGTCLDOCDIR=`basename %{SOURCE1} .zip`
mv $PGTCLDOCDIR Pgtcl-docs

%patch0 -p0
	pushd Pgtcl
%aconfver
	popd

%build
pushd Pgtcl
# pgtcl's configure only handles one include directory :-(
./configure \
	--libdir=%{_libdir} \
	--with-tcl=%{_libdir} \
	--with-postgres-include="../src/interfaces/libpq -I../src/include" \
	--with-postgres-lib=../src/interfaces/libpq
# note: as of pgtcl 1.5.2, its makefile is not parallel-safe
make all
popd

%install
rm -rf %{buildroot}
TCL_VERSION=`echo 'puts $tcl_version' | tclsh`
TCLLIBDIR="%{_libdir}/tcl$TCL_VERSION"
# check the target directory is a dir, not a symlink
if [ -h "$TCLLIBDIR" ] ; then
	echo "$TCLLIBDIR must not be a symlink"
	exit 1
fi
PGTCL_DIR="${RPM_BUILD_ROOT}${TCLLIBDIR}/Pgtcl"
install -d -m 755 "$PGTCL_DIR"
cp Pgtcl/pkgIndex.tcl "$PGTCL_DIR"
cp Pgtcl/libpgtcl*.so "$PGTCL_DIR"

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/tcl*/Pgtcl/
%doc Pgtcl-docs/*

%changelog
* Fri Aug 8 2008 Devrim Gunduz <devrim@commandprompt.com> 0:1.6.2-2PGDG
- Install Pgtcl in /usr/lib/tcl$TCL_VERSION, not directly in /usr/lib.
Needed because tcl 8.5 no longer puts /usr/lib into its package search path.
NOTE: do not back-port this change into branches using pre-8.5 tcl, because
/usr/lib/tcl8.4 had been a symlink to /usr/share/tcl8.4, and /usr/share
is exactly where we must not put Pgtcl. Resolves: #228263. Patch and changelog
text is from Tom.
  	 
* Sun Dec 30 2007 Devrim Gunduz <devrim@commandprompt.com> 0:1.6.2-1PGDG
- Update to 1.6.2

* Mon Sep 3 2007 Devrim Gunduz <devrim@commandprompt.com> 0:1.6.0-2PGDG
- Add {?dist} to release tag.

* Sun Feb 4 2007 Devrim Gunduz <devrim@CommandPrompt.com> 0:1.6.0-1PGDG
- Added postgresql-devel to buildrequires, per Stefan Kaltenbrunner
- Update to 1.6.0
- Update URLs

* Sat Oct 14 2006 Devrim Gunduz <devrim@CommandPrompt.com> 0:1.5.2-5PGDG
- Rebuilt

* Sat Oct 14 2006 Devrim Gunduz <devrim@CommandPrompt.com> 0:1.5.2-4PGDG
- strip .so file

* Sat Aug 12 2006 Devrim Gunduz <devrim@CommandPrompt.com> 0:1.5.2-3PGDG
- Fixed rpmlint warnings and errors

* Mon Jul 10 2006 Devrim Gunduz <devrim@CommandPrompt.com> 0:1.5.2-2PGDG
- Rebuilt for PostgreSQL 8.1

* Mon Jul 10 2006 Devrim Gunduz <devrim@CommandPrompt.com> 0:1.5.2-1PGDG
- Initial build for PGDG RPM Set
