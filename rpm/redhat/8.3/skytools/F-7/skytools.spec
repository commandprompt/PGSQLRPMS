# Python major version.
%{expand: %%define pyver %(python -c 'import sys;print(sys.version[0:3])')}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary:	PostgreSQL database management tools from Skype
Name:		skytools
Version:	2.1.7
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://pgfoundry.org/frs/download.php/1813/%{name}-%{version}.tar.gz
URL:		http://pgfoundry.org/projects/skytools
BuildRequires:	postgresql-devel, python-devel
Requires:	python-psycopg2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch1:		%{name}-setup.patch

%description
Database management tools from Skype:WAL shipping, queueing, replication. 
The tools are named walmgr, PgQ and Londiste, respectively.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1

%build
%configure --with-asciidoc

make %{?_smp_mflags} 

%install
rm -rf %{buildroot}

python setup.py install --no-compile --root %{buildroot}

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
%{_bindir}/*.py
%{_bindir}/*.pyo
%{_bindir}/*.pyc
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
%{python_sitearch}/*.egg-info

%changelog
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


