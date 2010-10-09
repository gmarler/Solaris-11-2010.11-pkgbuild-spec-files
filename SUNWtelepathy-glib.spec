#
# spec file for packages SUNWtelepathy-glib
#
# includes module(s): telepathy-glib
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jefftsai
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use telepathy_glib64 = telepathy-glib.spec
%endif

%include base.inc
%use telepathy_glib = telepathy-glib.spec

Name:                    SUNWtelepathy-glib
Summary:                 A GLib-based helper library for clients and connection managers
Version:                 %{telepathy_glib.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
#Requires: 

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
%ifarch amd64 sparcv9
mkdir -p %name-%version/%_arch64
%telepathy_glib64.prep -d %name-%version/%_arch64
%endif

mkdir -p %name-%version/%base_arch
%telepathy_glib.prep -d %name-%version/%base_arch

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export RPM_OPT_FLAGS="$CFLAGS"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"

%ifarch amd64 sparcv9
%telepathy_glib64.build -d %name-%version/%_arch64
%endif
    
%telepathy_glib.build -d %name-%version/%base_arch


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%telepathy_glib64.install  -d %name-%version/%_arch64
%endif
    
%telepathy_glib.install -d %name-%version/%base_arch

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%ifarch amd64 sparcv9
%{_libdir}/%{_arch64}/lib*.so*
%endif
%{_libdir}/lib*.so*
%{_datadir}/gtk-doc/*/*/*
%doc(bzip2) -d %{base_arch}/telepathy-glib-%{telepathy_glib.version} COPYING 
%doc(bzip2) -d %{base_arch}/telepathy-glib-%{telepathy_glib.version} NEWS
%doc(bzip2) -d %{base_arch}/telepathy-glib-%{telepathy_glib.version} ChangeLog
%doc(bzip2) -d %{base_arch}/telepathy-glib-%{telepathy_glib.version} AUTHORS
%doc(bzip2) -d %{base_arch}/telepathy-glib-%{telepathy_glib.version} README
%dir %attr (0755, root, other) %{_datadir}/doc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%dir %attr (0755, root, bin) %{_includedir}
%{_libdir}/pkgconfig/*.pc
%ifarch sparcv9 amd64
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%attr(755, root, bin) %{_includedir}/telepathy-1.0/*

%changelog
* Oct 9 2010 - jeff.cai@oracle.com
- Not ship /usr/lib/gir-repository
* Thu Mar 12 2009 - elaine.xiong@sun.com
- Move from spec-fies/trunk
* Wed Nov 05 2008 - rick.ju@sun.com
- Initial spec-file created
