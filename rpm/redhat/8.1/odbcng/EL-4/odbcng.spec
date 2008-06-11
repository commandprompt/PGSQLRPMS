Name:		odbcng
Summary:	PostgreSQL ODBCng driver
Version:	0.90.101
Release:	1%{?dist}
License:	GPLv2
Group:		Applications/Databases
Url:		http://projects.commandprompt.com/public/%{name}
Source0:	http://projects.commandprompt.com/public/%{name}/attachment/wiki/Downloads/%{name}-%{version}.tar.gz

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	openssl-devel
BuildRequires:	libtool automake autoconf 

%description
ODBCng is a written from scratch ODBC driver for PostgreSQL 8.x.
ODBCng is a wire-level ODBC driver meaning that we do not require 
libpq or any PostgreSQL libraries be installed to function.

%prep
%setup -q -n %{name}-%{version}

aclocal
libtoolize --force
autoconf

sed -i.strip -e 's|strip|true strip|' makefile.in

%build

%configure --with-ssl

make

%install
rm -rf %{buildroot}
install -m 755 -d %{buildroot}/%{_libdir}
install -m 755 ./.libs/libmodbc.so* %{buildroot}/%{_libdir}

pushd %{buildroot}/%{_libdir}
popd
strip %{buildroot}/%{_libdir}/*.so

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%attr(755,root,root) %{_libdir}/libmodbc.so*
%doc COPYING COPYRIGHT LICENSE.txt

%changelog
* Sat May 17 2008 Devrim GUNDUZ <devrim@commandprompt.com> - 0.90.101-1
- initial build for Fedora
