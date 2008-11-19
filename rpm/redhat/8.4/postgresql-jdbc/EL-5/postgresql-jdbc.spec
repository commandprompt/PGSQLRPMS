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
# Peter Eisentraut

# This spec file and ancilliary files are licensed in accordance with
# The PostgreSQL license.
# In this file you can find the default build package list macros.  These can be overridden by defining
# on the rpm command line

%{!?upstreamserver:%define upstreamver	8.3-604}
%{!?gcj_support:%define gcj_support	1}

%define beta 0
%{?beta:%define __os_install_post /usr/lib/rpm/brp-compress}

Summary:	JDBC driver for PostgreSQL
Name:		postgresql-jdbc
Version:	8.3.604
Release:	1PGDG%{?dist}
Epoch:		0
License:	BSD
Group:		Applications/Databases
URL:		http://jdbc.postgresql.org/

Source0:	http://jdbc.postgresql.org/download/%{name}-%{upstreamver}.src.tar.gz

%if %{gcj_support}
%else
BuildArch:	noarch
%endif
BuildRequires:  jpackage-utils >= 0:1.5
BuildRequires:  ant >= 0:1.6.2
BuildRequires:  ant-junit >= 0:1.6.2
BuildRequires:  junit >= 0:3.7
BuildRequires:	findutils gettext
%if %{gcj_support}
BuildRequires:	gcc-java
Requires(post):	/usr/bin/rebuild-gcj-db
Requires(postun):	/usr/bin/rebuild-gcj-db
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-jdbc package includes the .jar files needed for
Java programs to access a PostgreSQL database.

%prep
%setup -c -q
mv -f %{name}-%{upstreamver}.src/* .
rm -f %{name}-%{upstreamver}.src/.cvsignore
rmdir %{name}-%{upstreamver}.src

# remove any binary libs
find -name "*.jar" -or -name "*.class" | xargs rm -f

%build
export OPT_JAR_LIST="ant/ant-junit junit"
export CLASSPATH=
sh update-translations.sh
ant

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_javadir}
# Per jpp conventions, jars have version-numbered names and we add
# versionless symlinks.
install -m 644 jars/postgresql.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar

pushd %{buildroot}%{_javadir}
ln -s %{name}-%{version}.jar %{name}.jar
# Also, for backwards compatibility with our old postgresql-jdbc packages,
# add these symlinks.  (Probably only the jdbc3 symlink really makes sense?)
ln -s postgresql-jdbc.jar postgresql-jdbc2.jar
ln -s postgresql-jdbc.jar postgresql-jdbc2ee.jar
ln -s postgresql-jdbc.jar postgresql-jdbc3.jar
popd

%if %{gcj_support}
aot-compile-rpm
%endif

strip %{buildroot}/%{_libdir}/gcj/%{name}/*.jar.so

%clean
rm -rf %{buildroot}

%if %{gcj_support}
%post -p /usr/bin/rebuild-gcj-db
%postun -p /usr/bin/rebuild-gcj-db
%endif

%files
%defattr(-,root,root)
%doc LICENSE README doc/* 
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%{_libdir}/gcj/%{name}/*.jar.so
%{_libdir}/gcj/%{name}/*.jar.db
%endif

%changelog
* Wed Nov 19 2008 Devrim Gunduz <devrim@CommandPrompt.com> 0:8.3.604-1PGDG
- Update to build 604

* Thu Jan 31 2008 Devrim Gunduz <devrim@CommandPrompt.com> 0:8.3.603-1PGDG
- Update to build 603 (first stable release for 8.3)

* Tue Jan 1 2008 Devrim Gunduz <devrim@CommandPrompt.com> 0:8.3.602-2PGDG
- Updated gcj_support requires, per Fedora spec file
- Fix buildroot
- Cosmetic cleanup

* Tue Dec 4 2007 Devrim Gunduz <devrim@CommandPrompt.com> 0:8.3.602-1PGDG
- Update to build 602

* Sun Nov 4 2007 Devrim Gunduz <devrim@CommandPrompt.com> 0:8.3.601-1PGDG
- First cut for 8.3
- Removed unused section macro.

* Mon Sep 3 2007 Devrim Gunduz <devrim@CommandPrompt.com> 0:8.2.506-1PGDG
- Update to build 506
- Add {?dist} to release tag.

* Wed Apr 18 2007 Devrim Gunduz <devrim@CommandPrompt.com> 0:8.2.505-1PGDG
- Update to build 505

* Sun Dec 3 2006 Devrim Gunduz <devrim@CommandPrompt.com> 0:8.2.504-1PGDG
- Update to 8.2 build 504

* Thu Oct 19 2006 Devrim Gunduz <devrim@CommandPrompt.com> 0:8.2.407-1PGDG
- Rebuilt for PostgreSQL 8.2

* Sat Oct 14 2006 Devrim Gunduz <devrim@CommandPrompt.com> 0:8.1.407-4PGDG
- Fixed more rpmlint warnings and errors

* Sat Aug 12 2006 Devrim Gunduz <devrim@CommandPrompt.com> 0:8.1.407-3PGDG
- Fixed rpmlint warnings and errors
- Renamed spec file to meet rpm guidelines

* Mon Jul 17 2006 Devrim Gunduz <devrim@CommandPrompt.com> 0:8.1.407-2PGDG
- Rebuilt for PostgreSQL 8.1

* Mon Jul 10 2006 Devrim Gunduz <devrim@CommandPrompt.com> 0:8.1.407-1PGDG
- Updated macro definitions
- Initial build for PGDG RPM Set

* Wed Jun 14 2006 Tom Lane <tgl@redhat.com> 8.1.407-1jpp
- Update to build 8.1-407

* Mon Mar 27 2006 Tom Lane <tgl@redhat.com> 8.1.405-2jpp
- Back-patch upstream fix to support unspecified-type strings.

* Thu Feb 16 2006 Tom Lane <tgl@redhat.com> 8.1.405-1jpp
- Split postgresql-jdbc into its own SRPM (at last).
- Build it from source.  Add support for gcj compilation.
