#
# spec file for packages SUNWmission-control
#
# includes module(s): mission-control
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: elaine
#
%include Solaris.inc

%use mission_control = telepathy-mission-control.spec

Name:                SUNWmission-control
Summary:             A telepathy mission control component
Version:             %{default_pkg_version}
SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires:       SUNWtelepathy-glib
BuildRequires:       SUNWtelepathy-glib-devel
BuildRequires:       SUNWlibtelepathy
BuildRequires:       SUNWlibtelepathy-devel

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires:            SUNWtelepathy-glib

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version
%mission_control.prep -d %name-%version

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export RPM_OPT_FLAGS="$CFLAGS"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
%mission_control.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%mission_control.install -d %name-%version

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_bindir}/*
%{_libdir}/lib*.so*
%{_libexecdir}/mission-control
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc/*/*/*
%{_datadir}/dbus-1/*
%doc(bzip2) telepathy-mission-control-%{mission_control.version}/COPYING
%doc(bzip2) telepathy-mission-control-%{mission_control.version}/NEWS
%doc(bzip2) telepathy-mission-control-%{mission_control.version}/ChangeLog
%doc telepathy-mission-control-%{mission_control.version}/AUTHORS
%doc telepathy-mission-control-%{mission_control.version}/README
%dir %attr (0755, root, other) %{_datadir}/doc

%files devel
%defattr(-, root, bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%dir %attr (0755, root, bin) %{_includedir}
%{_libdir}/pkgconfig/*.pc
%attr(755, root, root) %{_includedir}/libmcclient
%attr(755, root, root) %{_includedir}/libmissioncontrol
%attr(755, root, root) %{_includedir}/mission-control

%changelog
* Thu Mar 12 2009 - elaine.xiong@sun.com
- Move from spec-files/trunk.
* Fri Jan 16 2009 - christian.kelly@sun.com
- Un-commented lines in %prep.
* Wed Nov 05 2008 - rick.ju@sun.com
- Initial spec-file created
