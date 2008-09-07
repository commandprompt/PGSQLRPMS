Summary:	High speed data loading utility for PostgreSQL
Name:		pg_bulkload
Version:	2.3.0
Release:	1%{?dist}
URL:		http://pgfoundry.org/projects/pgbulkload/
License:	BSD
Group:		Applications/Databases
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	postgresql-devel >= 8.3
Requires:	postgresql-server

Source0:	http://pgfoundry.org/frs/download.php/1739/%{name}-%{version}.tar.gz
Source1:	pg_crc.c
Source2:	nbtsort.c
Patch1:		pg_bulkload-nopgsrc.patch

%description
pg_bulkload provides high-speed data loading capability to PostgreSQL users.

%prep
%setup -q -n %{name}

# We keep a copy of pg_crc.c and nbtsort.c in this SRPM,
# so we don't need to have the full PostgreSQL sources at hand.
cp %{SOURCE1} bin/pg_crc.c
cp %{SOURCE2} util/nbtsort.c

# Need to tell pg_bulkload to find pg_crc.c and nbtsort.c in
# its own directories:
%patch1 -p0

%build
#export CFLAGS="$RPM_OPT_FLAGS"

make USE_PGXS=1 %{?_smp_mflags}

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/%{name}
install -m 755 lib/libpg_bulkload.so %{buildroot}%{_libdir}
install -m 755 util/libpg_timestamp.so %{buildroot}%{_libdir}
install -m 755 bin/pg_bulkload %{buildroot}%{_bindir}
install -m 755 bin/postgresql %{buildroot}%{_bindir}/pg_bulkload_ctl
install -m 644 lib/pg_bulkload.sql %{buildroot}%{_datadir}/%{name}/
install -m 644 lib/uninstall_pg_bulkload.sql %{buildroot}%{_datadir}/%{name}/
install -m 644 util/pg_timestamp.sql %{buildroot}%{_datadir}/%{name}/
install -m 644 util/uninstall_pg_timestamp.sql %{buildroot}%{_datadir}/%{name}/
install -m 644 sample* %{buildroot}%{_datadir}/%{name}/

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libpg_bulkload.so
%{_libdir}/libpg_timestamp.so
%{_bindir}/pg_bulkload
%{_bindir}/pg_bulkload_ctl
%{_datadir}/%{name}/pg_bulkload.sql
%{_datadir}/%{name}/*.sql
%{_datadir}/%{name}/sample*
%doc README.pg_bulkload

%changelog
* Fri Apr 18 2008 Devrim GUNDUZ <devrim@commandprompt.com> 2.3.0-1
- Initial packaging for PGDG Repository
