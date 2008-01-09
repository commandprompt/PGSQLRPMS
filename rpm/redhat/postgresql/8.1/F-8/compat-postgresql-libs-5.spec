Summary:	PostgreSQL client programs and libraries
Name:		compat-postgresql-libs
Version:	5
Release:	1PGDG%{dist}
License:	BSD
Group:		Applications/Databases
Url:		http://www.postgresql.org/
Source0:	%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Conflicts:	postgresql-libs < 8.2.6

%description
This package provides compatibility libraries
for PostgreSQL PostgreSQL <=8.2.6

%prep
%setup -q -n %{name}-%{version}

%build

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_libdir}
install -m 755 lib*/* %{buildroot}%{_libdir}

%post
# Remove some files
/bin/rm -f %{_libdir}/libpq.so.5
# ... and now link them.
/bin/ln -s %{_libdir}/libpq.so.5.1 %{_libdir}/libpq.so.5
# Run ldconfig
/sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/libpq.so.*

%changelog
* Tue Jan 8 2008 - Devrim GUNDUZ <devrim@CommandPrompt.com> 5.1PGDG
- Initial packaging for libpq5

