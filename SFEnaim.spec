#
# spec file for package SFEnaim
#
# Copyright 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jchoi42
#

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

Name:                    SFEnaim
Summary:                 naim - A console AIM, ICQ, IRC, and Lily CMC client
Version:                 0.11.8.3.2
Release:                 1
License:                 GPL
Group:                   Applications/Multimedia
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
URL:                     http://naim.n.ml.org
Source:                  http://naim.googlecode.com/files/naim-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SFEncurses
Requires: SFEgettext
BuildRequires: SUNWncurses-devel
BuildRequires: SFEncurses-devel


%prep
%setup -q -n naim-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc
export CXX=g++
export CXXFLAGS="%{gcc_cxx_optflags}"
export CFLAGS="%optflags"
export CPPFLAGS="-I/usr/include/ncurses -I/usr/gnu/include"
export PKG_CONFIG_PATH="%{_cxx_libdir}/pkgconfig"
export LDFLAGS="-L%{_cxx_libdir} -R%{_cxx_libdir}"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_cxx_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}
#make -j$CPUS 
# parallel build is currently not fully functional
# http://code.google.com/p/naim/issues/detail?id=11
make -j1


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# libs appear to not exist/build
rm -rf $RPM_BUILD_ROOT/usr/lib


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_bindir}
%{_bindir}/*
%{_mandir}/*
#%dir %attr (0755, root, bin) %{_cxx_libdir}
#%{_cxx_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/doc
%dir %attr(0755, root, bin) %{_includedir}
%{_includedir}/*


%changelog
* Sat May 08 2010 - jchoi42@pha.jhu.edu
- initial spec
