%define sname	ip4r

Summary:	IPv4 and IPv4 range index types for PostgreSQL
Name:		postgresql-%{sname}
Version:	1.01
Release:	2%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://pgfoundry.org/frs/download.php/1226/%{sname}-%{version}.tar.gz
URL:		http://pgfoundry.org/projects/ip4r
BuildRequires:	postgresql-devel >= 8.1
Requires:	postgresql-server >= 8.1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
ip4 and ip4r are types that contain a single IPv4 address and a range of 
IPv4 addresses respectively. They can be used as a more flexible, 
indexable version of the cidr type.

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
install -p -m 755 %{sname}.sql %{buildroot}%{_datadir}/%{name}
install -p -m 755 README.%{sname} %{buildroot}%{_docdir}/%{name}-%{version}/README

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{_docdir}/%{name}-%{version}/README
%{_datadir}/%{name}
%{_datadir}/%{name}/%{sname}*.sql
%{_libdir}/pgsql/%{sname}.so

%changelog
* Mon Jul 9 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 1.01-2
- Removed unneeded ldconfig calls, per bz review #246747

* Wed Jul 4 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 1.01-1
- Initial RPM packaging for Fedora
