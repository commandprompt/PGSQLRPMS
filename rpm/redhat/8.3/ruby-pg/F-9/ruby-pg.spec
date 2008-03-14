%{!?ruby_sitearch: %define ruby_sitearch %(ruby -rrbconfig -e "puts Config::CONFIG['sitearchdir']")}

Name:		ruby-pg
Version:	0.7.9.2008.02.05
Release:	1%{?dist}
Summary:	A Ruby interface for the PostgreSQL database engine
Group:		Development/Languages
License:	Ruby
URL: 		http://rubyforge.org/projects/ruby-pg
Source:		http://rubyforge.org/frs/download.php/31847/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  ruby >= 1.8 ruby-devel >= 1.8 postgresql-devel >= 8.1

Obsoletes:	ruby-postgres >= 0.7.1

%description
ruby-pg is a Ruby interface to the PostgreSQL Relational Database 
Management System. ruby-pg is a fork of the  unmaintained 
ruby-postgres project. ruby-pg is API-compatible (a drop-in 
replacement) with ruby-postgres.

%prep
%setup -q -n %{name}
chmod a-x sample/psql.rb

%build
ruby ext/extconf.rb --with-pgsql-include=%{_includedir}/pgsql/server -with-cflags="$RPM_OPT_FLAGS"

%install
rm -rf %{buildroot}
CC="%{__cc} -I%{_includedir}/pgsql -I%{_includedir}/pgsql/server" make DESTDIR=%{buildroot} %{?_smp_mflags} install

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc ChangeLog README README.ja doc LICENSE sample
%{ruby_sitearch}/pg.so

%changelog
* Fri Mar 14 2008 Devrim GUNDUZ <devrim@commandprompt.com> - 0.7.9.2008.02.05
- Initial build
