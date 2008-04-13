Name:		pgdg-redhat
Version:	8.3
Release:	4
Summary:	PostgreSQL 8.3.X PGDG RPMs for RHEL - Yum Repository Configuration
Group:		System Environment/Base 
License:	BSD
URL:		http://yum.pgsqlrpms.org
Source0:	http://yum.pgsqlrpms.org/RPM-GPG-KEY-PGDG
Source2:	pgdg-83-redhat.repo
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
Requires:	redhat-release

%description
This package contains yum configuration for RHEL, and also the GPG
key for PGDG RPMs.

%prep
%setup -q  -c -T
#install -pm 644 %{SOURCE0} .
#install -pm 644 %{SOURCE1} .

%build

%install
rm -rf %{buildroot}

install -Dpm 644 %{SOURCE0} \
	%{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PGDG

install -dm 755 %{buildroot}%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE2}  \
	%{buildroot}%{_sysconfdir}/yum.repos.d/

%clean
rm -rf %{buildroot}

%post 
rpm --import %{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PGDG

%files
%defattr(-,root,root,-)
%config %{_sysconfdir}/yum.repos.d/*
%{_sysconfdir}/pki/rpm-gpg/*

%changelog
* Sun Apr 13 2008 Devrim GUNDUZ <devrim@commandprompt.com> - 8.3-4
- Rebuilt

* Sun Apr 13 2008 Devrim GUNDUZ <devrim@commandprompt.com> - 8.3-3
- Enable srpms

* Tue Mar 11 2008 Devrim GUNDUZ <devrim@commandprompt.com> - 8.3-2
- Enable gpgcheck

* Mon Oct 8 2007 Devrim GUNDUZ <devrim@commandprompt.com> - 8.3-1
- Initial packaging for PostgreSQL Global Development Group RPMs
