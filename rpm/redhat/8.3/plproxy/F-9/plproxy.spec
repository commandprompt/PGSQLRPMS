Name:		plproxy
Version:	2.0.7
Release:	1%{?dist}
Summary:	PL/Proxy is database partitioning system implemented as PL language.
Group:		Applications/Databases
License:	BSD
URL:		http://pgfoundry.org/projects/plproxy/
Source0:	http://pgfoundry.org/frs/download.php/1919/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	postgresql-devel >= 8.1 flex >= 2.5.4
Requires:	postgresql >= 8.1

%description
PL/Proxy is database partitioning system implemented as PL language.

%prep
%setup -q -n %{name}-%{version}

%build
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
#make %{?_smp_mflags} install
install -d %{buildroot}%{_datadir}/%{name}-%{version}/
install -d %{buildroot}%{_libdir}/pgsql
install -m 644 plproxy.sql %{buildroot}%{_datadir}/%{name}-%{version}/
%{__cp} -rp sql/ %{buildroot}%{_datadir}/%{name}-%{version}/
%{__cp} -rp config/ %{buildroot}%{_datadir}/%{name}-%{version}/
ln -s %{name}.so.0.0 %{buildroot}%{_libdir}/pgsql/%{name}.so.0
ln -s %{name}.so.0.0 %{buildroot}%{_libdir}/pgsql/%{name}.so
%{__rm} -f %{buildroot}/%{_datadir}/pgsql/contrib/%{name}.sql

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README NEWS AUTHORS COPYRIGHT 
%{_datadir}/%{name}-%{version}/*
%{_libdir}/pgsql/%{name}.so*

%changelog
* Tue Oct 7 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0.7-1
- Update to 2.0.7

* Sat Sep 20 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0.6-1
- Update to 2.0.6

* Sun Jun 15 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0.5-1
- Update to 2.0.5
- Remove scanner.c and scanner.h, they are no longer needed.

* Tue Aug 28 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0.2-2
- Add pre-generated scanner.c and scanner.h as sources. Only very
recent versions of flex can compile plproxy.

* Tue Aug 28 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0.2-1
- Initial build 
