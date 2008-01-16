%define prefix	/usr

Summary:	Sh shell procedural language handler for PostgreSQL
Name:		pgplsh
Version:	1.3
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://pgfoundry.org/frs/download.php/1534/%{name}-%{version}.tar.gz
Patch1:		%{name}-makefile.patch
URL:		http://pgfoundry.org/projects/pgplsh
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
%configure --prefix=%{_prefix} --libdir=%{_libdir} 
make %{?_smp_mflags} 

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/
install -d %{buildroot}%{_datadir}/%{name}
install -d %{buildroot}%{_docdir}/%{name}
install -m 755 .libs/%{name}.so %{buildroot}%{_libdir}/
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
%{_libdir}/%{name}.so*

%changelog
* Tue Jan 15 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 1.3-1
- Initial RPM packaging for Fedora
