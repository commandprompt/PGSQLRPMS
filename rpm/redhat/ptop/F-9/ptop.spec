Summary:	'top' for PostgreSQL process
Name:		ptop
Version:	3.6.1
Release:	1.beta2%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://pgfoundry.org/frs/download.php/1538/%{name}-%{version}-beta2.tar.gz
Patch1:		%{name}-makefile.patch
URL:		http://pgfoundry.org/projects/ptop
BuildRequires:	postgresql-devel >= 8.1
Requires:	postgresql-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
ptop is 'top' for PostgreSQL processes. See running queries, 
query plans, issued locks, and table and index statistics.

%prep
%setup -q -n %{name}-%{version}-beta2
%patch1 -p0

%build
%configure
make %{?_smp_mflags} 

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}/
install -d %{buildroot}%{_mandir}/
install -d %{buildroot}%{_mandir}/man1
install -m 755 %{name} %{buildroot}%{_bindir}/
install -m 644 %{name}.1 %{buildroot}%{_mandir}/man1/
strip %{buildroot}%{_bindir}/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_mandir}/man1/%{name}*
%{_bindir}/%{name}

%changelog
* Mon Dec 13 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 3.6.1-1.beta2
- Initial RPM packaging for Fedora