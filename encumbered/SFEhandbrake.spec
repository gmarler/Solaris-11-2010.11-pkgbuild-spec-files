#
# spec file for package SFEhandbrake
#
# includes module(s): handbrake
#
# Copyright 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%use handbrake = handbrake.spec

Name:                    SFEhandbrake
Summary:                 handbrake - multiplatform, multithreaded video transcoder
Version:                 %{handbrake.version}

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEgcc
Requires: SFEfaad2
Requires: SFElibx264
Requires: SFElibmad
Requires: SFElibao
Requires: SFExvid
Requires: SFEffmpeg
Requires: SFElibmp4v2
Requires: SFElibdvdnav
Requires: SFElibiconv
Requires: SFESFElibmikmod
Requires: SFElibschroedinger
BuildRequires: SFEgcc
BuildRequires: SFEffmpeg-devel
BuildRequires: SFElibx264-devel
BuildRequires: SFElibao-devel
BuildRequires: SFElibiconv-devel
# TODO: more dependencies?

%prep
rm -rf %name-%version
mkdir %name-%version
%handbrake.prep -d %name-%version

%build
export CC='gcc'
export CXX=g++
export CFLAGS="%gcc_optflags -Os -Xlinker -i"
export LDFLAGS="-L%{_cxx_libdir} -R%{_cxx_libdir} -lsocket -lnsl %_ldflags %{xorg_lib_path} -L/usr/gnu/lib -R/usr/gnu/lib -L%{_libdir} -R%{_libdir}i -m64"
export CXXFLAGS="%gcc_cxx_optflags"
export PKG_CONFIG_PATH="%{_cxx_libdir}/pkgconfig"
%handbrake.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%handbrake.install -d %name-%version


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_bindir}
%{_bindir}/HandBrakeCLI


%changelog
* Wed Dec 16 2010 - jchoi42@pha.jhu.edu
- initial spec
