#
# spec file for packages SUNWlibtelepathy
#
# includes module(s): libtelepathy
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: elaine
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use libtelepathy64 = libtelepathy.spec
%endif

%include base.inc
%use libtelepathy= libtelepathy.spec

Name:                    SUNWlibtelepathy
Summary:                 A GLib library to ease writing Telepathy clients in glib
Version:                 %{libtelepathy.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:            SUNWtelepathy-glib
BuildRequires:       SUNWtelepathy-glib-devel

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
%ifarch amd64 sparcv9
mkdir -p %name-%version/%_arch64
%libtelepathy64.prep -d %name-%version/%_arch64
%endif
    
mkdir -p %name-%version/%base_arch
%libtelepathy.prep -d %name-%version/%base_arch


%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export RPM_OPT_FLAGS="$CFLAGS"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"

%ifarch amd64 sparcv9
%libtelepathy64.build -d %name-%version/%_arch64
%endif
    
%libtelepathy.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%libtelepathy64.install  -d %name-%version/%_arch64
%endif
    
%libtelepathy.install -d %name-%version/%base_arch

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%ifarch amd64 sparcv9
%{_libdir}/%{_arch64}/lib*.so*
%endif
%{_libdir}/lib*.so*
%doc(bzip2) -d %{base_arch}/libtelepathy-%{libtelepathy.version} COPYING
%doc(bzip2) -d %{base_arch}/libtelepathy-%{libtelepathy.version} NEWS
%doc(bzip2) -d %{base_arch}/libtelepathy-%{libtelepathy.version} ChangeLog
%doc -d %{base_arch}/libtelepathy-%{libtelepathy.version} AUTHORS README
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc

%files devel
%defattr(-, root, bin)
%ifarch sparcv9 amd64
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%dir %attr (0755, root, bin) %{_includedir}
%{_libdir}/pkgconfig/*.pc
%attr(755, root, root) %{_includedir}/telepathy-1.0/*

%changelog
* Oct 09 2010 - jeff.cai@oracle.com
- Add support for 64 bit.
* Thu Mar 12 2009 - elaine.xiong@sun.com
- Move from spec-files/trunk.
* Wed Nov 05 2008 - rick.ju@sun.com
- Initial spec-file created
