Summary:	PostgreSQL Config Tuner
Name:		pgtune
Version:	0.9.2
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
URL:		http://pgfoundry.org/projects/pgtune
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	http://pgfoundry.org/frs/download.php/2448/%{name}-%{version}.tar.gz
Patch0:		pgtune-settingsdir.patch
Requires:	postgresql-server
Buildarch:	noarch

%description
pgtune takes the wimpy default postgresql.conf and expands the database server 
to be as powerful as the hardware it's being deployed on.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p0

%build

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_datadir}/%{name}

install -m 755 pgtune %{buildroot}%{_bindir}

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc TODO COPYRIGHT
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%attr(755,root,root) %{_bindir}/pgtune

%changelog
* Wed Oct 28 2009 Devrim Gunduz <devrim@commandprompt.com> 0.9.2-1
- Update to 0.9.2

* Wed Oct 28 2009 Devrim Gunduz <devrim@commandprompt.com> 0.9.1-1
- Initial packaging for PostgreSQL RPM Repository
