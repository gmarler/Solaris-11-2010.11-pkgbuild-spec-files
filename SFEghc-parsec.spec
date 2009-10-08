#
# spec file for package SFEghc-parsec
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

# I'm unconvinced hundreds of SFEghc-mypkg.spec files would be nifty
# However, for the time being, this is needed to build xmobar

%define ver_par 3.0.1

%define ghc_version 6.10.4

Name:                    SFEghc-parsec 
Summary:                 ghc library bindings for parsec
Version:                 1.0
Release:                 1
License:                 BSD
Group:                   Development/Libraries/Haskell
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
URL:                     http://hackage.haskell.org/ghc
Source1:                 http://hackage.haskell.org/packages/archive/parsec/%{ver_par}/parsec-%{ver_par}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SFEghc
Requires: SFEghc-xmonad
BuildRequires: SUNWgzip
Requires: SUNWxorg-clientlibs
Requires: SUNWxorg-headers

%package prof
Summary:                 %{summary} - profiling libraries
sunw_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version

# Check which packages need to be installed 
%define install_par %(ghc-pkg list --simple-output parsec | grep -c parsec | grep -c 0)

export LD_LIBRARY_PATH=/usr/gnu/lib:$LD_LIBRARY_PATH
# Need to use same gcc as we used to build ghc (gcc 4.x)
export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++
export CXXFLAGS="%{gcc_cxx_optflags}"
export CFLAGS="%optflags"
export PKG_CONFIG_PATH="%{_cxx_libdir}/pkgconfig"
export LDFLAGS="-L%{_cxx_libdir} -R%{_cxx_libdir}"

# parsec
cd %{_builddir}/%name-%version
/usr/bin/gunzip < %SOURCE1 | tar xvf -
cd %{_builddir}/%name-%version/parsec-%ver_par
runhaskell Setup.hs configure --ghc --enable-library-profiling \
                --prefix='/usr' \
                --libdir=%{_cxx_libdir}/ghc-%{ghc_version}/

%build
export LD_LIBRARY_PATH=/usr/gnu/lib:$LD_LIBRARY_PATH

# parsec
cd %{_builddir}/%name-%version/parsec-%ver_par
runhaskell Setup.hs build


%install
export LD_LIBRARY_PATH=/usr/gnu/lib:$LD_LIBRARY_PATH
rm -rf $RPM_BUILD_ROOT

# parsec   
cd %{_builddir}/%name-%version/parsec-%ver_par
# Install files
runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT
rm -r $RPM_BUILD_ROOT%{_datadir}
# Generate the script to register the package with ghc-pkg
runhaskell Setup.hs register --gen-script
#runhaskell Setup.hs unregister --gen-script
cp register.sh $RPM_BUILD_ROOT%{_cxx_libdir}/ghc-%ghc_version/parsec-%{ver_par}/ghc-%{ghc_version}


# Prepare lists of files for packaging
cd %{_builddir}/%name-%version
find $RPM_BUILD_ROOT -type f -name "*.p_hi" > ghc-extra-prof.files
find $RPM_BUILD_ROOT -type f -name "*_p.a" >> ghc-extra-prof.files
find $RPM_BUILD_ROOT/usr/lib -type f -name "*" > ghc-extra-all.files
sort ghc-extra-prof.files > ghc-extra-prof-sort.files
sort ghc-extra-all.files > ghc-extra-all-sort.files
comm -23 ghc-extra-all-sort.files ghc-extra-prof-sort.files > ghc-extra.files
# Clean up syntax for %files section
cat ghc-extra.files | sed 's:'"$RPM_BUILD_ROOT"'::' > TEMP && mv TEMP ghc-extra.files
cat ghc-extra-prof-sort.files | sed 's:'"$RPM_BUILD_ROOT"'::' > TEMP && mv TEMP ghc-extra-prof.files


%clean
rm -rf $RPM_BUILD_ROOT

%post
# The %install section above will only install files
# We need to register the package with ghc-pkg for ghc to find it
cd %{_cxx_libdir}/ghc-%{ghc_version}/parsec-%{ver_par}/ghc-%{ghc_version}
./register.sh

%preun
# Need to use --force or unregister will fail on any dependent ghc pkgs 
# We presume SFE will maintain the dependencies from now
ghc-pkg unregister --force parsec

%files -f ghc-extra.files
%defattr (-, root, bin)

%files prof -f ghc-extra-prof.files
%defattr (-, root, bin)

%changelog
* Thu Oct 08 2009 - jchoi42@pha.jhu.edu
- Initial spec
