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
#Tom Lane
#Devrim Gunduz
#Peter Eisentraut

# This spec file and ancilliary files are licensed in accordance with
# The PostgreSQL license.
# In this file you can find the default build package list macros.  These can be overridden by defining
# on the rpm command line

%{!?upstreamserver:%define upstreamver	8.0-322}
%{!?gcj_support:%define gcj_support	1}

%define beta 0
%{?beta:%define __os_install_post /usr/lib/rpm/brp-compress}

Summary:	JDBC driver for PostgreSQL
Name:		postgresql-jdbc
Version:	8.0.322
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
rm -rf ${RPM_BUILD_ROOT}

install -d $RPM_BUILD_ROOT%{_javadir}
# Per jpp conventions, jars have version-numbered names and we add
# versionless symlinks.
install -m 644 jars/postgresql.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar

pushd $RPM_BUILD_ROOT%{_javadir}
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

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post -p /usr/bin/rebuild-gcj-db
%postun -p /usr/bin/rebuild-gcj-db
%endif

%files
%defattr(-,root,root)
%doc LICENSE README doc/* example
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%{_libdir}/gcj/%{name}/*.jar.so
%{_libdir}/gcj/%{name}/*.jar.db
%endif

%changelog
* Thu Jan 31 2008 Devrim Gunduz <devrim@CommandPrompt.com> 0:8.0.322-1PGDG
- Update to build 322

* Tue Jan 1 2008 Devrim Gunduz <devrim@CommandPrompt.com> 0:8.0.321-2PGDG
- Updated gcj_support requires, per Fedora spec file
- Fix buildroot
- Cosmetic cleanup
- Removed unused section macro

* Tue Dec 4 2007 Devrim Gunduz <devrim@CommandPrompt.com> 0:8.0.321-1PGDG
- Update to build 321

* Wed Apr 18 2007 Devrim Gunduz <devrim@CommandPrompt.com> 0:8.0.319-1PGDG
- Update to build 319

* Sun Feb 4 2007 Devrim Gunduz <devrim@CommandPrompt.com> 0:8.0.318-1PGDG
- Update to build 318

* Fri Oct 06 2006 Devrim Gunduz <devrim@CommandPrompt.com> 0:8.0.317-1PGDG
- Initial build for PGDG 8.0 RPM Set

