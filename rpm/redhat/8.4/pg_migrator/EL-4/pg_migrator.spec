Summary:	In-place data upgrade utility for PostgreSQL
Name:		pg_migrator
Version:	8.4
Release:	alpha13%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://pgfoundry.org/frs/download.php/2230/%{name}-%{version}-alpha13.tgz
URL:		http://pgfoundry.org/projects/pg-migrator
BuildRequires:	postgresql-devel >= 8.4
Requires:	postgresql-server >= 8.3
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
pg_migrator performs an in-place upgrade of existing data when 
upgrading from an old release of PostgreSQL to a new release. Use 
pg_migrator to avoid the typical (and painful) pg_dump/reload cycle 
required by many upgrades.

%prep
%setup -q -n %{name}-%{version}-alpha13

%build
make USE_PGXS=1 %{?_smp_mflags} 

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}/
install -d %{buildroot}%{_libdir}/
install -d %{buildroot}%{_docdir}/%{name}-%{version}
install -m 755 src/pg_migrator %{buildroot}%{_bindir}
install -m 644 func/pg_migrator.so %{buildroot}%{_libdir}
install -m 644 DEVELOPERS IMPLEMENTATION INSTALL LICENSE README TODO %{buildroot}%{_docdir}/%{name}-%{version}

%clean
rm -rf %{buildroot}

#%post -p /sbin/ldconfig 
#%postun -p /sbin/ldconfig 

%files
%defattr(-,root,root,-)
%doc DEVELOPERS IMPLEMENTATION INSTALL LICENSE README TODO
%{_bindir}/pg_migrator
%{_libdir}/pg_migrator.so

%changelog
* Sun May 17 2009 - Devrim GUNDUZ <devrim@commandprompt.com> 8.4-alpha13
- Initial RPM packaging for PostgreSQL RPM Repository
