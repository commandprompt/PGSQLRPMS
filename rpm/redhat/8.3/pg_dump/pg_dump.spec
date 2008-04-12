# We support RHEL 3+, and Fedora 7+ .
# RHEL 3 builds need a special macro to build.
%{?buildrhel3:%define kerbdir /usr/kerberos}

%define beta 0
%{?beta:%define __os_install_post /usr/lib/rpm/brp-compress}

%{!?kerbdir:%define kerbdir "/usr"}

%{!?ssl:%define ssl 1}
%{!?kerberos:%define kerberos 1}
%{!?nls:%define nls 1}
%{!?xml:%define xml 1}
%{!?pam:%define pam 1}
%{!?pgfts:%define pgfts 1}
%{!?uuid:%define uuid 0}

Summary:	Pg_dump binary for easy upgrade
Name:		pg_dump
Version:	8.3.1
Release:	1PGDG%{?dist}
License:	BSD
Group:		Applications/Databases
Url:		http://www.postgresql.org/ 

Source0:	ftp://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.bz2
Source5:	pg_config.h

Patch1:		rpm-pgsql.patch

Buildrequires:	glibc-devel bison flex 

BuildRequires:	readline-devel
BuildRequires:	zlib-devel >= 1.0.4

%if %ssl
BuildRequires:	openssl-devel
%endif

%if %kerberos
BuildRequires:	krb5-devel
BuildRequires:	e2fsprogs-devel
%endif

%if %xml
BuildRequires:	libxml2-devel libxslt-devel
%endif

%if %pam
BuildRequires:	pam-devel
%endif

%if %uuid
BuildRequires:	uuid-devel
%endif


BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This package provides pg_dump and pg_dumpall utilities only, to be used 
during upgrades/downgrades.

%prep
%setup -q -n postgresql-%{version}
%patch1 -p1

%build

CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS
%if %kerberos
CPPFLAGS="${CPPFLAGS} -I%{_includedir}/et" ; export CPPFLAGS
CFLAGS="${CFLAGS} -I%{_includedir}/et" ; export CFLAGS
%endif

# Strip out -ffast-math from CFLAGS....

CFLAGS=`echo $CFLAGS|xargs -n 1|grep -v ffast-math|xargs -n 100`

export LIBNAME=%{_lib}
%configure --disable-rpath \
%if %beta
	--enable-debug \
	--enable-cassert \
%endif
%if %ssl
	--with-openssl \
%endif
%if %pam
	--with-pam \
%endif
%if %kerberos
	--with-krb5 \
	--with-gssapi \
	--with-includes=%{kerbdir}/include \
	--with-libraries=%{kerbdir}/%{_lib} \
%endif
%if %nls
	--enable-nls \
%endif
%if %pgfts
	--enable-thread-safety \
%endif
%if %uuid
	--with-ossp-uuid \
%endif
%if %xml
	--with-libxml \
	--with-libxslt \
%endif
	--with-system-tzdata=%{_datadir}/zoneinfo \
	--sysconfdir=/etc/sysconfig/pgsql \
	--datadir=/usr/share/pgsql \
	--with-docdir=%{_docdir}

make %{?_smp_mflags} all

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}/
install -d %{buildroot}%{_libdir}/

install -m 755 src/bin/pg_dump/pg_dump %{buildroot}%{_bindir}/pg_dump-%{version}
install -m 755 src/bin/pg_dump/pg_dumpall %{buildroot}%{_bindir}/pg_dumpall-%{version}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/pg_dump-%{version}
%{_bindir}/pg_dumpall-%{version}

%changelog
* Thu Mar 13 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.3.1-1PGDG
- Initial packaging for pgsqlrpms project.
