%define perl_vendorlib %(eval "`%{__perl} -V:installvendorlib`"; echo $installvendorlib)
%define perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)

%define real_name DBD-Oracle

Summary:	Oracle database driver for the DBI module.
Name:		perl-DBD-Oracle
Version:	1.22
Release:	1
License:	Artistic/GPL
Group:		Applications/CPAN
URL:		http://search.cpan.org/dist/DBD-Oracle/

Source:		http://www.cpan.org/modules/by-module/DBD/DBD-Oracle-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	perl
Requires:	perl-Tk

%description
Oracle database driver for the DBI module. 

%prep
%setup -n %{real_name}-%{version} -q

%build
export ORACLE_HOME=/usr/lib/oracle/xe/app/oracle/product/10.2.0/server
export ORACLE_SID=XE
export PATH=$PATH:$ORACLE_HOME/bin

CFLAGS="%{optflags}" %{__perl} Makefile.PL INSTALLDIRS="vendor" PREFIX="%{buildroot}%{_prefix}"
%{__make} %{?_smp_mflags} OPTIMIZE="%{optflags}"

%install
%{__rm} -rf %{buildroot}
%{__make} pure_install

### Clean up buildroot
find %{buildroot} -name .packlist -exec %{__rm} {} \;

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc Changes MANIFEST MANIFEST.SKIP README README.aix.txt
%doc README.clients.txt README.explain.txt README.help.txt README.hpux.txt
%doc README.java.txt README.linux.txt README.login.txt README.longs.txt
%doc README.macosx.txt README.sec.txt README.vms.txt README.win32.txt
%doc README.wingcc.txt Todo
%doc %{_mandir}/man1/ora_explain.*
%doc %{_mandir}/man3/DBD::Oracle.3pm*
%doc %{_mandir}/man3/DBD::Oraperl.3pm*
%{_bindir}/ora_explain
%dir %{perl_vendorarch}/DBD/
%{perl_vendorarch}/DBD/Oracle/GetInfo.pm
%{perl_vendorarch}/DBD/Oracle.pm
%dir %{perl_vendorarch}/auto/DBD/
%{perl_vendorarch}/auto/DBD/Oracle/
%{perl_vendorarch}/Oraperl.pm
%{perl_vendorarch}/oraperl.ph

%changelog
* Tue Dec 30 2008 Devrim GUNDUZ <devrim@commandprompt.com> 1.22-1
- Initial packaging. Spec file is taken from Dries repo.
