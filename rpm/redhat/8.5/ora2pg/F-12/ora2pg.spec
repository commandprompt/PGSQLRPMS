Summary:	Oracle to PostgreSQL database schema converter
Name:		ora2pg
Version:	5.0
Release:	4%{?dist}
Group:		Productivity/Databases/Tools
License:	Artistic License, GPL
URL:		http://www.samse.fr/GPL/ora2pg/
Source:		http://www.darold.net/projects/ora2pg/%{name}-%{version}.tar.gz
#Patch0:		%{name}-%{version}-string-compare.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

BuildRequires:	perl
Requires:	perl(DBD::Oracle) perl(DBI) perl(String::Random) perl(IO::Compress::Base

%description
This package contains a Perl module and a companion script to convert an
Oracle database schema to PostgreSQL and to migrate the data from an
Oracle database to a PostgreSQL database.

%prep
%setup
#%patch0 -p1 

%build

%install
install -m 644 -D Ora2Pg.pm %{buildroot}%{perl_vendorarch}/Ora2Pg.pm
install -m 755 -D ora2pg.pl %{buildroot}/usr/bin/ora2pg
mkdir -p %{buildroot}/usr/share/man/man1 %{buildroot}/usr/share/man/man3
pod2man Ora2Pg.pm %{buildroot}/usr/share/man/man3/Ora2Pg.3
ln -s /usr/share/man/man3/Ora2Pg.3.gz %{buildroot}/usr/share/man/man1/ora2pg.1.gz

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc ora2pg.conf CHANGES TODO
%{_prefix}/*

%changelog
* Fri Mar 20 2009 Devrim GUNDUZ <devrim@commandprompt.com> 5.0-1
- Initial release, based on Peter's spec file.
