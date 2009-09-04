# Python major version.
%{expand: %%define pyver %(python -c 'import sys;print(sys.version[0:3])')}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary:	PostgreSQL database management tools from Skype
Name:		skytools
Version:	2.1.10
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://pgfoundry.org/frs/download.php/2370/%{name}-%{version}.tar.gz
URL:		http://pgfoundry.org/projects/skytools
BuildRequires:	postgresql-devel, python-devel
Requires:	python-psycopg2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Database management tools from Skype:WAL shipping, queueing, replication. 
The tools are named walmgr, PgQ and Londiste, respectively.

%prep
%setup -q -n %{name}-%{version}

%build
%configure

make %{?_smp_mflags} 

%install
rm -rf %{buildroot}

make %{?_smp_mflags} DESTDIR=%{buildroot} python-install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig 
%postun -p /sbin/ldconfig 

%files
%defattr(644,root,root,755)
%dir %{python_sitearch}/%{name}
%{_docdir}/%{name}/conf/*.templ
%{_docdir}/%{name}/conf/*.ini
%{_datadir}/%{name}/*.sql
%{_datadir}/%{name}/upgrade/final/*.sql
%{_bindir}/*.py
%{python_sitearch}/londiste/*.py
%{python_sitearch}/londiste/*.pyc
%{python_sitearch}/pgq/*.py
%{python_sitearch}/pgq/*.pyc
%{python_sitearch}/skytools/*.py
%{python_sitearch}/skytools/_cquoting.so
%{python_sitearch}/skytools/*.pyc
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

%changelog
* Wed Sep 2 2009 Devrim GUNDUZ <devrim@commandprompt.com> 2.1.10-1
- Update to 2.1.10

* Fri Mar 13 2009 Devrim GUNDUZ <devrim@commandprompt.com> 2.1.9-1
- Update to 2.1.9
- Remove pg84 patch, it is now in upstream.

* Thu Mar 12 2009 Devrim GUNDUZ <devrim@commandprompt.com> 2.1.8-1
- Update to 2.1.8
- Remove patch 1, it is now in upstream.
- Add a new patch to compile skytools against PostgreSQL 8.4.

* Sun Aug 24 2008 - David Fetter <david@fetter.org> 2.1.7-2
- Added man pages.
- Fix man builds (Devrim)
- copy paste is evil -- remove egg-info thing.

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


