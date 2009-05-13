%define pitrtoolsdir	/var/lib/pgsql/pitrtools/

Summary:	Wrapper scripts for PostgreSQL Warm Standby
Name:		pitrtools
Version:	1.2
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	%{name}-%{version}.tar.bz2
URL:		https://projects.commandprompt.com/public/pitrtools
Requires:	postgresql-server >= 8.3, postgresql-contrib >= 8.3
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Buildarch:	noarch

%description
PITRTools is a set of wrapper scripts that provide warm standby 
functionality to PostgreSQL. The software is essentially two scripts, 
cmd_archiver.py and cmd_standby.py. The project is under the BSD 
license. 

%prep
%setup -q -n %{name}-%{version}

%build

%install
rm -rf %{buildroot}

install -d -m 700 %{buildroot}%{pitrtoolsdir}
install -d -m 700 %{buildroot}%{pitrtoolsdir}/etc
install -d -m 755 %{buildroot}%{pitrtoolsdir}/bin
install -d -m 700 %{buildroot}%{pitrtoolsdir}/doc

install -m 755 cmd_archiver cmd_standby %{buildroot}%{pitrtoolsdir}/bin
install -m 644 *.ini.sample %{buildroot}%{pitrtoolsdir}/etc
install -m 644 *.README %{buildroot}%{pitrtoolsdir}/doc

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{pitrtoolsdir}/doc/*.README
%{pitrtoolsdir}/bin/cmd_*
%{pitrtoolsdir}/etc/*.ini.sample

%changelog
* Fri Mar 27 2009 - Devrim GUNDUZ <devrim@commandprompt.com> 1.2-1
- Initial RPM packaging for PostgreSQL RPM Repository
