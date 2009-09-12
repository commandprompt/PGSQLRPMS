%{!?javabuild:%define	javabuild 0}
%{!?utils:%define	utils 1}
%{!?gcj_support:%define	gcj_support 1}

Summary:	Geographic Information Systems Extensions to PostgreSQL
Name:		postgis
Version:	1.3.6
Release:	2%{?dist}
License:	GPLv2+
Group:		Applications/Databases
Source0:	http://postgis.refractions.net/download/%{name}-%{version}.tar.gz
Source2:	http://www.postgis.org/download/%{name}-%{version}.pdf
Source4:	filter-requires-perl-Pg.sh
URL:		http://postgis.refractions.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	postgresql-devel, proj-devel, geos-devel, byacc, proj-devel, flex, sinjdoc, java, java-devel, ant

Requires:	postgresql, geos, proj

%description
PostGIS adds support for geographic objects to the PostgreSQL object-relational
database. In effect, PostGIS "spatially enables" the PostgreSQL server,
allowing it to be used as a backend spatial database for geographic information
systems (GIS), much like ESRI's SDE or Oracle's Spatial extension. PostGIS 
follows the OpenGIS "Simple Features Specification for SQL" and has been 
certified as compliant with the "Types and Functions" profile.

%package docs
Summary:	Extra documentation for PostGIS
Group:		Applications/Databases
%description docs
The postgis-docs package includes PDF documentation of PostGIS.

%if %javabuild
%package jdbc
Summary:	The JDBC driver for PostGIS
Group:		Applications/Databases
License:	LGPL
Requires:	%{name} = %{version}-%{release}, postgresql-jdbc
BuildRequires:	ant >= 0:1.6.2, junit >= 0:3.7, postgresql-jdbc

%if %{gcj_support}
BuildRequires:		gcc-java
Requires(post):		%{_bindir}/rebuild-gcj-db
Requires(postun):	%{_bindir}/rebuild-gcj-db
%endif

%description jdbc
The postgis-jdbc package provides the essential jdbc driver for PostGIS.
%endif

%if %utils
%package utils
Summary:	The utils for PostGIS
Group:		Applications/Databases
Requires:	%{name} = %{version}-%{release}, perl-DBD-Pg

%description utils
The postgis-utils package provides the utilities for PostGIS.
%endif

%define __perl_requires %{SOURCE4}

%prep
%setup -q
# Copy .pdf file to top directory before installing.
cp -p %{SOURCE2} .

%build
%configure 
make %{?_smp_mflags} LPATH=`pg_config --pkglibdir` shlib="%{name}.so"

%if %javabuild
export BUILDXML_DIR=%{_builddir}/%{name}-%{version}/java/jdbc
JDBC_VERSION_RPM=`rpm -ql postgresql-jdbc| grep 'jdbc2.jar$'|awk -F '/' '{print $5}'`
sed 's/postgresql.jar/'${JDBC_VERSION_RPM}'/g' $BUILDXML_DIR/build.xml > $BUILDXML_DIR/build.xml.new
mv -f $BUILDXML_DIR/build.xml.new $BUILDXML_DIR/build.xml
pushd java/jdbc
ant
popd
%endif

%if %utils
 make -C utils
%endif

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
install -d %{buildroot}%{_libdir}/pgsql/
install lwgeom/liblwgeom.so* %{buildroot}%{_libdir}/pgsql/
install lwgeom/postgis.so* %{buildroot}%{_libdir}/pgsql/
install -d  %{buildroot}%{_datadir}/pgsql/contrib/
install -m 644 *.sql %{buildroot}%{_datadir}/pgsql/contrib/
rm -f  %{buildroot}%{_libdir}/liblwgeom.so*
rm -f  %{buildroot}%{_datadir}/*.sql

if [ "%{_libdir}" = "/usr/lib64" ] ; then
	mv %{buildroot}%{_datadir}/pgsql/contrib/lwpostgis.sql %{buildroot}%{_datadir}/pgsql/contrib/lwpostgis-64.sql
	mv %{buildroot}%{_datadir}/pgsql/contrib/lwpostgis_upgrade.sql %{buildroot}%{_datadir}/pgsql/contrib/lwpostgis_upgrade-64.sql
fi

%if %javabuild
install -d %{buildroot}%{_javadir}
install -m 755 java/jdbc/%{name}_%{version}.jar %{buildroot}%{_javadir}
%if %{gcj_support}
aot-compile-rpm
%endif
strip %{buildroot}/%{_libdir}/gcj/%{name}/*.jar.so
%endif

%if %utils
install -d %{buildroot}%{_datadir}/%{name}
install -m 644 utils/*.pl %{buildroot}%{_datadir}/%{name}
%endif

%clean
rm -rf %{buildroot}

%if %javabuild
%if %gcj_support
%post -p %{_bindir}/rebuild-gcj-db
%postun -p %{_bindir}/rebuild-gcj-db
%endif
%endif

%files
%defattr(-,root,root)
%doc COPYING CREDITS NEWS TODO README.%{name} doc/html loader/README.* doc/%{name}.xml doc/ZMSgeoms.txt
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/pgsql/postgis.so*
%attr(755,root,root) %{_libdir}/pgsql/liblwgeom.so*
%{_datadir}/pgsql/contrib/*.sql

%if %javabuild
%files jdbc
%defattr(-,root,root)
%doc java/jdbc/COPYING_LGPL java/jdbc/README
%attr(755,root,root) %{_javadir}/%{name}_%{version}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%{_libdir}/gcj/%{name}/*.jar.so
%{_libdir}/gcj/%{name}/*.jar.db
%endif
%endif

%if %utils
%files utils
%defattr(-,root,root)
%doc utils/README
%attr(755,root,root) %{_datadir}/%{name}/test_estimation.pl
%attr(755,root,root) %{_datadir}/%{name}/profile_intersects.pl
%attr(755,root,root) %{_datadir}/%{name}/test_joinestimation.pl
%attr(644,root,root) %{_datadir}/%{name}/create_undef.pl
%attr(644,root,root) %{_datadir}/%{name}/%{name}_proc_upgrade.pl
%attr(644,root,root) %{_datadir}/%{name}/%{name}_restore.pl
%endif

%files docs
%defattr(-,root,root)
%doc postgis*.pdf


%changelog
* Tue Jun 2 2009 Devrim GUNDUZ <devrim@commandprompt.com> - 1.3.6-2
- Add a new subpackage: -docs, and add postgis pdf file to it.
- Update license.
- Fix some very minor rpmlint problems.

* Mon May 4 2009 Devrim GUNDUZ <devrim@commandprompt.com> - 1.3.6-1
- Update to 1.3.6

* Tue Dec 16 2008 Devrim GUNDUZ <devrim@commandprompt.com> - 1.3.5-1
- Update to 1.3.5

* Sat Nov 29 2008 Devrim GUNDUZ <devrim@commandprompt.com> - 1.3.4-1
- Update to 1.3.4

* Mon Aug 11 2008 Devrim GUNDUZ <devrim@commandprompt.com> - 1.3.3-2
- Fix #451387. Patch from Toshio.

* Sun Apr 13 2008 Devrim GUNDUZ <devrim@commandprompt.com> - 1.3.3-1
- Update to 1.3.3

* Sat Jan 5 2008 Devrim GUNDUZ <devrim@commandprompt.com> - 1.3.2-2
- Various fixes from Mark Cave-Ayland
- Removed patch2: template_gis is no longer built by default.
- Removed patch0: Building the JDBC driver using make is now deprecated
- Build JDBC driver using ant, rather than make.

* Thu Dec 6 2007 Devrim GUNDUZ <devrim@commandprompt.com> - 1.3.2-1
- Update to 1.3.2
- Updated patch2

* Wed Nov 21 2007 Devrim GUNDUZ <devrim@commandprompt.com> - 1.3.1-2
- Move postgresql-jdbc dependency to the correct place, per Rob Nagler.

* Tue Oct 16 2007 Devrim GUNDUZ <devrim@commandprompt.com> - 1.3.1-1
- Update to 1.3.1
- Updated patch2

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.2.1-3
- Rebuild for selinux ppc32 issue.

* Mon Jul 2 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 1.2.1-2
- Fix build problems (removed template_gis, per discussion with upstream).

* Mon Feb 19 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 1.2.1-1
- Update to 1.2.1
- Removed configure patch (it is in the upstream now)
- Added postgresql-jdbc as as dependency to -jdbc package, per Guillaume
- move strip to correct place, per Guillaume
- Fix long-standing post/postun problem, per Guillaume

* Wed Jan 3 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 1.2.0-4
- Added postgis.so among installed files, per Jon Burgess.
- Fix jdbc jar dedection problem

* Wed Dec 27 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 1.2.0-3
- Fix Requires for subpackages per bugzilla review #220743

* Mon Dec 26 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 1.2.0-2
- More spec file fixes per bugzilla review #220743

* Mon Dec 25 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 1.2.0-1
- Initial submission for Fedora Core Extras
- Spec file changes and fixes per FC Extras packaging guidelines

* Fri Jun 23 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 1.1.2-2
- Update to 1.1.2

* Tue Dec 22 2005 - Devrim GUNDUZ <devrim@commandprompt.com> 1.1.0-2
- Final fixes for 1.1.0

* Tue Dec 06 2005 - Devrim GUNDUZ <devrim@gunduz.org>
- Update to 1.1.0

* Mon Oct 03 2005 - Devrim GUNDUZ <devrim@gunduz.org>
- Make PostGIS build against pgxs so that we don't need PostgreSQL sources.
- Fixed all build errors except jdbc (so, defaulted to 0)
- Added new files under %%utils
- Removed postgis-jdbc2-makefile.patch (applied to -head)

* Tue Sep 27 2005 - Devrim GUNDUZ <devrim@gunduz.org>
- Update to 1.0.4

* Sun Apr 20 2005 - Devrim GUNDUZ <devrim@gunduz.org>
- 1.0.0 Gold

* Sun Apr 17 2005 - Devrim GUNDUZ <devrim@gunduz.org>
- Modified the spec file so that we can build JDBC2 RPMs...
- Added -utils RPM to package list.

* Fri Apr 15 2005 - Devrim GUNDUZ <devrim@gunduz.org>
- Added preun and postun scripts.

* Sat Apr 09 2005 - Devrim GUNDUZ <devrim@gunduz.org>
- Initial RPM build
- Fixed libdir so that PostgreSQL installations will not complain about it.
- Enabled --with-geos and modified the old spec.
