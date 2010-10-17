#
# spec file for package SFEhowl
#
# includes module(s): howl
#
# # Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%use howl = howl.spec

Name:                    SFEhowl
Summary:                 howl - cross-platform implementation of Zeroconf
Version:                 %{howl.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnu-dbm
Requires: SUNWsqlite3
BuildRequires: SUNWsqlite3

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name


%prep
rm -rf %name-%version
mkdir %name-%version
%howl.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
export CC=gcc
export CXX=g++
export CXXFLAGS="%{gcc_cxx_optflags}"
export CFLAGS="%optflags"
export PKG_CONFIG_PATH="%{_cxx_libdir}/pkgconfig"
export LDFLAGS="-L%{_cxx_libdir} -R%{_cxx_libdir}"
export PERL_PATH=/usr/perl5/bin/perl
%howl.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%howl.install -d %name-%version


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/mDNS*
%dir %attr (0755, root, bin) %{_cxx_libdir}
%{_cxx_libdir}/lib*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/howl
%dir %attr (0755, root, bin) %{_libdir}
%attr (-, root, other) %{_libdir}/pkgconfig
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*


%changelog
* Fri Oct 01 2010 - jchoi42@pha.jhu.edu
- initial spec
