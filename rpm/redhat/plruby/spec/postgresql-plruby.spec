%{!?ruby_sitearch: %define ruby_sitearch %(ruby -rrbconfig -e "puts Config::CONFIG['sitearchdir']")}
%define sname	plruby

Summary:	PostgreSQL Ruby Procedural Language
Name:		postgresql-%{sname}
Version:	0.5.1
Release:	2%{?dist}
Source0:	ftp://moulon.inra.fr/pub/ruby/%{sname}-%{version}.tar.gz
License:	Ruby License
Group:		Applications/Databases
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Url:		http://raa.ruby-lang.org/project/pl-ruby
BuildRequires:	ruby >= 1.8 ruby-devel >= 1.8 postgresql-devel > 8.0
Requires:	postgresql-libs, ruby(abi) = 1.8

%description
PL/Ruby is a loadable procedural language for the PostgreSQL database
system that enable the Ruby language to create functions and trigger 
procedures.

%package doc
Summary:	Documentation for plruby
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description doc
Documentation for plruby.

%prep
%setup -q -n %{sname}-%{version}

%build
ruby extconf.rb  

make %{?smp_flags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} %{?smp_flags} install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc Changes README.en plruby.html 
%dir %{ruby_sitearch}
%dir %{ruby_sitearch}/plruby
%{ruby_sitearch}/plruby/plruby_*.so
%{ruby_sitearch}/plruby.so

%files doc
%defattr(-,root,root)
%doc docs/plruby.rb

%changelog
* Sat Oct 6 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 0.5.1-2
- Updates to spec file per bz review #246793

* Fri Oct 5 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 0.5.1-1
- Update to 0.5.1

* Tue Jul 17 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 0.5.0-2
- Minor fixes to spec file.

* Wed Jul 4 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 0.5.0-1
- Update to 0.5.0

* Sat Jun 16 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 0.4.8-1
- Initial packaging for Fedora
