Summary:	The USDA Food Database Sample for PostgreSQL
Name:		usda-r18
Version:	1.0
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
URL:		http://pgfoundry.org/projects/dbsamples
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	http://pgfoundry.org/frs/download.php/555/%{name}-%{version}.tar.gz

Requires:	postgresql
Buildarch:	noarch

%define		_usdadir  %{_datadir}/%{name}

%description
The USDA Food Database is published by the US Department of Agriculture.

%prep
%setup -q -n %{name}-%{version}

%build

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_usdadir}
install -m 644 -p *.sql %{buildroot}%{_usdadir}

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc README
%dir %{_usdadir}
%attr(644,root,root) %{_usdadir}/*.sql

%changelog
* Sat Feb 2 2008 Devrim Gunduz <devrim@commandprompt.com> 1.0-1
- Initial packaging for Fedora/EPEL
