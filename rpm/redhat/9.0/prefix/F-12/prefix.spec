Summary:	Prefix Opclass for PostgreSQL
Name:		prefix
Version:	1.1.0
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://pgfoundry.org/frs/download.php/2477/%{name}-%{version}.tar.gz
URL:		http://pgfoundry.org/projects/prefix
BuildRequires:	postgresql-devel >= 8.2
Requires:	postgresql-server >= 8.2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The prefix project implements text prefix matches operator (prefix @> 
text) and provide a GiST opclass for indexing support of prefix 
searches.

%prep
%setup -q

%build
make %{?_smp_mflags} 

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_libdir}/pgsql/
install -d %{buildroot}%{_datadir}/%{name}
install -d %{buildroot}%{_docdir}/%{name}-%{version}

install -m 755 prefix.so %{buildroot}%{_libdir}/pgsql
install -m 644 *.sql %{buildroot}%{_datadir}/%{name}/
install -m 644 *.csv %{buildroot}%{_datadir}/%{name}/
install -m 644 *.txt %{buildroot}%{_docdir}/%{name}-%{version}/

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README.txt TESTS.txt
%{_datadir}/%{name}/*.sql
%{_datadir}/%{name}/*.csv
%{_libdir}/pgsql/prefix.so

%changelog
* Fri Dec 11 2009 - Devrim GUNDUZ <devrim@commandprompt.com> 1.1.0-1
- Update to 1.1.0

* Fri May 30 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 0.2-1
- Initial RPM packaging for yum.pgsqlrpms.org 
