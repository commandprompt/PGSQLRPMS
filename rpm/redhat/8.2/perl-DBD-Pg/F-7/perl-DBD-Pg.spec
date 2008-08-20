Name:		perl-DBD-Pg
Version:	2.9.2
Release:	1%{?dist}
Summary:	PostgreSQL database driver for the DBI module
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/DBD-Pg/
Source0:	http://www.cpan.org/authors/id/T/TU/TURNSTEP/DBD-Pg-%{version}.tar.gz

Patch0:		perl-DBD-1.31-fixver.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	perl(DBI) >= 1.38
BuildRequires:	postgresql-devel >= 7.3
BuildRequires:	perl(ExtUtils::MakeMaker)
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:	perl(DBI) >= 1.38

%description 
An implementation of DBI for PostgreSQL for Perl.

%prep
%setup -q -n DBD-Pg-%{version}
%patch0 -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*

%check
# Full test coverage requires a live PostgreSQL database (see the README file)
#export DBI_DSN=dbi:Pg:dbname=<database>
#export DBI_USER=<username>
#export DBI_PASS=<password>
#make test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README README.dev TODO
%{perl_vendorarch}/DBD/
%{perl_vendorarch}/auto/DBD/
%{perl_vendorarch}/Bundle/DBD/
%{_mandir}/man3/*.3*

%changelog
* Wed Aug 20 2008 Devrim GUNDUZ <devrim@commandprompt.com - 2.9.2-1
- Update to 2.9.2

* Fri Aug 8 2008 Devrim GUNDUZ <devrim@commandprompt.com - 2.9.0-1
- Update to 2.9.0

* Sat Jul 26 2008 May 16 2008 Devrim GUNDUZ <devrim@commandprompt.com - 2.8.7-1
- Update to 2.8.7

* Fri May 16 2008 Devrim GUNDUZ <devrim@commandprompt.com - 2.7.2-1
- Update to 2.7.2
- Initial build for PGDG Yum Repository, based on Fedora spec.


