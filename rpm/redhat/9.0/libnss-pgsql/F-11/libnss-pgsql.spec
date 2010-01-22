Summary:	PostgreSQL NSS module
Name:		libnss-pgsql
Version:	1.5.0
Release:	beta_2%{?dist}
Group:		System Environment/Libraries
License:	GPL+
Source0:	http://pgfoundry.org/frs/download.php/1878/%{name}-%{version}-beta.tgz
Patch0:		libnss-pgsql-includepath.patch
Patch1:		libnss-pgsql-1.5.0-beta-exit-in-library.patch
URL: 		http://pgfoundry.org/projects/sysauth/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	xmlto, postgresql-devel >= 8.1

%description
libnss-pgsql is a name service switch module that allows the 
replacement of flatfile passwd, group and shadow lookups with a 
PostgreSQL backend.

%prep
%setup -q -n %name-%{version}-beta
%patch0 -p0
%patch1 -p1
%configure --with-docdir=%{_docdir}/%{name}-%{version} --disable-static

%build
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}/usr/doc
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%exclude %{_libdir}/*.so
%doc AUTHORS COPYING ChangeLog README doc/nss-pgsql.html doc/caution.png
%{_libdir}/libnss_pgsql.so.2.0.0
%{_libdir}/libnss_pgsql.so.2
%{_libdir}/libnss_pgsql.so

%changelog
* Mon Feb 2 2009 - Devrim GUNDUZ <devrim@commandprompt.com> 1.5.0-beta.2
- Add a patch from Fedora.
- A few fixes for spec file.

* Tue Jan 13 2009 - Devrim GUNDUZ <devrim@commandprompt.com> 1.5.0-beta.1
- Initial packaging for PostgreSQL RPM Repository.
