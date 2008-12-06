Summary:	IPv4 and IPv4 range index types for PostgreSQL
Name:		ip4r
Version:	1.03
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://pgfoundry.org/frs/download.php/1581/%{name}-%{version}.tar.gz
URL:		http://pgfoundry.org/projects/ip4r
BuildRequires:	postgresql-devel >= 8.0
Requires:	postgresql-server >= 8.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
ip4 and ip4r are types that contain a single IPv4 address and a range of 
IPv4 addresses respectively. They can be used as a more flexible, 
indexable version of the cidr type.

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
install -p -m 755 %{name}.sql %{buildroot}%{_datadir}/%{name}
install -p -m 755 README.%{name} %{buildroot}%{_docdir}/%{name}-%{version}/README

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{_docdir}/%{name}-%{version}/README
%{_datadir}/%{name}
%{_datadir}/%{name}/%{name}*.sql
%{_libdir}/pgsql/%{name}.so

%changelog
* Fri Feb 1 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 1.03-1
- Update to 1.03

* Sun Jan 20 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 1.02-1
- Update to 1.02

* Mon Jul 9 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 1.01-2
- Removed unneeded ldconfig calls, per bz review #246747

* Wed Jul 4 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 1.01-1
- Initial RPM packaging for Fedora
