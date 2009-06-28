Summary:	'top' for PostgreSQL process
Name:		pg_top
Version:	3.6.2
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://pgfoundry.org/frs/download.php/1780/%{name}-%{version}.tar.bz2
Patch1:		%{name}-makefile.patch
URL:		http://pgfoundry.org/projects/ptop
BuildRequires:	postgresql-devel >= 8.1, libtermcap-devel
Requires:	postgresql-server >= 8.1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Obsoletes:	ptop => 3.5.0

%description
pg_top is 'top' for PostgreSQL processes. See running queries, 
query plans, issued locks, and table and index statistics.

%prep
%setup -q -n %{name}-%{version}
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
* Thu May 15 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 3.6.2-1
- Update to 3.6.2

* Sat Apr 12 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 3.6.2-0.1.beta3
- Rename to pg_top
- Update to 3.6.2 beta3

* Mon Mar 10 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 3.6.1-1
- Update to 3.6.1

* Sun Jan 20 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 3.6.1-1.beta3
- Update to 3.6.1-beta3

* Mon Dec 13 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 3.6.1-1.beta2
- Initial RPM packaging for Fedora
