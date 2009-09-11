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

%define beta 0
%{?beta:%define __os_install_post /usr/lib/rpm/brp-compress}

%{!?upstreamserver:%define upstreamver	8.0-324}

Summary:	JDBC driver for PostgreSQL
Name:		postgresql-jdbc
Version:	8.0.324
Release:	1PGDG%{?dist}
BuildArch:	noarch
Epoch:		0
License:	BSD
Group:		Applications/Databases
URL:		http://jdbc.postgresql.org/

Source1:	http://jdbc.postgresql.org/download/postgresql-%{upstreamver}.jdbc2.jar
Source2:	http://jdbc.postgresql.org/download/postgresql-%{upstreamver}.jdbc2ee.jar
Source3:	http://jdbc.postgresql.org/download/postgresql-%{upstreamver}.jdbc3.jar

BuildRoot:	%{_tmppath}/%{name}-%{upstreamver}-%{release}-root-%(%{__id_u} -n)

%description
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-jdbc package includes the .jar files needed for
Java programs to access a PostgreSQL database.

%build

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_javadir}
install -m 755 %{SOURCE1} %{buildroot}%{_javadir}
install -m 755 %{SOURCE2} %{buildroot}%{_javadir}
install -m 755 %{SOURCE3} %{buildroot}%{_javadir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_javadir}/postgresql-%{upstreamver}.jdbc2.jar
%{_javadir}/postgresql-%{upstreamver}.jdbc2ee.jar
%{_javadir}/postgresql-%{upstreamver}.jdbc3.jar

%changelog
* Sat Sep 12 2009 Devrim Gunduz <devrim@CommandPrompt.com> 0:8.0.324-1PGDG
- Update to build 324
- Use non-src version for F-7, it does not have build  environment from source.
