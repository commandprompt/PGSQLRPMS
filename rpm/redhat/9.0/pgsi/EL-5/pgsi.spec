Summary:	PostgreSQL Log Analyzer Script
Name:		pgsi
Version:	1.1.1
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://bucardo.org/downloads/%{name}-%{version}.tar.gz
URL:		http://bucardo.org/pgsi
Requires:	postgresql-server >= 7.4
Requires:	perl(Data::Dumper) perl(Getopt::Long) perl(IO::Handle) perl(Time::Local)
BuildRequires:	perl-Test-Simple >= 0.80 perl-ExtUtils-MakeMaker
Buildarch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
PGSI is a Perl utility for parsing and analyzing PostgreSQL logs to 
produce wiki-ready system impact reports.

%prep
%setup -q

%build
perl Makefile.PL
make

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_bindir}/
install -d %{buildroot}%{_mandir}/man3
install -d %{buildroot}%{_docdir}/%{name}-%{version}
install -m 755 pgsi.pl %{buildroot}%{_bindir}/
install -m 644 tmp/pgsi.pl.1 tmp/pgsi.3pm %{buildroot}%{_mandir}/man3
install -m 644 Changes INSTALL LICENSE MANIFEST MANIFEST.SKIP pgsi.html README  SIGNATURE %{buildroot}%{_docdir}/%{name}-%{version}/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}.pl
%{_mandir}/man3/*
%dir %{_docdir}/%{name}-%{version}
%{_docdir}/%{name}-%{version}/*

%changelog
* Sun Feb 15 2009 - Devrim GUNDUZ <devrim@commandprompt.com> 1.1.1-1
- Initial RPM packaging for yum.pgsqlrpms.org
