Summary:	Procedural language interface between PostgreSQL and R
Name:		plr
Version:	8.2.0.5
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://pgfoundry.org/frs/download.php/1403/%{name}-%{version}.tar.gz
URL:		http://pgfoundry.org/projects/plr
BuildRequires:	postgresql-devel >= 8.1
Requires:	postgresql-server >= 8.1, R
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Procedural Language Handler for the "R software environment for 
statistical computing and graphics".

%prep
%setup -q -n %{name}

%build
make R_HOME=%{_libdir}/R/ USE_PGXS=1 %{?_smp_mflags} 

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/pgsql/
install -d %{buildroot}%{_datadir}/%{name}
install -d %{buildroot}%{_docdir}/%{name}-%{version}
install -m 755 lib%{name}.so %{buildroot}%{_libdir}/pgsql/%{name}.so
install -m 755 %{name}.sql %{buildroot}%{_datadir}/%{name}
install -m 755 README.%{name} %{buildroot}%{_docdir}/%{name}-%{version}/README

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig 
%postun -p /sbin/ldconfig 

%files
%defattr(644,root,root,755)
%doc %{_docdir}//%{name}-%{version}/README
%{_datadir}/%{name}/%{name}*.sql
%{_libdir}/pgsql/%{name}.so*

%changelog
* Wed Jul 4 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 8.2.0.5-1
- Initial RPM packaging for Fedora
