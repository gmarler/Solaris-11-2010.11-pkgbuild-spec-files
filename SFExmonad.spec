#
# spec file for package SFExmonad 
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jchoi42
#

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%define ghc_version 6.10.4

Name:                    SFExmonad 
Summary:                 XMonad - a tiling window manager
Version:                 0.8.1
Release:                 1
License:                 BSD
Group:                   Window Manager
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
URL:                     http://www.xmonad.org/
Source:                  http://hackage.haskell.org/packages/archive/xmonad/%{version}/xmonad-%{version}.tar.gz
Source10:		 xmonad.desktop
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SFEgcc
Requires: SFEghc
Requires: SFEghc-xmonad
Requires: SUNWxorg-clientlibs
Requires: SUNWxorg-headers

%package prof
Summary:                 %{summary} - profiling libraries
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n xmonad-%version
export LD_LIBRARY_PATH=/usr/gnu/lib:$LD_LIBRARY_PATH

# Need to use same gcc as we used to build ghc (gcc 4.x)
export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++
export CXXFLAGS="%{gcc_cxx_optflags}"
export CFLAGS="%optflags"
export PKG_CONFIG_PATH="%{_cxx_libdir}/pkgconfig"
export LDFLAGS="-L%{_cxx_libdir} -R%{_cxx_libdir}"

runhaskell Setup.lhs configure --ghc --enable-library-profiling \
                --prefix='/usr' \
                --libdir=%{_cxx_libdir}/ghc-%{ghc_version}/

%build
export LD_LIBRARY_PATH=/usr/gnu/lib:$LD_LIBRARY_PATH

runhaskell Setup.lhs build

%install
export LD_LIBRARY_PATH=/usr/gnu/lib:$LD_LIBRARY_PATH
rm -rf $RPM_BUILD_ROOT

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# Generate the script to register the package with ghc-pkg
runhaskell Setup.lhs register --gen-script
#runhaskell Setup.lhs unregister --gen-script
cp register.sh $RPM_BUILD_ROOT%{_cxx_libdir}/ghc-%ghc_version/xmonad-%version/ghc-%{ghc_version}

# Prepare lists of files for packaging
#cd %{_builddir}/%name-%version
find $RPM_BUILD_ROOT -type f -name "*.p_hi" > pkg-prof.files
find $RPM_BUILD_ROOT -type f -name "*_p.a" >> pkg-prof.files
find $RPM_BUILD_ROOT/usr/lib -type f -name "*" > pkg-all.files
sort pkg-prof.files > pkg-prof-sort.files
sort pkg-all.files > pkg-all-sort.files
comm -23 pkg-all-sort.files pkg-prof-sort.files > pkg.files
# Clean up syntax for %files section
cat pkg.files | sed 's:'"$RPM_BUILD_ROOT"'::' > TEMP && mv TEMP xmonad.files
cat pkg-prof-sort.files | sed 's:'"$RPM_BUILD_ROOT"'::' > TEMP && mv TEMP xmonad-prof.files

# Add XMonad to gdm chooser list
mkdir -p $RPM_BUILD_ROOT%{_datadir}/xsessions
install -m 0644 %{SOURCE10} $RPM_BUILD_ROOT%{_datadir}/xsessions


%clean
rm -rf $RPM_BUILD_ROOT

%post
# The %install section above will only install files
# We need to register the package with ghc-pkg for ghc to find it
cd %{_cxx_libdir}/ghc-%{ghc_version}/xmonad-%version/ghc-%{ghc_version}
./register.sh

%preun
# Need to use --force or unregister will fail on any dependent ghc pkgs
# We presume SFE will maintain the dependencies from now
ghc-pkg unregister --force xmonad


%files -f xmonad.files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_bindir}
%{_bindir}/*
#%{_mandir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/xsessions
%{_datadir}/xsessions/*

%files prof -f xmonad-prof.files
%defattr (-, root, bin)

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Sun Sep 6 2009 - jchoi42@pha.jhu.edu
- Initial Solaris version
