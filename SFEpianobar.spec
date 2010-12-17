#
#
# spec file for package SFEpianobar
#
# includes module(s): pianobar
#
# Copyright 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%use pianobar = pianobar.spec

Name:                    SFEpianobar
Summary:                 pianobar - console client for Pandora web radio
Version:                 %{pianobar.version}

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFElibfaad
Requires: SFElibmad
Requires: SFElibao
BuildRequires: SFElibao-devel


%prep
rm -rf %name-%version
mkdir %name-%version
%pianobar.prep -d %name-%version

%build
export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export LDFLAGS="-L%{_cxx_libdir} -R%{_cxx_libdir} -lsocket -lnsl"
export CXXFLAGS="%gcc_cxx_optflags"
export PKG_CONFIG_PATH="%{_cxx_libdir}/pkgconfig"
%pianobar.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%pianobar.install -d %name-%version


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}/man1/*


%changelog
* Wed Dec 16 2010 - jchoi42@pha.jhu.edu
- initial spec
