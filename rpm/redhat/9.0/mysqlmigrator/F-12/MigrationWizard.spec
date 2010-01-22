Name:		MigrationWizard
Version:        1.1
Release:        1%{?dist}
Summary:	MySQL to PostgreSQL Migration Wizard

Group:		Application/Databases
License:	BSD
URL:		http://www.enterprisedb.com/
Source0:	http://files.pgsqlrpms.org/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:	noarch

BuildRequires:	ant
Requires:	java

%description
This is MySQL to PostgreSQL Migration Wizard by EnterpriseDB.

%prep
%setup -q -n wizard

%build
ant compile

%install
rm -rf %{buildroot}
ant dist
install -d %{buildroot}%{_datadir}/%{name}
install -d %{buildroot}%{_datadir}/%{name}/lib
install -m 644 dist/*.jar %{buildroot}%{_datadir}/%{name}
install -m 644 dist/lib/* %{buildroot}%{_datadir}/%{name}/lib

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.jar
%{_datadir}/%{name}/lib/*

%changelog
* Wed Oct 28 2009 Devrim Gunduz <devrim@CommandPrompt.com> 1.1-1
- Initial build for PostgreSQL RPM Repository

