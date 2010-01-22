Summary:	Implementation of some Oracle functions into PostgreSQL
Name:		orafce
Version:	3.0RC1
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://pgfoundry.org/frs/download.php/2185/%{name}-%{version}.tar.gz
URL:		http://pgfoundry.org/projects/orafce/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	postgresql-devel, bison, flex, openssl-devel, krb5-devel
Requires:	postgresql

%description 	
The goal of this project is implementation some functions from Oracle database. 
Some date functions (next_day, last_day, trunc, round, ...) are implemented 
now. Functionality was verified on Oracle 10g and module is useful 
for production work.

%prep
%setup -q -n %{name}

%build
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS

USE_PGXS=1 make %{?_smp_mflags} 

%install
rm -rf %{buildroot}
make USE_PGXS=1 %{?_smp_mflags} DESTDIR=%{buildroot} install

install -d %{buildroot}%{_libdir}/pgsql/
install -d %{buildroot}%{_datadir}/%{name}-%{version}
install -d %{buildroot}%{_docdir}/%{name}-%{version}
install -p -m 755 liborafunc.so.0.0 %{buildroot}%{_libdir}/pgsql/orafunc.so
install -p -m 644 uninstall_orafunc.sql orafunc.sql %{buildroot}%{_datadir}/%{name}-%{version}
install -m 644 README.orafunc INSTALL.orafunc COPYRIGHT.orafunc %{_docdir}/%{name}-%{version}

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%dir %{_datadir}/pgsql/contrib
%{_datadir}/%{name}-%{version}/*.sql
%{_libdir}/pgsql/orafunc.so
%doc README.orafunc INSTALL.orafunc COPYRIGHT.orafunc

%changelog
* Tue May 19 2009 - Devrim GUNDUZ <devrim@commandprompt.com> 3.0RC1-1
- Update to 3.0RC1

* Wed Aug 20 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 2.1.4-1
- Update to 2.1.4

* Sun Jan 20 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 2.1.3-2
- Spec file fixes, per bz review #251805

* Mon Jan 14 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 2.1.3-1
- Update to 2.1.3

* Fri Aug 10 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 2.1.1-1
- Update to 2.1.1
- Spec file cleanup

* Wed Aug 30 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0.1-1
- Initial packaging
