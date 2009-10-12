Summary:	Enable planner hints for PostgreSQL
Name:		plantuner
Version:	0.0.1
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://pgfoundry.org/frs/download.php/2278/%{name}-%{version}.tar.bz2
URL:		http://www.sai.msu.su/~megera/wiki/plantuner
BuildRequires:	postgresql-devel >= 8.4
Requires:	postgresql-server >= 8.4
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
contrib/plantuner is a contribution module for PostgreSQL 8.4+, which 
enable planner hints.

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
install -p -m 755 sql/%{name}.sql %{buildroot}%{_datadir}/%{name}
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
* Mon Oct 12 2009 - Devrim GUNDUZ <devrim@commandprompt.com> 0.0.1-1
- Initial RPM packaging for Fedora
