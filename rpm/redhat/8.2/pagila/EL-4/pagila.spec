Summary:	A sample database for PostgreSQL
Name:		pagila
Version:	0.10.0
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
URL:		http://pgfoundry.org/projects/dbsamples
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	http://pgfoundry.org/frs/download.php/1556/%{name}-%{version}.zip

Requires:	postgresql
Buildarch:	noarch

%define		_pagiladir  %{_datadir}/%{name}

%description
Pagila is a port of the Sakila example database available for MySQL, which was
originally developed by Mike Hillyer of the MySQL AB documentation team. It
is intended to provide a standard schema that can be used for examples in
books, tutorials, articles, samples, etc.

%prep
%setup -q -n %{name}-%{version}

%build

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_pagiladir}
install -m 644 -p *.sql %{buildroot}%{_pagiladir}

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc README
%dir %{_pagiladir}
%attr(644,root,root) %{_pagiladir}/*.sql

%changelog
* Fri Feb 1 2008 Devrim Gunduz <devrim@commandprompt.com> 0.10.0-1
- Initial packaging for Fedora/EPEL
