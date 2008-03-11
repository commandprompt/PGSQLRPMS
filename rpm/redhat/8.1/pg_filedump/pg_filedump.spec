Summary:	PostgreSQL File Dump Utility
Name:		pg_filedump
Version:	8.1.0
Release:	1%{?dist}
URL:		http://sources.redhat.com/rhdb/
License:	GPLv2+
Group:		Applications/Databases
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	postgresql-devel >= 8.1

Source0:	http://sources.redhat.com/rhdb/tools/%{name}-%{version}.tar
Source1:	pg_crc.c
Patch1:		pg_filedump-make.patch

Obsoletes:	rhdb-utils => 8.1.0

%description
Display formatted contents of a PostgreSQL heap/index/control file.

%prep
%setup -q 

# We keep a copy of pg_crc.c in this SRPM so we don't need to have the
# full PostgreSQL sources at hand.
cp %{SOURCE1} pg_crc.c

%patch1 -p1

%build
export CFLAGS="$RPM_OPT_FLAGS"

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
install -m 755 pg_filedump %{buildroot}%{_bindir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/pg_filedump
%doc ChangeLog README.pg_filedump

%changelog
* Tue Mar 11 2008 Devrim GUNDUZ <devrim@commandprompt.com> 8.1.0-1
- Initial packaging for PGDG Repository, using the Fedora
  spec of Tom, with minor stylistic cleanup. Also, conflict
  with rhdb-utils.
