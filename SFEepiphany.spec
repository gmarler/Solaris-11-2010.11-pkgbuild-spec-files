#
# spec file for package SFEepiphany
#
# includes module(s): epiphany
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: gheet
#
%include Solaris.inc

%use epiphany = epiphany.spec

%define revision = %{epiphany.revision}

Name:                    SFEepiphany
Summary:                 GNOME web browser - epiphany
Version:                 %{epiphany.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-base-libs
Requires: SUNWfirefox
Requires: SUNWdbus
Requires: SUNWlibmsr
Requires: SUNWprd
Requires: SFEwebkit
Requires: SUNWgnome-gvfs
Requires: SFEgconfmm
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWdbus-devel
BuildRequires: SUNWfirefox-devel
BuildRequires: SUNWprd
BuildRequires: SFEwebkit-devel
BuildRequires: SFEgconfmm-devel

%package devel
Summary:         %{summary} - development files
SUNW_BaseDir:    %{_basedir}
%include default-depend.inc
Requires: %name

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%epiphany.prep -d %name-%version

%build
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags"
export PKG_CONFIG_PATH=%{_datadir}/pkgconfig:%{_pkg_config_path}
%if %option_with_gnu_iconv
export CFLAGS="$CFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl"
export CXXFLAGS="$CXXFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl"
%endif
%epiphany.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%epiphany.install -d %name-%version
#rm $RPM_BUILD_ROOT%{_cxx_libdir}/*.la

# Remove useless aclocal and m4 definitions
rm -rf $RPM_BUILD_ROOT%{_datadir}/aclocal*

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (-, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/epiphany
%{_datadir}/epiphany/*
%dir %attr (-, root, bin) %{_datadir}/dbus-1
%{_datadir}/dbus-1/*
%dir %attr (-, root, other) %{_datadir}/gnome
%{_datadir}/gnome/*
%dir %attr (-, root, other) %{_datadir}/icons
#%{_datadir}/icons/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16/apps
%{_datadir}/icons/hicolor/16x16/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22/apps
%{_datadir}/icons/hicolor/22x22/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24/apps
%{_datadir}/icons/hicolor/24x24/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32/apps
%{_datadir}/icons/hicolor/32x32/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/48x48/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable/apps
%{_datadir}/icons/hicolor/scalable/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/LowContrastLargePrint
%dir %attr (-, root, other) %{_datadir}/icons/LowContrastLargePrint/48x48
%dir %attr (-, root, other) %{_datadir}/icons/LowContrastLargePrint/48x48/apps
%{_datadir}/icons/LowContrastLargePrint/48x48/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/HighContrastLargePrint
%dir %attr (-, root, other) %{_datadir}/icons/HighContrastLargePrint/48x48
%dir %attr (-, root, other) %{_datadir}/icons/HighContrastLargePrint/48x48/apps
%{_datadir}/icons/HighContrastLargePrint/48x48/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/HighContrastLargePrintInverse
%dir %attr (-, root, other) %{_datadir}/icons/HighContrastLargePrintInverse/48x48
%dir %attr (-, root, other) %{_datadir}/icons/HighContrastLargePrintInverse/48x48/apps
%{_datadir}/icons/HighContrastLargePrintInverse/48x48/apps/*

%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/epiphany/2.28/epiphany/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_cxx_libdir}
%dir %attr (0755, root, other) %{_cxx_libdir}/pkgconfig
%{_cxx_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (-, root, bin) %{_datadir}/gtk-doc
%{_datadir}/gtk-doc/*
%dir %attr (-, root, other) %{_datadir}/locale
#%attr (-, root, other) %{_datadir}/locale
%{_datadir}/locale/[a-z]*/LC_MESSAGES/*
%dir %attr (0755, root, bin) %{_datadir}/omf
%{_datadir}/omf/*
%dir %attr (0755, root, bin) %{_datadir}/man
%{_datadir}/man/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/epiphany*


%changelog
* Fri Feb 12 2010 - jchoi42@pha.jhu.edu
- add devel pkg
- update %files for new filenames, add %revision, remove gvfs module
- add dependencies to gvfs, webkit, update install to gpp-built libdir 
* Thu Nov 07 2007 - damien.carbery@sun.com
- Initial version.
