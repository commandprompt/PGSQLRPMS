Summary:	A PostgreSQL API to interface with memcached.
Name:		pgmemcache
Version:	1.2beta1
Release:	3%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://pgfoundry.org/frs/download.php/1300/%{name}-%{version}.tar.gz
URL:		http://pgfoundry.org/projects/pgmemcache
BuildRequires:	postgresql-devel >= 8.1
Requires:	postgresql-server >= 8.1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
pgmemcache is a set of PostgreSQL user-defined functions that provide
an interface to memcached.

%prep
%setup -q -n %{name}-%{version}

%build
make USE_PGXS=1 %{?_smp_mflags} 

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/pgsql/
install -d %{buildroot}%{_datadir}/%{name}
install -d %{buildroot}%{_docdir}/%{name}-%{version}
install -m 755 %{name}.so %{buildroot}%{_libdir}/pgsql/%{name}.so
install -m 755 %{name}.sql %{buildroot}%{_datadir}/%{name}
install -m 755 %{name}_init.sql %{buildroot}%{_datadir}/%{name}
install -m 755 README.%{name} %{buildroot}%{_docdir}/%{name}-%{version}/README

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig 
%postun -p /sbin/ldconfig 

%files
%defattr(644,root,root,755)
%doc %{_docdir}//%{name}-%{version}/README
%{_datadir}/%{name}/%{name}*.sql
%{_libdir}/pgsql/%{name}.so

%changelog
* Wed Apr 9 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 0.4.4-3
- Initial commit for pgsqlrpms.org repo.

* Sat Jun 17 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 0.4.4-2
- Added Requires, per bugzilla review #244536 (Thanks Ruben)
- Renamed README file, per bugzilla review #244536

* Sat Jun 16 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 0.4.4-1
- Initial RPM packaging for Fedora
