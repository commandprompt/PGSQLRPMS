Summary:	PostgreSQL monitoring script
Name:		check_postgres
Version:	2.13.0
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://bucardo.org/downloads/%{name}-%{version}.tar.gz
URL:		http://bucardo.org/check_postgres/
Requires:	postgresql-server >= 7.4
Buildarch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
check_postgres.pl is a script for checking the state of one or more 
Postgres databases and reporting back in a Nagios-friendly manner. It is 
also used for MRTG.

%prep
%setup -q

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}/
install -d %{buildroot}%{_docdir}/%{name}-%{version}
install -d %{buildroot}%{_mandir}/man3/
install -m 755 %{name}.pl %{buildroot}%{_bindir}/
install -m 644 %{name}.pl.html README TODO %{buildroot}%{_docdir}/%{name}-%{version}/
install -m 644 blib/man3/check_postgres.3pm %{buildroot}%{_mandir}/man3/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{name}.pl.html README TODO
%{_mandir}/man3/%{name}.*
%{_bindir}/%{name}.pl

%changelog
* Mon Feb 1 2010 - Devrim GUNDUZ <devrim@commandprompt.com> 2.13.0-1
- Update to 2.13.0
- Refactor spec file:
  * Use tarball, instead of .pl file directly.
  * Add man page

* Wed Sep 2 2009 - Devrim GUNDUZ <devrim@commandprompt.com> 2.12.0-1
- Update to 2.12.0

* Wed Sep 2 2009 - Devrim GUNDUZ <devrim@commandprompt.com> 2.11.1-1
- Update to 2.11.1

* Tue Aug 4 2009 - Devrim GUNDUZ <devrim@commandprompt.com> 2.9.10-1
- Update to 2.9.10

* Tue Jul 28 2009 - Devrim GUNDUZ <devrim@commandprompt.com> 2.9.2-1
- Update to 2.9.2

* Sat Jul 4 2009 - Devrim GUNDUZ <devrim@commandprompt.com> 2.9.1-1
- Update to 2.9.1

* Mon May 18 2009 - Devrim GUNDUZ <devrim@commandprompt.com> 2.8.1-1
- Update to 2.8.1

* Thu May 7 2009 - Devrim GUNDUZ <devrim@commandprompt.com> 2.8.0-1
- Update to 2.8.0

* Tue Feb 17 2009 - Devrim GUNDUZ <devrim@commandprompt.com> 2.7.3-1
- Update to 2.7.3

* Sun Feb 1 2009 - Devrim GUNDUZ <devrim@commandprompt.com> 2.6.0-1
- Update to 2.6.0

* Fri Dec 19 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 2.5.3-1
- Update to 2.5.3

* Wed Dec 17 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 2.5.2-1
- Update to 2.5.2

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
