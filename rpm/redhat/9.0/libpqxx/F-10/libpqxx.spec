Name:           libpqxx
Version:        3.0.2
Release:        1%{?dist}
Summary:        C++ client API for PostgreSQL

Group:          System Environment/Libraries
License:        BSD
URL:            http://pqxx.org/
Source0:	http://pqxx.org/download/software/%{name}/%{name}-%{version}.tar.gz
Source1:        http://pqxx.org/download/software/%{name}/%{name}-%{version}.tar.gz.md5sum
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# drop -Werror for now, since we get -fvisibility warnings using gcc-4.1.1/fc6+
# http://thaiopensource.org/development/libpqxx/ticket/83
Patch1:         libpqxx-2.6.8-visibility.patch
Patch2:         libpqxx-3.0-gcc43.patch
Patch3:         libpqxx-2.6.8-multilib.patch

BuildRequires:  automake libtool
BuildRequires:  postgresql-devel
BuildRequires:  pkgconfig

%description
C++ client API for PostgreSQL. The standard front-end (in the sense of
"language binding") for writing C++ programs that use PostgreSQL.
Supersedes older libpq++ interface.

%package devel
Summary:        Development tools for %{name} 
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires:       postgresql-devel
%description devel
%{summary}.

%prep
%setup -q

# fix spurious permissions
chmod -x COPYING INSTALL

#if ! 0%{?fedora} > 8 
%patch1 -p1 -b .visibility
#endif
%patch2 -p1 -b .gcc43
%patch3 -p1 -b .multilib

# better fix/hack for current rpath issues
autoreconf


%build
%configure --enable-shared --disable-static

# rpath sucks...
#sed -i -e 's/hardcode_into_libs=yes/hardcode_into_libs=no/' libtool

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_libdir}/lib*.la


%check 
# not enabled, by default, takes awhile.
%{?_with_check:make check }


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README TODO VERSION
%{_libdir}/libpqxx-*.so

%files devel
%defattr(-,root,root,-)
%doc README-UPGRADE
%{_bindir}/pqxx-config
%{_includedir}/pqxx/
%{_libdir}/libpqxx.so
%{_libdir}/pkgconfig/libpqxx.pc


%changelog
* Wed Sep 2 2009 Devrim GUNDUZ <devrim@commandprompt.com> 3.0.2-1
- Update to 3.0.2

* Mon Jun 29 2009 Devrim GUNDUZ <devrim@commandprompt.com> 3.0.1-1
- Update to 3.0.1

* Tue Dec 2 2008 Devrim GUNDUZ <devrim@commandprompt.com> 3.0.0-1
- Update to 3.0.0
- Update gcc 4.3 patch

* Sat Jun 28 2008 Devrim GUNDUZ <devrim@commandprompt.com> 2.6.9-1
- Initial build for PGDG Yum Repository, based on Fedora spec.
  Please note that this build probably won't work with koffice,
  but I will ignore that.
