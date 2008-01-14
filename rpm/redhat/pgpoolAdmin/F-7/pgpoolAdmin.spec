Summary:	PgpoolAdmin - web-based pgpool administration
Name:		pgpoolAdmin
Version:	1.0.0
Release:	10%{?dist}
License:	BSD
Group:		Applications/Databases
URL:		http://pgpool.projects.postgresql.org
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	http://pgfoundry.org/frs/download.php/980/%{name}-%{version}.tar.gz
Source1:	%{name}.conf

Requires:	php >= 4.3.9
Requires:	php-pgsql >= 4.3.9
Requires:	webserver
Requires:	postgresql-pgpool-II

Buildarch:	noarch
BuildRequires:	httpd

%define		_pgpoolAdmindir	%{_datadir}/%{name}

Patch1:		%{name}-conf.patch

%description
The pgpool Administration Tool is management tool of pgpool-II. It is 
possible to monitor, start, stop pgpool and change settings of pgpool-II.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1
%build

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_pgpoolAdmindir}
install -d %{buildroot}%{_pgpoolAdmindir}/conf
install -d %{buildroot}%{_sysconfdir}/%{name}
install -m 644 *.php %{buildroot}%{_pgpoolAdmindir}
cp -a  doc/ images/ install/ lang/ libs/ templates/ templates_c/ screen.css %{buildroot}%{_pgpoolAdmindir}
install -m 755 conf/* %{buildroot}%{_sysconfdir}/%{name}/
ln -s ../../../..%{_sysconfdir}/%{name}/pgmgt.conf.php %{buildroot}%{_pgpoolAdmindir}/conf/pgmgt.conf.php

if [ -d %{_sysconfdir}/httpd/conf.d/ ]
then
	install -d %{buildroot}%{_sysconfdir}/httpd/conf.d/
	install -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
fi

%post
	/sbin/service httpd reload > /dev/null 2>&1
%postun 
	/sbin/service httpd reload > /dev/null 2>&1

%clean
rm -rf %{buildroot}

%files
%defattr(0644,nobody,nobody,0755)
%doc README README.euc_jp
%dir %{_pgpoolAdmindir}
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%attr(644,apache,apache,0644) %config(noreplace) %{_sysconfdir}/%{name}/*
%attr(644,root,root) %{_pgpoolAdmindir}/*.php
%{_pgpoolAdmindir}/conf
%{_pgpoolAdmindir}/doc
%{_pgpoolAdmindir}/images
%{_pgpoolAdmindir}/install
%{_pgpoolAdmindir}/lang
%{_pgpoolAdmindir}/libs
%{_pgpoolAdmindir}/templates
%attr(755,apache,apache) %{_pgpoolAdmindir}/templates_c
%{_pgpoolAdmindir}/screen.css

%changelog
* Sat Jan 12 2008 Devrim Gunduz <devrim@commandprompt.com> 1.0.0-10
- Require PHP 4.3.9 (Fix for RHEL/CentOS 4)

* Tue Oct 16 2007 Devrim Gunduz <devrim@commandprompt.com> 1.0.0-9
- Fixed smarty error caused by wrong ownership

* Thu Aug 16 2007 Devrim Gunduz <devrim@commandprompt.com> 1.0.0-8
- Fix ownership problem of pgmgmt.conf

* Thu Aug 16 2007 Devrim Gunduz <devrim@commandprompt.com> 1.0.0-7
- Fix httpd configuration file -- it was using wrong directory.

* Sat Jun 2 2007 Devrim Gunduz <devrim@commandprompt.com> 1.0.0-6
- Fixes for bugzilla review #229323

* Tue Feb 20 2007 Devrim Gunduz <devrim@commandprompt.com> 1.0.0-5
- Fixes for packaging guidelines of web apps.
- Fix ownership problems

* Mon Oct 02 2006 Devrim Gunduz <devrim@commandprompt.com> 1.0.0-4
- chgrp and chmod pgpool-II conf files so that apache can write it. 
- Change file ownership from apache to nobody.

* Tue Sep 26 2006 Devrim Gunduz <devrim@commandprompt.com> 1.0.0-3
- Update patch1

* Tue Sep 26 2006 Devrim Gunduz <devrim@commandprompt.com> 1.0.0-2
- Fix file ownership
- Update patch1

* Tue Sep 26 2006 Devrim Gunduz <devrim@commandprompt.com> 1.0.0-1
- Initial build 
