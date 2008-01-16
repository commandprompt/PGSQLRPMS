Summary:	PostgreSQL client programs and libraries
Name:		compat-postgresql-libs
Version:	3
Release:	2PGDG%{dist}
License:	BSD
Group:		Applications/Databases
Url:		http://www.postgresql.org/
Source0:	%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This package provides compatibility libraries for PostgreSQL

%prep
%setup -q -n %{name}-%{version}

%build

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_libdir}
install -m 755 lib*/* %{buildroot}%{_libdir}

%post
# Remove some files
/bin/rm -f %{_libdir}/libpq.so.3
# ... and now link them.
/bin/ln -s %{_libdir}/libpq.so.3.1 %{_libdir}/libpq.so.3
/sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/libpq.so.*

%changelog
* Sun Jan 13 2008 - Devrim GUNDUZ <devrim@CommandPrompt.com> 3.2PGDG
- Fix libpq version number

* Tue Jan 8 2008 - Devrim GUNDUZ <devrim@CommandPrompt.com> 3.1PGDG
- Initial packaging for libpq3

