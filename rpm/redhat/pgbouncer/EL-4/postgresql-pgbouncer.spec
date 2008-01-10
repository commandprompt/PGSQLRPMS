%define sname	pgbouncer
%define debug 0
%{?debug:%define __os_install_post /usr/lib/rpm/brp-compress}

Name:		postgresql-%{sname}
Version:	1.0.8
Release:	2%{?dist}
Summary:	Lightweight connection pooler for PostgreSQL
Group:		Applications/Databases
License:	BSD
URL:		http://pgfoundry.org/projects/pgbouncer/
Source0:	http://pgfoundry.org/frs/download.php/1356/%{sname}-%{version}.tgz
Source1:	%{sname}.init
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	libevent-devel
Requires:	libevent initscripts

%description
pgbouncer is a lightweight connection pooler for PostgreSQL.
pgbouncer uses libevent for low-level socket handling.

%prep
%setup -q -n %{sname}-%{version}

%build
%configure \
%if %debug
	--enable-debug \
	--enable-cassert \
%endif
--datadir=%{_datadir} 

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
install -d %{buildroot}%{_sysconfdir}/
install -m 644 etc/pgbouncer.ini %{buildroot}%{_sysconfdir}/
rm -f %{buildroot}%{_docdir}/%{sname}/pgbouncer.ini
install -d %{buildroot}%{_initrddir}
install -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{sname}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README NEWS
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/%{sname}.ini
%{_initrddir}/%{sname}


%changelog
* Tue Sep 25 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 1.0.8-2
- Added init script from Darcy.

* Tue Sep 18 2007 - Darcy Buskermolen <darcyb@commandprompt.com> 1.0.8-1
- Update to pgBouncer 1.0.8
- Add libevent to requires

* Sat Jun 18 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 1.0.7-2
- Prepare for Fedora review
- Change spec file name

* Thu May 03 2007 David Fetter <david@fetter.org> 1.0.7-1
- Initial build 
