Name:		uuid
Version:	1.5.1
Release:	4%{?dist}
Summary:	Universally Unique Identifier library
License:	MIT
Group:		System Environment/Libraries
URL:		http://www.ossp.org/pkg/lib/uuid/
Source0:	ftp://ftp.ossp.org/pkg/lib/uuid/uuid-%{version}.tar.gz
Patch0:		ossp-uuid.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	/usr/bin/libtool

%description
OSSP uuid is a ISO-C:1999 application programming interface (API)
and corresponding command line interface (CLI) for the generation
of DCE 1.1, ISO/IEC 11578:1996 and RFC 4122 compliant Universally
Unique Identifier (UUID). It supports DCE 1.1 variant UUIDs of version
1 (time and node based), version 3 (name based, MD5), version 4
(random number based) and version 5 (name based, SHA-1). Additional
API bindings are provided for the languages ISO-C++:1998, Perl:5 and
PHP:4/5. Optional backward compatibility exists for the ISO-C DCE-1.1
and Perl Data::UUID APIs.

%package devel
Summary:	Development support for Universally Unique Identifier library
Group:		Development/Libraries
Requires:	%{_libdir}/pkgconfig
Requires:	%{name} = %{version}-%{release}

%description devel
Development headers and libraries for OSSP uuid.

%package c++
Summary:	C++ support for Universally Unique Identifier library
Group:		System Environment/Libraries
Requires:	%{name} = %{version}-%{release}

%description c++
C++ libraries for OSSP uuid.

%package c++-devel
Summary:	C++ development support for Universally Unique Identifier library
Group:		Development/Libraries
Requires:	%{name}-c++ = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}

%description c++-devel
C++ development headers and libraries for OSSP uuid.

%package perl
Summary:	Perl support for Universally Unique Identifier library
Group:		Development/Libraries
BuildRequires:	perl(ExtUtils::MakeMaker)
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:	%{name} = %{version}-%{release}

%description perl
Perl OSSP uuid modules, which includes a Data::UUID replacement.

%package php
Summary:	PHP support for Universally Unique Identifier library
Group:		Development/Libraries
BuildRequires:	/usr/bin/phpize
Requires:	%{_libdir}/php/modules
Requires:	%{name} = %{version}-%{release}

%description php
PHP OSSP uuid module.

%package dce
Summary:	DCE support for Universally Unique Identifier library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description dce
DCE OSSP uuid library.

%package dce-devel
Summary:	DCE development support for Universally Unique Identifier library
Group:		Development/Libraries
Requires:	%{name}-dce = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}

%description dce-devel
DCE development headers and libraries for OSSP uuid.

%prep
%setup -q
%patch0 -p1

%build
# Build the library.
export LIB_NAME=libossp-uuid.la
export DCE_NAME=libossp-uuid_dce.la
export CXX_NAME=libossp-uuid++.la
export PHP_NAME=$RPM_SOURCE_DIR/php/modules/ossp-uuid.so
%configure \
    --disable-static \
    --without-perl \
    --without-php \
    --with-dce \
    --with-cxx \
    --without-pgsql

make LIBTOOL=/usr/bin/libtool %{?_smp_mflags}

# Build the Perl module.
pushd perl
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS" COMPAT=1
%{__perl} -pi -e 's/^\tLD_RUN_PATH=[^\s]+\s*/\t/' Makefile
make %{?_smp_mflags}
popd

# Build the PHP module.
pushd php
phpize
CFLAGS="$RPM_OPT_FLAGS -I.. -L.. -L../.libs"
%configure --enable-uuid
sed -i -e '/^LDFLAGS =/s/-Wl,-rpath,[^[:space:]]*//' Makefile
make LIBTOOL=/usr/bin/libtool %{?_smp_mflags}
popd

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.la %{buildroot}%{_libdir}/*.a
chmod 755 %{buildroot}%{_libdir}/*.so.*.*.*

# Install the Perl modules.
pushd perl
make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name '*.bs' -size 0 -exec rm -f {} \;
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*
popd

# Install the PHP module.
pushd php
make install INSTALL_ROOT=%{buildroot}
rm -f %{buildroot}%{_libdir}/php/modules/*.a
popd

%check
make check

pushd perl
LD_LIBRARY_PATH=../.libs make test
popd

pushd php
LD_LIBRARY_PATH=../.libs make test
popd

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%post c++ -p /sbin/ldconfig

%post dce -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%postun c++ -p /sbin/ldconfig

%postun dce -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog HISTORY NEWS PORTING README SEEALSO THANKS TODO USERS
%{_bindir}/uuid
%{_libdir}/libossp-uuid.so.*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%{_bindir}/uuid-config
%{_includedir}/uuid.h
%{_libdir}/libossp-uuid.so
%{_libdir}/pkgconfig/ossp-uuid.pc
%{_mandir}/man3/ossp-uuid.3*

%files c++
%defattr(-,root,root,-)
%{_libdir}/libossp-uuid++.so.*

%files c++-devel
%defattr(-,root,root,-)
%{_includedir}/uuid++.hh
%{_libdir}/libossp-uuid++.so
%{_mandir}/man3/uuid++.3*

%files perl
%defattr(-,root,root,-)
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Data*
%{perl_vendorarch}/OSSP*
%{_mandir}/man3/Data::UUID.3*
%{_mandir}/man3/OSSP::uuid.3*

%files php
%defattr(-,root,root,-)
%{_libdir}/php4/*

%files dce
%defattr(-,root,root,-)
%{_libdir}/libossp-uuid_dce.so.*

%files dce-devel
%defattr(-,root,root,-)
%{_includedir}/uuid_dce.h
%{_libdir}/libossp-uuid_dce.so

%changelog
* Tue Oct 7 2008 Devrim GUNDUZ <devrim@commandprompt.com> 1.5.1-4
- Initial build for yum.pgsqlrpms.org, based on EPEL spec
