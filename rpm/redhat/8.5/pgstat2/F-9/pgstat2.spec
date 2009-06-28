Summary:	PostgreSQL monitoring script
Name:		pgstat2
Version:	0.8
Release:	beta_1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://pgfoundry.org/frs/download.php/2107/%{name}-%{version}beta.tar.bz2
Source1:	README.pgstat2
URL:		http://pgfoundry.org/projects/pgstat2/
Requires:	postgresql-server >= 8.1, python-psycopg2
Buildarch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
pgstat is a command line utility to display PostgreSQL information on the 
command line similar to iostat or vmstat. This data can be used for 
monitoring or performance tuning.

%prep
%setup -q -n %{name}-%{version}beta

%build

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}/
install -m 755 pgstat %{buildroot}%{_bindir}/
cp %{SOURCE1} README.pgstat2

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.pgstat2
%{_bindir}/pgstat

%changelog
* Thu Mar 5 2009 - Devrim GUNDUZ <devrim@commandprompt.com> 0.8beta-1
- Update to 0.8beta
- Add a README file -- tarball does not include one.

* Wed Feb 25 2009 - Devrim GUNDUZ <devrim@commandprompt.com> 0.7beta-1
- Initial RPM packaging for yum.pgsqlrpms.org
