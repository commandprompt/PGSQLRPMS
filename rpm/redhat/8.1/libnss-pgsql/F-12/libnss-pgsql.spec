Summary:	PostgreSQL NSS module
Name:		libnss-pgsql
Version:	1.5.0
Release:	beta_1%{?dist}
Group:		System Environment/Libraries
License:	BSD
Source0:	http://pgfoundry.org/frs/download.php/1878/%{name}-%{version}-beta.tgz
Patch0:		libnss-pgsql-includepath.patch
URL: 		http://pgfoundry.org/projects/sysauth/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	xmlto, postgresql-devel >= 8.1

%description
libnss-pgsql is a name service switch module that allows the 
replacement of flatfile passwd, group and shadow lookups with a 
PostgreSQL backend.

%prep
%setup -q -n %name-%{version}-beta
%patch0 -p0
%configure --with-docdir=%{_docdir}/%{name}-%{version}

%build
make

%install
rm -fr %{buildroot}
make DESTDIR=%{buildroot} install
install -d %{buildroot}/%{_docdir}-%{name}-%{version}/
mv doc/caution.png doc/nss-pgsql.html %{buildroot}/%{_docdir}-%{name}-%{version}/

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README conf/*
%{_libdir}/libnss_pgsql.a
%{_libdir}/libnss_pgsql.la
%{_libdir}/libnss_pgsql.so*
%{_docdir}-%{name}-%{version}/*

%changelog
* Tue Jan 13 2009 - Devrim GUNDUZ <devrim@commandprompt.com> 1.5.0-beta.1
- Initial packaging for PostgreSQL RPM Repository.
