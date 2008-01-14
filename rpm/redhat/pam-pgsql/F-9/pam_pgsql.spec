Summary:	PAM module to authenticate using a PostgreSQL database 
Name:		pam_pgsql
Version:	0.6.3
Release:	1%{dist}
Source0:	libpam-pgsql-%{version}.tar.bz2
License:	GPLv2
URL:		http://sourceforge.net/projects/pam-pgsql/
Group:		System Environment/Base
BuildRequires:	postgresql-devel, pam-devel, mhash-devel
Requires:	postgresql >= 7.4
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch1:		pam-pgsql-getservice.patch

%description 
This module lets you authenticate users against a table in a 
PostgreSQL database. It also supports: 
- Checking account information (pam_acct_expired,new_authtok_reqd) 
- Updating auth to

%prep
%setup -q -n pam-pgsql-%{version}
%patch1 -p0

%build
%configure 
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make %{?_smp_mflags} DESTDIR=%{buildroot} install
install -d %{buildroot}/%{_lib}/security
install -m 755 pam_pgsql.so %{buildroot}/%{_lib}/security

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/%{_lib}/security/pam_pgsql.so
%doc README CREDITS

%changelog
* Wed Nov 7 2007 Devrim Gunduz <devrim@commandprompt.com> - 0.6.3-1
- Initial packaging for Fedora
