Summary:	Routing functionality for PostGIS
Name:		pgrouting
Version:	1.03
Release:	5
License:	GPLv2
Group:		Applications/Databases
Source0:	http://files.postlbs.org/%{name}/source/pgRouting-%{version}.tgz
# The following patch is used for building pgrouting against PostgreSQL 8.4+ :
Patch0:		pgrouting-pg84.patch
URL:		http://pgrouting.postlbs.org/
BuildRequires:	gcc-c++, cmake
BuildRequires:	postgresql-devel, proj-devel, geos-devel
BuildRequires:	boost-devel >= 1.33
Requires:	postgis >= 1.3
Requires:	postgresql >= 8.1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Routing functionality for PostgreSQL/PostGIS system.

%prep

%setup -q -n %{name}
%patch0 -p0

%build
install -d build
cd build
%cmake .. \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DWITH_TSP=OFF \
	-DWITH_DD=OFF \
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64
%endif

%{__make}

%install
rm -rf %{buildroot}

%{__make} -C build install \
	DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.routing
%attr(755,root,root) %{_libdir}/pgsql/*.so
%{_datadir}/postlbs

%changelog
* Wed Jan 20 2010 Devrim GÜNDÜZ <devrim@commandprompt.com> 1.0.3-5
- Initial import to PostgreSQL RPM repository, with very little cosmetic 
  changes. Thanks Peter	for sending spec to me.

* Wed Dec 09 2009 Peter HOPFGARTNER <peter.hopfgartner@r3-gis.com> - 1.0.3-4
- New build for PostGIS 1.4.

* Tue May 05 2009 Peter HOPFGARTNER <peter.hopfgartner@r3-gis.com> - 1.0.3-3
- Adapted to CentOS 5.

* Thu Jan 01 2009 PLD Team <feedback@pld-linux.org>
All persons listed below can be reached at <cvs_login>@pld-linux.org

Revision 1.2  2009/01/14 00:19:37  djurban
- and the md5

Revision 1.1  2009/01/14 00:19:13  djurban - rel. 1, this way PLD becomes the first distribution to support routing in
  postgis on the market. opensuse kiss my ding dong.


