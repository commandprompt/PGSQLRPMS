%define prefix	/usr

Summary:	Sh shell procedural language handler for PostgreSQL
Name:		pgplsh
Version:	1.3
Release:	2%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://pgfoundry.org/frs/download.php/1534/%{name}-%{version}.tar.gz
Patch1:		%{name}-makefile.patch
URL:		http://pgfoundry.org/projects/plsh
BuildRequires:	postgresql-devel >= 8.2
Requires:	postgresql-server >= 8.2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
PL/sh is a procedural language handler for PostgreSQL that 
allows you to write stored procedures in a shell of your choice.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p0

%build
%configure --prefix=%{_prefix} --libdir=%{_libdir}/pgsql
make %{?_smp_mflags} 

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/
install -d %{buildroot}%{_libdir}/pgsql
install -d %{buildroot}%{_datadir}/%{name}
install -d %{buildroot}%{_docdir}/%{name}
install -m 755 .libs/%{name}.so %{buildroot}%{_libdir}/pgsql/
install -m 755 createlang_%{name}.sql %{buildroot}%{_datadir}/%{name}/
install -m 755 test.sql %{buildroot}%{_datadir}/%{name}/
install -m 755 README %{buildroot}%{_docdir}/%{name}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig 
%postun -p /sbin/ldconfig 

%files
%defattr(644,root,root,755)
%doc %{_docdir}/%{name}/README
%{_datadir}/%{name}/*.sql
%{_libdir}/pgsql/%{name}.so*

%changelog
* Sun Jan 20 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 1.3-2
- Move .so file to the correct directory

* Tue Jan 15 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 1.3-1
- Initial RPM packaging for Fedora
