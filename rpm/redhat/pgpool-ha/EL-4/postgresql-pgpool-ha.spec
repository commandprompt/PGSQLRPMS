%define short_name	pgpool-ha

Summary:	Pgpool-HA uses heartbeat to keep pgpool from being a single point of failure
Name:		postgresql-%{short_name}
Version:	1.1.0
Release:	4%{?dist}
License:	BSD
Group:		Applications/Databases
URL:		http://pgpool.projects.PostgreSQL.org
Source0:	http://pgfoundry.org/frs/download.php/1400/%{short_name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	heartbeat >= 2.0
BuildRequires:	heartbeat-devel >= 2.0 postgresql-pgpool-II

%description
Pgpool-HA combines pgpool with heartbeat. Pgpool is a replication
server of PostgreSQL and makes reliability, but the pgpool server is
always a single point failure.  Pgpool-HA uses heartbeat to eliminate
this.

%prep
%setup -q -n %{short_name}-%{version}

%build
%configure --bindir=%{_bindir} --sysconfdir=%{_sysconfdir} --mandir=%{_mandir} --libdir=%{_libdir}
make %{?smp_flags} -C src

%install
rm -rf %{buildroot}
cd src
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sysconfdir}/ha.d/resource.d/heartbeat/
install -d %{buildroot}%{_datadir}/ocf/resource.d/heartbeat/
install -m 755 pgpool.monitor %{buildroot}%{_bindir}/pgpool.monitor
install -m 755 pgpool %{buildroot}%{_sysconfdir}/ha.d/resource.d/heartbeat/pgpool
install -m 755 pgpool %{buildroot}%{_datadir}/ocf/resource.d/heartbeat/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/pgpool.monitor
%{_sysconfdir}/ha.d/resource.d/heartbeat/pgpool
%{_datadir}/ocf/resource.d/heartbeat/pgpool
%doc AUTHORS COPYING INSTALL README.ja ChangeLog doc README 

%changelog
* Mon Jul 9 2007 Devrim GUNDUZ <devrim@CommandPrompt.com> 1.1.0-4
- Made package arch, per bz review.
- Move ocf path back to datadir/ocf/resource.d .

* Thu Jul 5 2007 Devrim GUNDUZ <devrim@CommandPrompt.com> 1.1.0-3
- Fix ocf path

* Wed Jul 4 2007 Devrim GUNDUZ <devrim@CommandPrompt.com> 1.1.0-2
- Removed make install (per bz review)
- Fix rpmlint errors

* Sun Jun 24 2007 Devrim GUNDUZ <devrim@CommandPrompt.com> 1.1.0-1
- Update to 1.1.0

* Sat Jun 02 2007 Devrim GUNDUZ <devrim@CommandPrompt.com> 1.0.0-4
- Fixes to spec file, per bz review #229322

* Wed Apr 18 2007 Devrim GUNDUZ <devrim@CommandPrompt.com> 1.0.0-3
- Added heartbeat-devel as buildrequires, per #229322
- Removed vendor tag
- Added /usr/lib/ocf/resource.d/heartbeat/pgpool

* Tue Oct 10 2006 Devrim GUNDUZ <devrim@CommandPrompt.com> 1.0.0-2
- Some fixes to spec file

* Tue Oct 10 2006 David Fetter <david@fetter.org> 1.0.0-1
- Initial build pgpool-HA 1.0.0 for PgPool Global Development Group
