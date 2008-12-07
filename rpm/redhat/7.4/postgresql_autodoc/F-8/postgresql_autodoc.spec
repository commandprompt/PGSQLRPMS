Name:		postgresql_autodoc
Version:	1.31
Release:	1%{?dist}
Summary:	PostgreSQL AutoDoc Utility
Group:		Applications/Databases
License:	BSD
URL:		http://www.rbt.ca/autodoc/
Source0:	http://www.rbt.ca/autodoc/binaries/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

BuildRequires:	perl(DBD::Pg)
BuildRequires:	perl(HTML::Template), perl(Term::ReadKey)

Requires:	postgresql-server >= 8.0, perl-TermReadKey
Requires:	perl(DBD::Pg)

%description
This is a utility which will run through PostgreSQL system 
tables and returns HTML, Dot, Dia and DocBook XML which 
describes the database.

%prep
%setup -q -n %{name}

%build
%configure --datadir=%{_datadir}/pgsql
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
install -d %{buildroot}/%{_bindir}/
install -d %{buildroot}/%{_docdir}/%{name}
cp -p postgresql_autodoc %{buildroot}/%{_bindir}/
install -d %{buildroot}/%{_datadir}/pgsql/%{name}
cp -p *.tmpl %{buildroot}/%{_datadir}/pgsql/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_datadir}/pgsql/%{name}

%changelog
* Mon Mar 17 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 1.31-1
- Update to 1.31

* Sat Jun 9 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 1.30-2
- Some more fixes ber bugzilla review #200630

* Tue Jan 2 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 1.30-1
- Updated to 1.30
- Removed patch, since it is in now upstream

* Fri Dec 29 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 1.25-5
- Added a patch from Toshio Kuratomi 

* Sat Aug 19 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 1.25-4
- Fixed spec file per bugzilla review #200630

* Wed Aug 9 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 1.25-3
- Fixed license

* Thu Dec 29 2005 - Devrim GUNDUZ <devrim@commandprompt.com> 1.25-2
- Rebuilt for Fedora Core Extras submission
- Fixed rpmlint errors and warnings

* Thu Dec 29 2005 - Devrim GUNDUZ <devrim@commandprompt.com> 1.25-1
- Initial version
