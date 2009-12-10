Name:		proj
Version:	4.7.0
Release:	1%{?dist}
Epoch:		0
Summary:	Cartographic projection software (PROJ.4)

Group:		Applications/Engineering
License:	MIT
URL:		http://trac.osgeo.org/proj
Source0:	http://download.osgeo.org/%{name}/%{name}-%{version}.tar.gz
Source1:	http://download.osgeo.org//proj/proj-datumgrid-1.5.zip
Source2:	http://packages.debian.org/changelogs/pool/main/p/proj/proj_4.4.8-3/proj.copyright
Patch0:		proj.copyright.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	libtool

%package devel
Summary:	Development files for PROJ.4
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%package nad
Summary:	US, Canadian, French and New Zealand datum shift grids for PROJ.4
Group:		Applications/Engineering
Requires:	%{name} = %{version}-%{release}

%package epsg
Summary:	EPSG dataset for PROJ.4
Group:		Applications/Engineering
Requires:	%{name} = %{version}-%{release}

%description
Proj and invproj perform respective forward and inverse transformation of
cartographic data to or from cartesian data with a wide range of selectable
projection functions. Proj docs: http://www.remotesensing.org/dl/new_docs/

%description devel
This package contains libproj and the appropriate header files and man pages.

%description nad
This package contains additional US and Canadian datum shift grids.

%description epsg
This package contains additional EPSG dataset.

%prep
%setup -q

# Prepare copyright
cp %{SOURCE2} ./
%patch0 -p0 -b .buildroot
cp proj.copyright COPYING

# disable internal libtool to avoid hardcoded r-path
for makefile in `find . -type f -name 'Makefile.in'`; do
sed -i 's|@LIBTOOL@|%{_bindir}/libtool|g' $makefile
done

# Prepare nad
cd nad
unzip %{SOURCE1}
cd ..
# fix shebag header of scripts
for script in `find nad/ -type f -perm -a+x`; do
sed -i -e '1,1s|:|#!/bin/bash|' $script
done

%build
%configure
make OPTIMIZE="$RPM_OPT_FLAGS" %{?_smp_mflags}

%install
rm -rf %{buildroot}
%makeinstall
install -p -m 0644 nad/pj_out27.dist nad/pj_out83.dist nad/td_out.dist %{buildroot}%{_datadir}/%{name}
install -p -m 0755 nad/test27 nad/test83 nad/testvarious %{buildroot}%{_datadir}/%{name}
install -p -m 0644 nad/epsg %{buildroot}%{_datadir}/%{name}

%check
pushd nad
# set test enviroment for porj
export PROJ_LIB=%{buildroot}%{_datadir}/%{name}
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH%{buildroot}%{_libdir}
# run tests for proj
./test27      %{buildroot}%{_bindir}/%{name} || exit 0
./test83      %{buildroot}%{_bindir}/%{name} || exit 0
./testntv2    %{buildroot}%{_bindir}/%{name} || exit 0
./testvarious %{buildroot}%{_bindir}/%{name} || exit 0
popd

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc NEWS AUTHORS COPYING README ChangeLog
%{_bindir}/*
%{_mandir}/man1/*.1*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_mandir}/man3/*.3*
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.a
%exclude %{_libdir}/libproj.la

%files nad
%defattr(-,root,root,-)
%doc nad/README
%attr(0755,root,root) %{_datadir}/%{name}/test27
%attr(0755,root,root) %{_datadir}/%{name}/test83
%attr(0755,root,root) %{_datadir}/%{name}/testvarious
%exclude %{_datadir}/%{name}/epsg
%{_datadir}/%{name}

%files epsg
%defattr(-,root,root,-)
%doc nad/README
%attr(0644,root,root) %{_datadir}/%{name}/epsg

%changelog
* Thu Dec 10 2009 - Devrim GUNDUZ <devrim@commandprompt.com> - 0:4.7.0-1
- Update to 4.7.0
- Update proj-datumgrid to 1.5
- Fix attr issue for epsg package.

* Tue Dec 2 2008 - Devrim GUNDUZ <devrim@commandprompt.com> - 0:4.6.1-1
- Update to 4.6.1
- Update URLs

* Thu Apr 3 2008 - Devrim GUNDUZ <devrim@commandprompt.com> - 0:4.6.0-1
- Initial build for pgsqlrpms.org, based on Fedora/EPEL spec.

