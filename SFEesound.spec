#
# spec file for package SFEesound
#
# includes module(s): gnome-audio
#
# Copyright (c) 2004, 2010, Oracle and/or its affiliates. All rights reserved.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use esound_64 = esound.spec
%endif

%include base.inc
%use esound = esound.spec

Name:                    SUNWesound
IPS_package_name:        gnome/esound
Meta(info.classification): %{classification_prefix}:System/Multimedia Libraries
Summary:                 GNOME audio support framework
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
License:                 LGPL v2, , MIT, Sun Public Domain, binaries use GPL v2
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SUNWgnome-common-devel
BuildRequires: SUNWaudh
Requires: SUNWlibms

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%esound_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%base_arch
%esound.prep -d %name-%version/%base_arch

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%ifarch amd64 sparcv9
%esound_64.build -d %name-%version/%_arch64
%endif

%esound.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%esound_64.install -d %name-%version/%_arch64

rm $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*a
rm $RPM_BUILD_ROOT%{_prefix}/lib/esd
%endif

%esound.install -d %name-%version/%base_arch

rm $RPM_BUILD_ROOT%{_libdir}/lib*a
rm $RPM_BUILD_ROOT%{_bindir}/{esdfilt,esdloop}

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/esd
%ifarch amd64 sparcv9
%{_libdir}/%{_arch64}/lib*.so*
%endif
%{_libexecdir}/lib*.so*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files root
%defattr (0644, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/esd-config
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/esd-config
%endif
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%changelog
* Tue Dec 07 2010 - brian.cameron@oracle.com
- Created.
