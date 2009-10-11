Summary:	Implementation of SQL/PSM language for PostgreSQL
Name:		plpgpsm
Version:	0.3.1
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://pgfoundry.org/frs/download.php/1805/%{name}-%{version}.tar.gz
URL:		http://pgfoundry.org/projects/plpsm/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)

BuildRequires:	postgresql-devel
Requires:	postgresql

%description 	
In 1998 a draft of the new standard became part of SQL3 - under the
name SQL/PSM (ANSI/ISO/IEC 9075-4:1999). Unfortunately at that time
most big companies had their own languages (incompatible with the
standard) and refused to abandon them in favor of standard. SQL/PSM
was implemented only in those RDBMS, in which there was no support for
stored procedures before 1998. Except for DB2 (SQL PL, IBM, 2001) all
of them were minor RDBMS: Miner, Solid, 602SQL Server. After 2005 the
SQL/PSM standard started to become more popular, when it was
implemented in Advantage Database Server (Sybase iAnywhere, 2005),
MySQL (2005) and PostgreSQL (2007). Implementation of SQL/PSM is
usually incomplete, SQL PL in DB2 is considered to be one of the best
implementations. PostgreSQL implementation is called PL/pgPSM (using
the standard naming scheme in PostgreSQL).

%prep
%setup -q -n %{name}

%build
USE_PGXS=1 make %{?_smp_mflags} 

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/pgsql/
install -d %{buildroot}%{_datadir}/%{name}
install -m 755 libplpgpsm.so.0.0 %{buildroot}%{_libdir}/pgsql/plpgpsm.so
install -p -m 644 plpgpsm.sql %{buildroot}%{_datadir}/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc INSTALL.plpgpsm
%{_libdir}/pgsql/plpgpsm.so
%{_datadir}/%{name}/plpgpsm.sql

%changelog
* Wed May 21 2008 - Pavel STEHULE <pavel.stehule@gmail.com> 0.3.1-1
- Initial packaging
