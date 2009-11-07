#
# spec file for package SFEglibmm-gpp
#
# includes module(s): glibmm
#
# # Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%use glibmm = glibmm.spec

Name:                    SFEglibmm-gpp
Summary:                 glibmm - C++ Wrapper for the Glib2 Library (g++-built)
Version:                 %{glibmm.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
Requires: SFEsigcpp-gpp
BuildRequires: SFEsigcpp-gpp-devel
BuildRequires: SUNWsigcpp-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-base-libs-devel
Requires: SFEsigcpp-gpp-devel
Requires: SUNWsigcpp-devel

%prep
rm -rf %name-%version
mkdir %name-%version
%glibmm.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++
export CXXFLAGS="%{gcc_cxx_optflags}"
export CFLAGS="%optflags"
export PKG_CONFIG_PATH="%{_cxx_libdir}/pkgconfig"
export LDFLAGS="-L%{_cxx_libdir} -R%{_cxx_libdir}"
export PERL_PATH=/usr/perl5/bin/perl
%glibmm.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%glibmm.install -d %name-%version
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

# Remove useless m4, pm and extra_gen_defs files 
rm -rf $RPM_BUILD_ROOT%{_cxx_libdir}/glibmm-2.4/proc/m4
rm -rf $RPM_BUILD_ROOT%{_cxx_libdir}/glibmm-2.4/proc/pm
rm -rf $RPM_BUILD_ROOT%{_cxx_libdir}/libglibmm_generate_extra_defs*.so*
rm -rf $RPM_BUILD_ROOT%{_cxx_includedir}/glibmm-2.4/glibmm_generate_extra_defs

# REMOVE l10n FILES - included in Solaris
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale

# remove files included in SUNWglibmm-devel:
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
%{_cxx_libdir}/glibmm*
%{_cxx_libdir}/giomm*

%changelog
* Fri Nov 06 2009 - jchoi42@pha.jhu.edu
- comment depreciated patch
* Fri Sep 25 2009 - jchoi42@pha.jhu.edu
- specified giomm dir in %files section
* Sun Jun 29 2008 - river@wikimedia.org
- force to use gcc in /usr/sfw, not /usr/gnu
* Wed Apr 23 2008 - laca@sun.com
- create, re-work from SUNWglibmm.spec to build with g++
