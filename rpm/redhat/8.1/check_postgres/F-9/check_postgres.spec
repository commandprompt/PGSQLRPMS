Summary:	PostgreSQL monitoring script
Name:		check_postgres
Version:	2.5.0
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://bucardo.org/%{name}/%{name}.pl
Source2:	http://bucardo.org/%{name}/%{name}.pl.html
URL:		http://bucardo.org/check_postgres/
Requires:	postgresql-server >= 7.4
Buildarch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
check_postgres.pl is a script for checking the state of one or more 
Postgres databases and reporting back in a Nagios-friendly manner. It is 
also used for MRTG.

%prep

%build

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}/
install -d %{buildroot}%{_docdir}/%{name}-%{version}
install -m 755 %{SOURCE0} %{buildroot}%{_bindir}/
install -m 644 %{SOURCE2} %{buildroot}%{_docdir}/%{name}-%{version}/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}-%{version}/%{name}.pl.html
%{_bindir}/%{name}.pl

%changelog
* Sun Dec 7 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 2.5.0-1
- Update to 2.5.0

* Tue Dec 2 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 2.4.3-1
- Update to 2.4.3

* Tue Oct 7 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 2.3.0-1
- Update to 2.3.0
- Make package noarch

* Mon Sep 29 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 2.2.1-1
- Update to 2.2.1

* Tue Sep 23 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 2.1.4-1
- Initial RPM packaging for yum.pgsqlrpms.org
