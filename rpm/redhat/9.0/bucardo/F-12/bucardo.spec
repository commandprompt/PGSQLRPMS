%define         realname Bucardo
Name:           bucardo
Version:        4.4.0
Release:        1%{?dist}
Summary:        Postgres replication system for both multi-master and multi-slave operations

Group:          Applications/Databases
License:        BSD
URL:            http://bucardo.org/
Source0:        http://bucardo.org/downloads/Bucardo-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:     noarch

BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(DBI)
BuildRequires:  perl(DBD::Pg)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(Sys::Hostname)
BuildRequires:  perl(Sys::Syslog)
BuildRequires:  perl(Net::SMTP)
# available from fedora 10
BuildRequires:  perl(DBIx::Safe)

Requires:  perl(ExtUtils::MakeMaker)
Requires:  postgresql-plperl

Requires:  perl(DBI)
Requires:  perl(DBD::Pg)
Requires:  perl(DBIx::Safe)
Requires:  perl(IO::Handle)
Requires:  perl(Sys::Hostname)
Requires:  perl(Sys::Syslog)
Requires:  perl(Net::SMTP)

#testsuite
Requires:  perl(Test::Simple)
Requires:  perl(Test::Harness)

%description
Bucardo is an asynchronous PostgreSQL replication system, allowing for both
multi-master and multi-slave operations.It was developed at Backcountry.com
primarily by Greg Sabino Mullane of End Point Corporation.

%prep
%setup -q -n %{realname}-%{version}


%build

%{__perl} Makefile.PL INSTALLDIRS=vendor

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} +
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

sed -i -e '1d;2i#!/usr/bin/perl' bucardo_ctl

rm -f $RPM_BUILD_ROOT/%{_bindir}/bucardo_ctl
install -Dp -m 755 bucardo_ctl $RPM_BUILD_ROOT/%{_sbindir}/bucardo_ctl
mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/run/bucardo

%{_fixperms} %{buildroot}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc bucardo_ctl.html Bucardo.pm.html Changes
%doc INSTALL LICENSE README SIGNATURE TODO
%{perl_vendorlib}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_sbindir}/bucardo_ctl
%{_datadir}/bucardo/bucardo.schema
%dir %{_localstatedir}/run/bucardo

%changelog
* Tue Nov 17 2009 Devrim GUNDUZ <devrim@gunduz.org> 4.4.0-1
- Initial packaging for PostgreSQL RPM Repository. Spec file was taken from
  Fedora, which is written by Itamar Reis Peixoto <itamar@ispbrasil.com.br> 
