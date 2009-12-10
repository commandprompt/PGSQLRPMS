Summary:	PgpoolAdmin - web-based pgpool administration
Name:		pgpoolAdmin
Version:	2.3
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
URL:		http://pgpool.projects.postgresql.org
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	http://pgfoundry.org/frs/download.php/2494/%{name}-%{version}.tar.gz
Source1:	%{name}.conf

Requires:	php >= 4.3.9
Requires:	php-pgsql >= 4.3.9
Requires:	webserver
Requires:	pgpool-II

Buildarch:	noarch
BuildRequires:	httpd

%define		_pgpoolAdmindir	%{_datadir}/%{name}

Patch1:		%{name}-conf.patch

%description
The pgpool Administration Tool is management tool of pgpool-II. It is 
possible to monitor, start, stop pgpool and change settings of pgpool-II.

%prep
%setup -q 
%patch1 -p1
%build

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_pgpoolAdmindir}
install -d %{buildroot}%{_pgpoolAdmindir}/conf
install -d %{buildroot}%{_sysconfdir}/%{name}
install -m 644 *.php %{buildroot}%{_pgpoolAdmindir}
cp -a  doc/ images/ install/ lang/ libs/ templates/ screen.css %{buildroot}%{_pgpoolAdmindir}
install -m 755 conf/* %{buildroot}%{_sysconfdir}/%{name}/
ln -s ../../../..%{_sysconfdir}/%{name}/pgmgt.conf.php %{buildroot}%{_pgpoolAdmindir}/conf/pgmgt.conf.php

if [ -d %{_sysconfdir}/httpd/conf.d/ ]
then
	install -d %{buildroot}%{_sysconfdir}/httpd/conf.d/
	install -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
fi

%post
	/sbin/service httpd reload > /dev/null 2>&1
	chgrp apache /var/log/pgpool
	chgrp apache /var/run/pgpool
	chmod g+rwx /var/run/pgpool/
	chmod g+rwx /var/log/pgpool/
	
%postun 
	/sbin/service httpd reload > /dev/null 2>&1
	chmod g-rwx /var/run/pgpool
	chmod g-rwx /var/log/pgpool

%clean
rm -rf %{buildroot}

%files
%defattr(0644,nobody,nobody,0755)
%doc README README.euc_jp
%dir %{_pgpoolAdmindir}
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%attr(0644,apache,apache) %config(noreplace) %{_sysconfdir}/%{name}/*
%attr(0644,root,root) %{_pgpoolAdmindir}/*.php
%{_pgpoolAdmindir}/conf
%{_pgpoolAdmindir}/doc
%{_pgpoolAdmindir}/images
%{_pgpoolAdmindir}/install
%{_pgpoolAdmindir}/lang
%{_pgpoolAdmindir}/libs
%{_pgpoolAdmindir}/templates
%{_pgpoolAdmindir}/screen.css

%changelog
* Thu Dec 10 2009 Devrim Gunduz <devrim@commandprompt.com> 2.3-1
- Update to 2.3

* Mon Mar 23 2009 Devrim Gunduz <devrim@commandprompt.com> 2.2-1
- Update to 2.2
- Update spec and patches so that pgpoolAdmin works against pgpool 2.2

* Sun Jun 15 2008 Devrim Gunduz <devrim@commandprompt.com> 2.1-beta1-1
- Update to 2.1 beta1

* Tue Oct 16 2007 Devrim Gunduz <devrim@commandprompt.com> 1.0.0-9
- Fixed smarty error caused by wrong ownership
- Change php requires version for EL-4

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
