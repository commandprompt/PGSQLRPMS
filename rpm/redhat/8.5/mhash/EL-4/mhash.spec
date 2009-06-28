Summary:	Thread-safe hash algorithms library
Name:		mhash
Version:	0.9.9.9
Release:	1%{dist}
URL:		http://mhash.sourceforge.net/
License:	LGPL
Group:		System Environment/Libraries
Source:		http://easynews.dl.sourceforge.net/sourceforge/mhash/mhash-%{version}.tar.bz2
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
Provides:	libmhash = %{version}-%{release}

%description
Mhash is a free library which provides a uniform interface to a
large number of hash algorithms.

These algorithms can be used to compute checksums, message digests,
and other signatures. The HMAC support implements the basics for
message authentication, following RFC 2104. In the later versions
some key generation algorithms, which use hash algorithms, have been
added. Currently, the library supports the algorithms: SHA1, GOST,
HAVAL256, HAVAL224, HAVAL192, HAVAL160, HAVAL128, MD5, MD4, MD2,
RIPEMD128/160/256/320, TIGER, TIGER160, TIGER128, SHA224/384/512,
Whirlpool, SNEFRU128/256, CRC32B and CRC32 checksums.


%package -n %{name}-devel
Summary: Header files and libraries for developing apps which use mhash
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Provides: libmhash-devel = %{version}-%{release}

%description -n %{name}-devel
This package contains the header files and libraries needed to
develop programs that use the mhash library.

%prep
%setup -q

%build
%configure --enable-shared %{?_with_static: --enable-static} %{!?_with_static: --disable-static}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%makeinstall

%post -n %{name} -p /sbin/ldconfig

%postun -n %{name} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files -n %{name}
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README THANKS TODO
%{_libdir}/*.so.*

%files -n %{name}-devel
%defattr(-,root,root,-)
%doc ChangeLog ./doc/*.c ./doc/skid2-authentication
%dir %{_includedir}/mutils
%{_includedir}/*.h
%{_includedir}/mutils/*.h
%{?_with_static: %{_libdir}/*.a}
%{_libdir}/*.so
%exclude %{_libdir}/*.la
%{_mandir}/man3/*

%changelog
* Sun Feb 1 2009 Devrim GUNDUZ <devrim@commandprompt.com> - 0.9.9.9-1
- Update to 0.9.9.9

* Tue Jan 13 2008  Devrim GUNDUZ <devrim@commandprompt.com> - 0.9.9-1
- Initial build for PostgreSQL RPM Repository, based on EPEL spec.
