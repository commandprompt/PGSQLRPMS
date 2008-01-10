%define sname	table_log

Summary:	Log data changes in a PostgreSQL table
Name:		postgresql-%{sname}
Version:	0.4.4
Release:	2%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://pgfoundry.org/frs/download.php/1387/%{sname}-%{version}.tar.gz
URL:		http://pgfoundry.org/projects/tablelog
BuildRequires:	postgresql-devel >= 8.1
Requires:	postgresql-server >= 8.1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
table_log is a set of functions to log changes on a table in PostgreSQL
and to restore the state of the table or a specific row on any time
in the past.

%prep
%setup -q -n %{sname}-%{version}

%build
make USE_PGXS=1 %{?_smp_mflags} 

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/pgsql/
install -d %{buildroot}%{_datadir}/%{name}
install -d %{buildroot}%{_docdir}/%{name}-%{version}
install -m 755 %{sname}.so %{buildroot}%{_libdir}/pgsql/%{sname}.so
install -m 755 %{sname}.sql %{buildroot}%{_datadir}/%{name}
install -m 755 %{sname}_init.sql %{buildroot}%{_datadir}/%{name}
install -m 755 README.%{sname} %{buildroot}%{_docdir}/%{name}-%{version}/README

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig 
%postun -p /sbin/ldconfig 

%files
%defattr(644,root,root,755)
%doc %{_docdir}/%{name}-%{version}/README
%{_datadir}/%{name}/%{sname}*.sql
%{_libdir}/pgsql/%{sname}.so

%changelog
* Sat Jun 17 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 0.4.4-2
- Added Requires, per bugzilla review #244536 (Thanks Ruben)
- Renamed README file, per bugzilla review #244536

* Sat Jun 16 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 0.4.4-1
- Initial RPM packaging for Fedora
