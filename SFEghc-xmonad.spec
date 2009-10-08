#
# spec file for package SFEghc-xmonad 
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

# This is by no means a comprehensive list of all ghc lib bindings
# I'm unconvinced hundreds of SFEghc-mypkg.spec files would be nifty
# So, for the time being, these are libraries needed to build xmonad+xmobar

%define ver_x11 1.4.5
%define ver_mtl 1.1.0.2
# needed for xmobar
#%define ver_par 3.0.1
%define ver_stm 2.1.1.2
%define ver_utf 0.3.5

%define ghc_version 6.10.4

Name:                    SFEghc-xmonad 
Summary:                 extra ghc library bindings
Version:                 1.0
Release:                 1
License:                 BSD
Group:                   Development/Libraries/Haskell
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
URL:                     http://hackage.haskell.org/ghc
Source0:                 http://hackage.haskell.org/packages/archive/X11/%{ver_x11}/X11-%{ver_x11}.tar.gz
Source1:                 http://hackage.haskell.org/packages/archive/mtl/%{ver_mtl}/mtl-%{ver_mtl}.tar.gz
#Source2:                 http://hackage.haskell.org/packages/archive/parsec/%{ver_par}/parsec-%{ver_par}.tar.gz
Source3:                 http://hackage.haskell.org/packages/archive/stm/%{ver_stm}/stm-%{ver_stm}.tar.gz
Source4:                 http://hackage.haskell.org/packages/archive/utf8-string/%{ver_utf}/utf8-string-%{ver_utf}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SFEghc
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
%define install_x11 %(ghc-pkg list --simple-output X11 | grep -c X11 | grep -c 0)
%define install_mtl %(ghc-pkg list --simple-output mtl | grep -c mtl | grep -c 0)

export LD_LIBRARY_PATH=/usr/gnu/lib:$LD_LIBRARY_PATH
# Need to use same gcc as we used to build ghc (gcc 4.x)
export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++
export CXXFLAGS="%{gcc_cxx_optflags}"
export CFLAGS="%optflags"
export PKG_CONFIG_PATH="%{_cxx_libdir}/pkgconfig"
export LDFLAGS="-L%{_cxx_libdir} -R%{_cxx_libdir}"

# X11
cd %{_builddir}/%name-%version
/usr/bin/gunzip < %SOURCE0 | tar xvf -
cd %{_builddir}/%name-%version/X11-%ver_x11
runhaskell Setup.hs configure --ghc --enable-library-profiling \
                --prefix='/usr' \
                --libdir=%{_cxx_libdir}/ghc-%{ghc_version}/

# mtl 
cd %{_builddir}/%name-%version
/usr/bin/gunzip < %SOURCE1 | tar xvf -
cd %{_builddir}/%name-%version/mtl-%ver_mtl
runhaskell Setup.hs configure --ghc --enable-library-profiling \
                --prefix='/usr' \
                --libdir=%{_cxx_libdir}/ghc-%{ghc_version}/

# stm 
cd %{_builddir}/%name-%version
/usr/bin/gunzip < %SOURCE3 | tar xvf -
cd %{_builddir}/%name-%version/stm-%ver_stm
runhaskell Setup.hs configure --ghc --enable-library-profiling \
                --prefix='/usr' \
                --libdir=%{_cxx_libdir}/ghc-%{ghc_version}/

# utf8-string
cd %{_builddir}/%name-%version
/usr/bin/gunzip < %SOURCE4 | tar xvf -
cd %{_builddir}/%name-%version/utf8-string-%ver_utf
runhaskell Setup.lhs configure --ghc --enable-library-profiling \
                --prefix='/usr' \
                --libdir=%{_cxx_libdir}/ghc-%{ghc_version}/


%build
export LD_LIBRARY_PATH=/usr/gnu/lib:$LD_LIBRARY_PATH

# X11
cd %{_builddir}/%name-%version/X11-%ver_x11
runhaskell Setup.hs build

# mtl
cd %{_builddir}/%name-%version/mtl-%ver_mtl
runhaskell Setup.hs build

# stm
cd %{_builddir}/%name-%version/stm-%ver_stm
runhaskell Setup.hs build

# utf8-string
cd %{_builddir}/%name-%version/utf8-string-%ver_utf
runhaskell Setup.lhs build


%install
export LD_LIBRARY_PATH=/usr/gnu/lib:$LD_LIBRARY_PATH
rm -rf $RPM_BUILD_ROOT

# X11
cd %{_builddir}/%name-%version/X11-%ver_x11
# Install files
runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT
rm -r $RPM_BUILD_ROOT%{_datadir}
# Generate the script to register the package with ghc-pkg
runhaskell Setup.hs register --gen-script
#runhaskell Setup.hs unregister --gen-script
cp register.sh $RPM_BUILD_ROOT%{_cxx_libdir}/ghc-%ghc_version/X11-%{ver_x11}/ghc-%{ghc_version}

# mtl   
cd %{_builddir}/%name-%version/mtl-%ver_mtl
# Install files
runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT
rm -r $RPM_BUILD_ROOT%{_datadir}
# Generate the script to register the package with ghc-pkg
runhaskell Setup.hs register --gen-script
#runhaskell Setup.hs unregister --gen-script
cp register.sh $RPM_BUILD_ROOT%{_cxx_libdir}/ghc-%ghc_version/mtl-%{ver_mtl}/ghc-%{ghc_version}

# PARSEC DEPN ON MTL
# parsec   

# stm   
cd %{_builddir}/%name-%version/stm-%ver_stm
# Install files
runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT
rm -r $RPM_BUILD_ROOT%{_datadir}
# Generate the script to register the package with ghc-pkg
runhaskell Setup.hs register --gen-script
#runhaskell Setup.hs unregister --gen-script
cp register.sh $RPM_BUILD_ROOT%{_cxx_libdir}/ghc-%ghc_version/stm-%{ver_stm}/ghc-%{ghc_version}

# utf8-string
cd %{_builddir}/%name-%version/utf8-string-%ver_utf
# Install files
runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT
rm -r $RPM_BUILD_ROOT%{_datadir}
# Generate the script to register the package with ghc-pkg
runhaskell Setup.lhs register --gen-script
#runhaskell Setup.lhs unregister --gen-script
cp register.sh $RPM_BUILD_ROOT%{_cxx_libdir}/ghc-%ghc_version/utf8-string-%{ver_utf}/ghc-%{ghc_version}


# Prepare lists of files for packaging
cd %{_builddir}/%name-%version
#touch ghc-extra.files ghc-extra-prof.files ghc-extra-all.files
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
cd %{_cxx_libdir}/ghc-%{ghc_version}/X11-%{ver_x11}/ghc-%{ghc_version}
./register.sh
cd %{_cxx_libdir}/ghc-%{ghc_version}/mtl-%{ver_mtl}/ghc-%{ghc_version}
./register.sh
cd %{_cxx_libdir}/ghc-%{ghc_version}/stm-%{ver_stm}/ghc-%{ghc_version}
./register.sh
cd %{_cxx_libdir}/ghc-%{ghc_version}/utf8-string-%{ver_utf}/ghc-%{ghc_version}
./register.sh

%preun
# Need to use --force or unregister will fail on any dependent ghc pkgs 
# We presume SFE will maintain the dependencies from now
ghc-pkg unregister --force X11
ghc-pkg unregister --force mtl
ghc-pkg unregister --force stm
ghc-pkg unregister --force utf8-string

%files -f ghc-extra.files
%defattr (-, root, bin)

%files prof -f ghc-extra-prof.files
%defattr (-, root, bin)

%changelog
* Sun Sep 6 2009 - jchoi42@pha.jhu.edu
- Initial spec
