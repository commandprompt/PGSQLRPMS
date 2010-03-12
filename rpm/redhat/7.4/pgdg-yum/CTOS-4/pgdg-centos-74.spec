Name:		pgdg-centos
Version:	7.4
Release:	5
Summary:	PostgreSQL 7.4.X PGDG RPMs for CentOS - Yum Repository Configuration
Group:		System Environment/Base 
License:	BSD
URL:		http://yum.pgsqlrpms.org
Source0:	http://yum.pgsqlrpms.org/RPM-GPG-KEY-PGDG
Source2:	pgdg-74-centos.repo
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
Requires:	centos-release

%description
This package contains yum configuration for CentOS, and also the GPG
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
* Thu Mar 11 2010 CMD RPM Packagers <packages@commandprompt.com> - 7.4-5
- Rebuilt for new key

* Sun Apr 13 2008 Devrim GUNDUZ <devrim@commandprompt.com> - 7.4-4
- Rebuilt

* Sun Apr 13 2008 Devrim GUNDUZ <devrim@commandprompt.com> - 7.4-3
- Enable srpms   

* Tue Mar 11 2008 Devrim GUNDUZ <devrim@commandprompt.com> - 7.4-2
- Enable gpgcheck

* Mon Oct 8 2007 Devrim GUNDUZ <devrim@commandprompt.com> - 7.4-1
- Initial packaging for PostgreSQL Global Development Group RPMs
