Name:		pgdg-fedora
Version:	8.4
Release:	2
Summary:	PostgreSQL 8.4.X PGDG RPMs for Fedora - Yum Repository Configuration
Group:		System Environment/Base 
License:	BSD
URL:		http://yum.pgsqlrpms.org
Source0:	http://yum.pgsqlrpms.org/RPM-GPG-KEY-PGDG
Source2:	pgdg-84-fedora.repo
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
Requires:	fedora-release

%description
This package contains yum configuration for Fedora, and also the GPG
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
* Thu Mar 11 2010 CMD RPM Packagers <packages@commandprompt.com> - 8.4-2
- Rebuilt

* Wed Sep 3 2008 Devrim GUNDUZ <devrim@commandprompt.com> - 8.4-1
- 8.4 set

* Sat Jun 14 2008 Devrim GUNDUZ <devrim@commandprompt.com> - 8.3-5
- Fix srpm path.

* Sun Apr 13 2008 Devrim GUNDUZ <devrim@commandprompt.com> - 8.3-4
- Rebuilt

* Sun Apr 13 2008 Devrim GUNDUZ <devrim@commandprompt.com> - 8.3-3
- Enable srpms

* Tue Mar 11 2008 Devrim GUNDUZ <devrim@commandprompt.com> - 8.3-2
- Enable gpgcheck

* Mon Oct 8 2007 Devrim GUNDUZ <devrim@commandprompt.com> - 8.3-1
- Initial packaging for PostgreSQL Global Development Group RPMs
