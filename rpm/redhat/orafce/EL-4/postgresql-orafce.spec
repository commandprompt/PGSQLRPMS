%define sname	orafce

Summary:	Implementation of some Oracle functions into PostgreSQL
Name:		postgresql-%{sname}
Version:	2.1.1
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://pgfoundry.org/frs/download.php/1301/%{sname}-%{version}.tar.gz
URL:		http://pgfoundry.org/projects/orafce/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)

BuildRequires:	postgresql-devel
Requires:	postgresql

%description 	
The goal of this project is implementation some functions from Oracle database. 
Some date functions (next_day, last_day, trunc, round, ...) are implemented 
now. Functionality was verified on Oracle 10g and module is useful 
for production work.

%prep
%setup -q -n %{sname}

%build
USE_PGXS=1 make %{?_smp_mflags} 

%install
rm -rf %{buildroot}
USE_PGXS=1 make %{?_smp_mflags} install

install -d %{buildroot}%{_libdir}/pgsql/
install -m 755 liborafunc.so.0.0 %{buildroot}%{_libdir}/pgsql/orafunc.so

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc README.orafunc INSTALL.orafunc COPYRIGHT.orafunc orafunc.sql
%{_libdir}/pgsql/orafunc.so

%changelog
* Fri Aug 10 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 2.1.1-1
- Update to 2.1.1
- Spec file cleanup

* Wed Aug 30 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0.1-1
- Initial packaging
