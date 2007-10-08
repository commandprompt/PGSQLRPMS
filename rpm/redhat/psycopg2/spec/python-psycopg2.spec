# Python major version.
%{expand: %%define pyver %(python -c 'import sys;print(sys.version[0:3])')}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define ZPsycopgDAdir %{_localstatedir}/lib/zope/Products/ZPsycopgDA


Summary:	A PostgreSQL database adapter for Python
Name:		python-psycopg2
Version:	2.0.3
Release:	3%{?dist}
Source0:	http://initd.org/pub/software/psycopg/psycopg2-%{version}.tar.gz
License:	GPL (with Exceptions)
Group:		Applications/Databases
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Url:		http://www.initd.org/software/initd/psycopg
BuildRequires:	python-devel postgresql-devel
Requires:	postgresql-libs

%description
psycopg is a PostgreSQL database adapter for the Python programming
language (just like pygresql and popy.) It was written from scratch 
with the aim of being very small and fast, and stable as a rock. The 
main advantages of psycopg are that it supports the full Python
DBAPI-2.0 and being thread safe at level 2.

%package doc
Summary:	Documentation for psycopg python PostgreSQL database adapter
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description doc
Documentation and example files for the psycopg python PostgreSQL
database adapter.

%package zope
Summary:	Zope Database Adapter ZPsycopgDA
Group:		Applications/Databases
Requires:	%{name} = %{version}-%{release} zope

%description zope
Zope Database Adapter for PostgreSQL, called ZPsycopgDA

%prep
%setup -q -n psycopg2-%{version}

%build
python setup.py build
# Fix for wrong-file-end-of-line-encoding problem; upstream also must fix this.
for i in `find doc -iname "*.html"`; do sed -i 's/\r//' $i; done
for i in `find doc -iname "*.css"`; do sed -i 's/\r//' $i; done

%install
rm -Rf %{buildroot}
mkdir -p %{buildroot}%{python_sitearch}/psycopg2
python setup.py install --no-compile --root %{buildroot}

install -d %{buildroot}%{ZPsycopgDAdir}
cp -pr ZPsycopgDA/* %{buildroot}%{ZPsycopgDAdir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog INSTALL LICENSE MANIFEST README
%dir %{python_sitearch}/psycopg2
%{python_sitearch}/psycopg2/*.py
%{python_sitearch}/psycopg2/*.pyc
%{python_sitearch}/psycopg2/*.so
%ghost %{python_sitearch}/psycopg2/*.pyo

%files doc
%defattr(-,root,root)
%doc doc examples/

%files zope
%defattr(-,root,root)
%dir %{ZPsycopgDAdir}
%{ZPsycopgDAdir}/*.py
%ghost %{ZPsycopgDAdir}/*.pyo
%{ZPsycopgDAdir}/*.pyc
%{ZPsycopgDAdir}/dtml/*
%{ZPsycopgDAdir}/icons/*

%changelog
* Sun Aug 6 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0.3-3
- Fixed zope package dependencies and macro definition, per bugzilla review (#199784)
- Fixed zope package directory ownership, per bugzilla review (#199784)
- Fixed cp usage for zope subpackage, per bugzilla review (#199784)

* Mon Jul 31 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0.3-2
- Fixed 64 bit builds
- Fixed license
- Added Zope subpackage
- Fixed typo in doc description
- Added macro for zope subpackage dir

* Mon Jul 31 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0.3-1
- Update to 2.0.3
- Fixed spec file, per bugzilla review (#199784)

* Sat Jul 22 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0.2-3
- Removed python dependency, per bugzilla review. (#199784)
- Changed doc package group, per bugzilla review. (#199784)
- Replaced dos2unix with sed, per guidelines and bugzilla review (#199784)
- Fix changelog dates

* Sat Jul 21 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0.2-2
- Added dos2unix to buildrequires
- removed python related part from package name

* Fri Jul 20 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0.2-1
- Fix rpmlint errors, including dos2unix solution
- Re-engineered spec file

* Fri Jan 23 2006 - Devrim GUNDUZ <devrim@commandprompt.com>
- First 2.0.X build

* Fri Jan 23 2006 - Devrim GUNDUZ <devrim@commandprompt.com>
- Update to 1.2.21

* Tue Dec 06 2005 - Devrim GUNDUZ <devrim@commandprompt.com>
- Initial release for 1.1.20
