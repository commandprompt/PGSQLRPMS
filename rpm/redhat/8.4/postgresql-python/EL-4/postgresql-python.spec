# Conventions for PostgreSQL Global Development Group RPM releases:

# Official PostgreSQL Development Group RPMS have a PGDG after the release number.
# Integer releases are stable -- 0.1.x releases are Pre-releases, and x.y are
# test releases.

# Pre-releases are those that are built from CVS snapshots or pre-release
# tarballs from postgresql.org.  Official beta releases are not
# considered pre-releases, nor are release candidates, as their beta or
# release candidate status is reflected in the version of the tarball. Pre-
# releases' versions do not change -- the pre-release tarball of 7.0.3, for
# example, has the same tarball version as the final official release of 7.0.3:

# Major Contributors:
# ---------------
# Devrim Gunduz

# This spec file and ancilliary files are licensed in accordance with
# The PostgreSQL license.
# In this file you can find the default build package list macros.  These can be overridden by defining
# on the rpm command line

# Python major version.
%{expand: %%define pyver %(python -c 'import sys;print(sys.version[0:3])')}
%{expand: %%define pynextver %(python -c 'import sys;print(float(sys.version[0:3])+0.1)')}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary:	Development module for Python code to access a PostgreSQL DB
Name:		postgresql-python
Version:	3.8.1
Release:	7PGDG%{?dist}.pg83
Epoch:		0
License:	BSD
Group:		Applications/Databases
URL:		ftp://www.pygresql.org
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	ftp://ftp.pygresql.org/pub/distrib/PyGreSQL-%{version}.tgz

BuildRequires:	python-devel, postgresql-devel >= 8.3
Requires:	python mx  postgresql-libs >= 8.3

%description
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-python package includes a module for
developers to use when writing Python code for accessing a PostgreSQL
database.

%prep
%setup -c -q

tar xzf %{SOURCE0}
PYGRESQLDIR=`basename %{SOURCE0} .tgz`
mv $PYGRESQLDIR PyGreSQL
# Some versions of PyGreSQL.tgz contain wrong file permissions
chmod 644 PyGreSQL/docs/*.txt
chmod 755 PyGreSQL/tutorial
chmod 644 PyGreSQL/tutorial/*.py
chmod 755 PyGreSQL/tutorial/advanced.py PyGreSQL/tutorial/basics.py

%build
PYTHON=/usr/bin/python
python_version=`${PYTHON} -c "import sys; print sys.version[:3]"`
python_prefix=`${PYTHON} -c "import sys; print sys.prefix"`
python_includespec="-I${python_prefix}/include/python${python_version}"

pushd PyGreSQL

gcc $CFLAGS -fpic -shared -o _pgmodule.so ${python_includespec} -I%{kerbdir}/include -I../src/interfaces/libpq -I../src/include -L../src/interfaces/libpq -lpq -I /usr/include/pgsql/server pgmodule.c

popd

%install
rm -rf %{buildroot}
pushd PyGreSQL
install -m 0755 -d %{buildroot}%{_libdir}/python%{pyver}/site-packages
install -m 0755 _pgmodule.so %{buildroot}%{_libdir}/python%{pyver}/site-packages
install -m 0755 pg.py %{buildroot}%{_libdir}/python%{pyver}/site-packages
install -m 0755 pgdb.py %{buildroot}%{_libdir}/python%{pyver}/site-packages
popd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc PyGreSQL/tutorial PyGreSQL/docs/*.txt
%{python_sitearch}/_pgmodule.so
%{python_sitearch}/pg.py
%{python_sitearch}/pgdb.py
%{python_sitearch}/*.pyc
%ghost %{python_sitearch}/*.pyo

%changelog
* Fri Jan 4 2008 Devrim Gunduz <devrim@commandprompt.com> 0:3.8.1-7PGDG
- Add postgresql-libs as Requires
- Use a more proper Requires and Release info

* Tue Jan 1 2008 Devrim Gunduz <devrim@commandprompt.com> 0:3.8.1-6PGDG
- Added postgresql-devel as buildrequires
- Changed buildroot macro
- Fix dist macro

* Mon Sep 3 2007 Devrim Gunduz <devrim@commandprompt.com> 0:3.8.1-5PGDG
- Add {?dist} to release tag.

* Sun Dec 3 2006 Devrim Gunduz <devrim@commandprompt.com> 0:3.8.1-4PGDG
- Rebuilt

* Wed Aug 16 2006 Devrim Gunduz <devrim@commandprompt.com> 0:3.8.1-3PGDG
- Rebuilt for PostgreSQL 8.2 RPM Set

* Mon Jul 17 2006 Devrim Gunduz <devrim@commandprompt.com> 0:3.8.1-2PGDG
- Rebuilt for PostgreSQL 8.1

* Mon Jul 10 2006 Devrim Gunduz <devrim@commandprompt.com> 0:3.8.1-1PGDG
- Initial build for PGDG RPM Set
