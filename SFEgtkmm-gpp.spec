#
#
# spec file for package SFEgtkmm-gpp
#
# includes module(s): gtkmm
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%use gtkmm = gtkmm.spec

Name:                    SFEgtkmm-gpp
Summary:                 gtkmm - C++ Wrapper for the Gtk+ Library (g++-built)
Version:                 %{gtkmm.version}

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEglibmm-gpp
Requires: SFEcairomm-gpp
Requires: SUNWgnome-base-libs
Requires: SUNWlibms
Requires: SFEsigcpp-gpp
Requires: SUNWlibC
Requires: SUNWgccruntime
BuildRequires: SUNWsigcpp-devel
BuildRequires: SUNWglibmm-devel
BuildRequires: SUNWcairomm-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SFEsigcpp-gpp-devel
BuildRequires: SFEglibmm-gpp-devel
BuildRequires: SFEcairomm-gpp-devel

%package devel
Summary:                 gtkmm - C++ Wrapper for the Gtk+ Library - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-base-libs-devel
Requires: SFEglibmm-gpp-devel
Requires: SFEsigcpp-gpp-devel
Requires: SFEcairomm-gpp-devel
Requires: SUNWglibmm-devel
Requires: SUNWcairomm-devel
Requires: SUNWsigcpp-devel


%prep
rm -rf %name-%version
mkdir %name-%version
%gtkmm.prep -d %name-%version

%build
export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export LDFLAGS="-L%{_cxx_libdir} -R%{_cxx_libdir}"
export CXXFLAGS="%gcc_cxx_optflags -D_XPG4_2 -D__EXTENSIONS__"
export PKG_CONFIG_PATH="%{_cxx_libdir}/pkgconfig"
%gtkmm.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gtkmm.install -d %name-%version

# Move demo to demo directory
#
install -d $RPM_BUILD_ROOT%{_prefix}/demo/jds/bin
mv $RPM_BUILD_ROOT%{_bindir}/gtkmm-demo \
    $RPM_BUILD_ROOT%{_prefix}/demo/jds/bin/gtkmm-gpp-demo
rm -r $RPM_BUILD_ROOT%{_bindir}

# delete files already included in SUNWgtkmm-devel:
rm -r $RPM_BUILD_ROOT%{_datadir}
rm -r $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_cxx_libdir}
%{_cxx_libdir}/lib*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_cxx_libdir}
%dir %attr (0755, root, other) %{_cxx_libdir}/pkgconfig
%{_cxx_libdir}/pkgconfig/*
%{_cxx_libdir}/gtkmm*
%{_cxx_libdir}/gdkmm*
%dir %attr (0755, root, bin) %{_prefix}/demo
%dir %attr (0755, root, bin) %{_prefix}/demo/jds
%dir %attr (0755, root, bin) %{_prefix}/demo/jds/bin
%{_prefix}/demo/jds/bin/gtkmm-gpp-demo


%changelog
* Thu Oct 4 2009 - jchoi42@pha.jhu.edu
- added SFEpango dependency 
* Wed Apr 23 2008 - laca@sun.com
- create, re-work from SUNWgtkmm.spec to build with g++
