Name:		dbi-link
Version:	2.0.0
Release:	3%{?dist}
Summary:	Partial implementation of the SQL/MED portion of the SQL:2003 specification
Group:		Applications/Databases
License:	BSD
URL:		http://pgfoundry.org/projects/dbi-link/
Source0:	http://pgfoundry.org/frs/download.php/1235/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	postgresql-server, perl, perl-DBI >= 1.52, perl-YAML >= 0.62
BuildArch:	noarch

%description
If you've ever wanted to treat DBI-accessible data sources as though
they were PostgreSQL tables, you now can.

You can do gradual, low-risk migrations from other DBMSs, add speed
and accuracy to your ETL processes...your imagination is the only
limit.

%prep
%setup -q -n %{name}-%{version}

%build

%install
rm -rf %{buildroot}
install -d %{buildroot}/%{_datadir}/%{name}/
install -p -m 644 *.sql %{buildroot}/%{_datadir}/%{name}/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc copyright.txt  IMPLEMENTATION.txt README.txt
%doc README.Oracle README.Sybase_MSSQL TODO.txt ROADMAP.txt
%doc examples
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.sql

%changelog
* Tue Feb 20 2007 - Kevin Fenzi <kevin@tummy.com> 2.0.0-3
- Move examples under the regular doc directory. 

* Tue Feb 20 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0.0-2
- 2.0.0-2
- Spec file fix per rh bugzilla #199682

* Sat Jan 27 2007 - David Fetter <david@fetter.org> 2.0.0-1
- 2.0.0
- Moved "test" files to the more appropriate "examples" directory per
  rh bugzilla # 199682.
- Put back Oracle and Excel portions as they no longer cause
  inappropriate dependencies.
- Added new Sybase/MS-SQL Server examples.

* Mon Jan 22 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0-0.4.beta1
- More spec file fixes per rh bugzilla #199682

* Wed Jan 17 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0-0.3.beta1
- A few more spec file fixes, per rh bugzilla review # 199682

* Tue Jan 16 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0-0.2.beta1
- Removed Oracle and Excel portions

* Sun Jan 14 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0-0.1.beta1
- Some fixes to spec file, per bugzilla review

* Tue Dec 12 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0beta1-1
- Update to 2.0beta1

* Fri Jul 21 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 1.0.0-2
- 1.1.0
- Fixed rpmlint errors

* Thu Dec 29 2005 - Devrim GUNDUZ <devrim@commandprompt.com> 1.0.0
- Initial version
