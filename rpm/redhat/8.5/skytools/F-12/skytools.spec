# Python major version.
%{expand: %%define pyver %(python -c 'import sys;print(sys.version[0:3])')}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary:	PostgreSQL database management tools from Skype
Name:		skytools
Version:	2.1.10
Release:	4%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://pgfoundry.org/frs/download.php/2370/%{name}-%{version}.tar.gz
URL:		http://pgfoundry.org/projects/skytools
BuildRequires:	postgresql-devel, python-devel
Requires:	python-psycopg2, postgresql
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Database management tools from Skype:WAL shipping, queueing, replication. 
The tools are named walmgr, PgQ and Londiste, respectively.

%package modules
Summary:	PostgreSQL modules of Skytools
Group:		Applications/Databases
Requires:	%{name}-%{version}

%description modules
This package has PostgreSQL modules of skytools.

%prep
%setup -q -n %{name}-%{version}

%build
%configure

make %{?_smp_mflags} 

%install
rm -rf %{buildroot}

make %{?_smp_mflags} DESTDIR=%{buildroot} python-install modules-install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig 
%postun -p /sbin/ldconfig 

%files
%defattr(644,root,root,755)
%dir %{python_sitearch}/%{name}
%{_docdir}/%{name}/conf/*.templ
%{_docdir}/%{name}/conf/*.ini
%{_docdir}/pgsql/contrib/*
%{_datadir}/%{name}/*.sql
%{_datadir}/%{name}/upgrade/final/*.sql
%{_datadir}/pgsql/contrib/londiste.sql
%{_datadir}/pgsql/contrib/londiste.upgrade.sql
%{_datadir}/pgsql/contrib/pgq.sql
%{_datadir}/pgsql/contrib/pgq.upgrade.sql
%{_datadir}/pgsql/contrib/pgq_ext.sql
%{_datadir}/pgsql/contrib/uninstall_pgq.sql
%attr(755,root,root) %{_bindir}/*.py
%{_libdir}/pgsql/*.so
%{python_sitearch}/londiste/*.py
%{python_sitearch}/londiste/*.pyc
%{python_sitearch}/pgq/*.py
%{python_sitearch}/pgq/*.pyc
%{python_sitearch}/skytools/*.py
%{python_sitearch}/skytools/_cquoting.so
%{python_sitearch}/skytools/*.pyc
%ghost %{python_sitearch}/londiste/*.pyo
%ghost %{python_sitearch}/pgq/*.pyo
%ghost %{python_sitearch}/skytools/*.pyo
%{_mandir}/man1/bulk_loader.*
%{_mandir}/man1/cube_dispatcher.*
%{_mandir}/man1/londiste.*
%{_mandir}/man1/pgqadm.*
%{_mandir}/man1/queue_mover.*
%{_mandir}/man1/queue_splitter.*
%{_mandir}/man1/scriptmgr.*
%{_mandir}/man1/skytools_upgrade.*
%{_mandir}/man1/table_dispatcher.*
%{_mandir}/man1/walmgr.*
%{_mandir}/man5/londiste.*
%{python_sitearch}/%{name}-%{version}-py%{pyver}.egg-info

%files modules
%{_libdir}/pgsql/*.so
%{_datadir}/pgsql/contrib/pgq_lowlevel.sql
%{_datadir}/pgsql/contrib/pgq_triggers.sql
%{_datadir}/pgsql/contrib/logtriga.sql

%changelog
* Tue Dec 8 2009 Devrim GUNDUZ <devrim@gunduz.org> - 2.1.10-4
- Split PostgreSQL modules to a separate package, per idea from
  Greg Smith.

* Thu Dec 03 2009 Greg Smith <greg@2ndQuadrant.com> - 2.1.10-3
- Build and package the PostgreSQL modules

* Wed Nov 04 2009 Devrim GUNDUZ <devrim@gunduz.org> - 2.1.10-2
- Set executable flag on .py files, per report from Dimitri Fontaine

* Wed Sep 2 2009 Devrim GUNDUZ <devrim@commandprompt.com> 2.1.10-1
- Update to 2.1.10

* Fri Mar 13 2009 Devrim GUNDUZ <devrim@commandprompt.com> 2.1.9-1
- Update to 2.1.9
- Remove patch 1, it is now in upstream.

* Sun Aug 24 2008 - David Fetter <david@fetter.org> 2.1.7-2
- Added man pages.
- Fix man builds (Devrim)

* Mon Jun 13 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 2.1.7-1
- Need to require python-psycopg v2, not v1.
- Update to 2.1.7

* Mon Jun 2 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 2.1.6-2
- Fix build for Fedora 9

* Sun Apr 6 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 2.1.6-1
- Update to 2.1.6
- Initial RPM packaging for yum.pgsqlrpms.org

* Mon Nov 19 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 2.1.5-1
- Update to 2.1.5

* Wed Nov 14 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 2.1.4-1
- Initial RPM packaging for Fedora


