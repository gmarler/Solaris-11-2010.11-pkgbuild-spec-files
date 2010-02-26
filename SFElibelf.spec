#
# spec file for package SFElibelf
#
# includes module(s): libelf
#
# Copyright (c) 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include usr-gnu.inc

%define cc_is_gcc 1
%include base.inc
%use libelf = libelf.spec

Name:                SFElibelf
Summary:             libelf - A Library to Manipulate ELf Files
Version:             %{libelf.version}
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%libelf.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export CXXFLAGS="%{gcc_cxx_optflags}"
export PKG_CONFIG_PATH="%{_cxx_libdir}/pkgconfig"
export LDFLAGS="-L%{_cxx_libdir} -R%{_cxx_libdir}"
export PERL_PATH=/usr/perl5/bin/perl

%libelf.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%libelf.install -d %name-%version

rm $RPM_BUILD_ROOT/usr/gnu/lib/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/locale/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/libelf/*


%changelog
* Thu Feb 25 2010 - jchoi42@pha.jhu.edu
- Initial spec
