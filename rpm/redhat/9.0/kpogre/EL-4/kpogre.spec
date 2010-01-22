Summary:	PostgreSQL graphical frontend for KDE 3.x
Name:		kpogre
Version:	1.5.4
Release:	2%{?dist}
License:	GPL
Url:		http://kpogre.sourceforge.net
Group:		Applications/Databases
Source:		http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:		kpogre-docmakefile.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	libpqxx >= 2.6.8 postgresql-libs >= 7.4 qt >= 3.0
BuildRequires:	libpqxx-devel >= 2.6.8 kdelibs >= 3.0 postgresql >= 7.4 , kdelibs-devel => 3.0
BuildRequires:	qt-devel >= 3.0

%description
KPoGre is graphical administration tool for PostgreSQL. 
It uses libpqxx library.

%ifarch ia64 x86_64
  %define rcopts --with-extra-includes="%{_includedir}/pqxx -I %{_includedir}/pgsql" --enable-libsuffix=64 --with-extra-lib=%{_libdir}
%else
  %define rcopts --with-extra-includes="%{_includedir}/pqxx -I %{_includedir}/pgsql" --with-extra-lib=%{_libdir}
%endif

%prep
%setup -q
%patch0 -p0

%configure %{rcopts} --disable-rpath

%build
make %{?smp_flags }

%install
rm -rf %{buildroot}
make %{?smp_flags} install-strip DESTDIR=%{buildroot}

cd %{buildroot}
find . -type d | sed '1,2d;s,^\.,\%attr(-\,root\,root) \%dir ,' > $RPM_BUILD_DIR/file.list.kpogre
find . -type f | sed 's,^\.,\%attr(-\,root\,root) ,' >> $RPM_BUILD_DIR/file.list.kpogre
find . -type l | sed 's,^\.,\%attr(-\,root\,root) ,' >> $RPM_BUILD_DIR/file.list.kpogre

%clean
rm -rf %{buildroot}

%files 
%dir %{_datadir}/apps/kpogre
%dir %{_datadir}/doc/HTML/en/kpogre
%{_datadir}/apps/kpogre/*
%{_datadir}/apps/kpogre/pics/schema_unl.png
%{_datadir}/doc/HTML/en/kpogre/*
%{_datadir}/applnk/Applications/kpogre.desktop
%{_datadir}/icons/hicolor/16x16/apps/kpogre.png
%{_datadir}/icons/hicolor/32x32/apps/kpogre.png
%{_bindir}/kpogre

%changelog
* Wed Aug 29 2007 Devrim GUNDUZ <devrim@CommandPrompt.com> 1.5.4-2
- Fix some ownership problems
- Added a patch to surpress rpmlint warning

* Sun Aug 12 2007 Devrim GUNDUZ <devrim@CommandPrompt.com> 1.5.4-1
- Initial packaging for Fedora. Spec file is based on
  the spec which is shipped with the kpogre tarball.

#W: kpogre symlink-should-be-relative /usr/share/doc/HTML/en/kpogre/common /usr/share/doc/HTML/en/common
#Absolute symlinks are problematic eg. when working with chroot environments.

