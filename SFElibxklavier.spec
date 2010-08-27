#
# spec file for package SFElibxklavier
#
# includes module(s): libxklavier
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%define owner sureshc
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%define _sysconfdir /etc/%{_arch64}
%use libxklavier_64 = libxklavier.spec
%endif

%include base.inc

%use libxklavier = libxklavier.spec

Name:                    SFElibxklavier
Summary:                 XKB utility library
Version:                 %{libxklavier.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgtk2
Requires: SUNWlibart
Requires: SUNWlibmsr
BuildRequires: SUNWlibm
BuildRequires: SUNWlibglade-devel
BuildRequires: SUNWlibart-devel
BuildRequires: SUNWgnome-common-devel

%package devel		
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SFElibxklavier

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n content
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64

%libxklavier_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libxklavier.prep -d %name-%version/%{base_arch}

cd %{_builddir}/%name-%version

%build
PKG_CONFIG_DISABLE_UNINSTALLED=
unset PKG_CONFIG_DISABLE_UNINSTALLED

%ifarch amd64 sparcv9
%libxklavier_64.build -d %name-%version/%_arch64
%endif

%libxklavier.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%libxklavier_64.install -d %name-%version/%_arch64
%endif

%libxklavier.install -d %name-%version/%{base_arch}

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc -d  %{base_arch} libxklavier-%{libxklavier.version}/README
%doc -d  %{base_arch} libxklavier-%{libxklavier.version}/AUTHORS
%doc(bzip2) -d  %{base_arch} libxklavier-%{libxklavier.version}/COPYING.LIB
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif
%dir %attr (0755, root, sys) %{_datadir}

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %dir %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif
%dir %attr (0755, root, sys) %dir %{_datadir}
%{_datadir}/gtk-doc

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %dir %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Thu Oct 08 2009 - suresh.chandrasekharan@sun.com
- 64-bit support
* Fri Sep 04 2009 - suresh.chandrasekharan@sun.com
- initial version
