# Python major version.
%{expand: %%define pyver %(python -c 'import sys;print(sys.version[0:3])')}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary:	Fast data loader for PostgreSQL
Name:		pgloader
Version:	2.3.2
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
URL:		http://pgfoundry.org/projects/pgloader/
Source0:	http://pgfoundry.org/frs/download.php/2294/%{name}-%{version}.tar.gz
Patch1:		pgloader-makefile.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	python
Requires:	python-psycopg2

%description
The PostgreSQL Loader project is a fast data loader for PostgreSQL, 
with the ability to generate files of rejected rows. It currently 
requires Python and Psycopg (version 1 or version 2, latter preferred).

%prep
%setup -q -n %{name}-%{version}
%patch1 -p0

%install
rm -rf %{buildroot}
#export LIBDIR=%{python_sitearch}/
#export EXDIR=%{_docdir}/%{name}-%{version}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_docdir}/%{name}
install -d %{buildroot}/%{python_sitearch}/%{name}/
install -d %{buildroot}/%{python_sitearch}/%{name}/reformat
install -d %{buildroot}/%{_mandir}/man1/
install -m 755 pgloader.py %{buildroot}%{_bindir}/pgloader
install -m 644 pgloader/*.py %{buildroot}/%{python_sitearch}/%{name}/
install -m 644 reformat/*.py %{buildroot}/%{python_sitearch}/%{name}/reformat/
%{__cp} -r  examples/* %{buildroot}%{_docdir}/%{name}
install -m 644 TODO.txt BUGS.txt %{buildroot}%{_docdir}/%{name}
%{__gzip} -q pgloader.1
install -m 644 pgloader.1.gz %{buildroot}/%{_mandir}/man1/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
#%doc BUGS.txt BUGS.txt TODO.txt
%{_bindir}/pgloader
%{_docdir}/%{name}/*
%dir %{python_sitearch}/%{name}/
%dir %{python_sitearch}/%{name}/reformat
%{python_sitearch}/%{name}/*.py
%{python_sitearch}/%{name}/*.pyo
%{python_sitearch}/%{name}/*.pyc
%{python_sitearch}/%{name}/reformat/*.py
%{python_sitearch}/%{name}/reformat/*.pyo
%{python_sitearch}/%{name}/reformat/*.pyc
%{_mandir}/man1/pgloader.1.gz

%changelog
* Tue Jul 28 2009 Devrim Gunduz <devrim@CommandPrompt.com> 2.3.2-1
- Update to 2.3.2

* Sun Jun 15 2008 Devrim Gunduz <devrim@CommandPrompt.com> 2.3.1-1
- Update to 2.3.1

* Wed Apr 9 2008 Devrim Gunduz <devrim@CommandPrompt.com> 2.3.0-1
- Update to 2.3.0
- Various spec file fixes

* Fri Feb 1 2008 Devrim Gunduz <devrim@CommandPrompt.com> 2.2.6-1
- Update to 2.2.6

* Sat Jan 19 2008 Devrim Gunduz <devrim@CommandPrompt.com> 2.2.5-1
- Update to 2.2.5

* Thu Jun 21 2007 Devrim Gunduz <devrim@CommandPrompt.com> 2.2.0-1
- Initial packaging
