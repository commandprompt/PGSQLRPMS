%define oldname libevent

Name:		compat-libevent11
Version:	1.1a
Release:	1%{dist}
Summary:	Abstract asynchronous event notification library

Group:		System Environment/Libraries
License:	BSD
URL:		http://monkey.org/~provos/libevent/
Source0:	http://monkey.org/~provos/libevent-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Obsoletes:	%{oldname} < 1.2
Provides:	%{oldname} = 1.2

%description
The libevent API provides a mechanism to execute a callback function
when a specific event occurs on a file descriptor or after a timeout
has been reached. libevent is meant to replace the asynchronous event
loop found in event driven network servers. An application just needs
to call event_dispatch() and can then add or remove events dynamically
without having to change the event loop.

%package devel
Summary:	Header files and libraries for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -q -n %{oldname}-%{version}

%build
%configure \
    --disable-dependency-tracking
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
rm -f %{buildroot}%{_libdir}/*.la

%check
make verify

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,0755)
%doc README
%{_libdir}/libevent-%{version}.so.*

%files devel
%defattr(-,root,root,0755)
%doc sample/*.c
%{_includedir}/event.h
%{_libdir}/libevent.so
%{_libdir}/libevent.a
%{_mandir}/man3/*



%changelog
* Wed Sep 09 2009 Pavel Lisy <pavel.lisy@gmail.com> 1.1a-1
- based on libevent-1.1a-3.2.1
- name changed to compat-libevent11 for use with new libevent from PGDG84 repository
- Fix some rpmlint warnings (Devrim)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> -
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.1a-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.1a-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 24 2006 Warren Togami <wtogami@redhat.com> - 1.1a-3
- rebuild (#177697)

* Mon Jul 04 2005 Ralf Ertzinger <ralf@skytale.net> - 1.1a-2
- Removed unnecessary -r from rm

* Fri Jun 17 2005 Ralf Ertzinger <ralf@skytale.net> - 1.1a-1
- Upstream update

* Wed Jun 08 2005 Ralf Ertzinger <ralf@skytale.net> - 1.1-2
- Added some docs
- Moved "make verify" into %%check

* Mon Jun 06 2005 Ralf Ertzinger <ralf@skytale.net> - 1.1-1
- Initial build for Fedora Extras, based on the package
  by Dag Wieers
