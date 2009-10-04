#
#
# spec file for package SFEpangomm-gpp
#
# includes module(s): pangomm
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%use pangomm = pangomm.spec

Name:                    SFEpangomm-gpp
Summary:                 pangomm - C++ Wrapper for the pango Library (g++ built)
Version:                 %{pangomm.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWpango
Requires: SUNWpangomm
Requires: SFEsigcpp-gpp
Requires: SUNWcairomm
Requires: SFEglibmm-gpp
BuildRequires: SUNWpango-devel
BuildRequires: SUNWpangomm-devel
BuildRequires: SFEsigcpp-gpp-devel
BuildRequires: SUNWcairomm-devel
BuildRequires: SFEglibmm-gpp-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWpangomm-devel
Requires: SFEsigcpp-gpp-devel

%prep
rm -rf %name-%version
mkdir %name-%version
%pangomm.prep -d %name-%version
#cd %{_builddir}/%name-%version
#gzcat %SOURCE0 | tar -xf -

%build
export CC=gcc
export CXX=g++
#export CC=/usr/sfw/bin/gcc
#export CXX=/usr/sfw/bin/g++
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="-L%{_cxx_libdir} -R%{_cxx_libdir}"
export CXXFLAGS="%gcc_cxx_optflags -D_XPG4_2 -D__EXTENSIONS__"
export PKG_CONFIG_PATH="%{_cxx_libdir}/pkgconfig"

#libtoolize --f
%pangomm.build -d %name-%version

%install
%pangomm.install -d %name-%version

# delete files already included in SUNWpangomm-devel:
rm -r $RPM_BUILD_ROOT%{_datadir}
rm -r $RPM_BUILD_ROOT%{_includedir}

# Remove useless m4, pm and extra_gen_defs files 
rm -rf $RPM_BUILD_ROOT%{_cxx_libdir}/pangomm-1.4/proc/m4*
rm -rf $RPM_BUILD_ROOT%{_cxx_libdir}/g++//pangomm-1.4/proc/m4*

#rm -rf $RPM_BUILD_ROOT%{_libdir}/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_cxx_libdir}
%{_cxx_libdir}/lib*
#%dir %attr(0755, root, bin) %{_mandir}
#%{_mandir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_cxx_libdir}
%dir %attr (0755, root, other) %{_cxx_libdir}/pkgconfig
%{_cxx_libdir}/pkgconfig/*
%{_cxx_libdir}/pangomm*

%changelog
* Wed Sep 23 2009 - jchoi42@pha.jhu.edu
- Intially reworked from SUNWpangomm to build w gcc

