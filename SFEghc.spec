#
# spec file for package SFEghc 
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jchoi42
#

%include Solaris.inc

%define cc_is_gcc 1
%define bootstrap 6.10.4
%include base.inc

# WARNING: you need a lot of diskspace to build this spec!

Name:                    SFEghc 
Summary:                 ghc - The Glasglow Haskell Compiler (g++-built)
Version:                 6.10.4 
Release:                 1
License:                 BSD
Group:                   Development/Languages/Haskell
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
URL:                     http://www.haskell.org/ghc
Source:                  http://www.haskell.org/ghc/dist/%{version}/ghc-%{version}-src.tar.bz2
Source1:                 http://www.haskell.org/ghc/dist/%bootstrap/maeder/ghc-%bootstrap-i386-unknown-solaris2.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SFEgcc
Requires: SUNWgnu-mpfr
Requires: SUNWgnu-mp
BuildRequires: SUNWgtar
BuildRequires: SUNWesu
Requires: SUNWreadline
#Requires: SFEreadline
BuildRequires: SFEncurses
BuildRequires: SUNWncurses

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
rm -rf %name-%version
mkdir %name-%version
cd %name-%version
# ghc requires ghc to compile ghc omg
# bootstrap from prebuilt ghc (version %bootstrap)
mkdir prebuilt
cd prebuilt
# need to use gnu tar to deal with filenames >100ch
/usr/gnu/bin/tar -xjf %SOURCE1
cd ghc-%version
mkdir %{_builddir}/%name-%version/postbuilt
./configure CC=gcc CXX=g++ --prefix=%{_builddir}/%name-%version/postbuilt
gmake install


%build
cd %{_builddir}/%name-%version
/usr/gnu/bin/tar -xjf %SOURCE0
export PATH=%{_builddir}/%name-%version/postbuilt/bin/:$PATH
export LD_LIBRARY_PATH=%{_builddir}/%name-%version/postbuilt/lib/ghc-%bootstrap/:/usr/gnu/lib:$LD_LIBRARY_PATH

# use gcc 4.x
export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++
export CXXFLAGS="%{gcc_cxx_optflags}"
export CFLAGS="%optflags"
export PKG_CONFIG_PATH="%{_cxx_libdir}/pkgconfig"
export LDFLAGS="-L%{_cxx_libdir} -R%{_cxx_libdir}"
export PERL_PATH=/usr/perl5/bin/perl
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

# Note GHC conf does not support differing host/target (i.e., cross-compiling)
cd %{_builddir}/%name-%version/ghc-%version
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_cxx_libdir}          \
            --libexecdir=%{_libexecdir}      \
            --infodir=%{_infodir}            \
            --sysconfdir=%{_sysconfdir}      \
            --with-gmp-includes=/usr/include/gmp    \
            --with-gmp-libraries=/usr/include/gmp   

gmake -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
cd %{_builddir}/%name-%version/ghc-%version
gmake install DESTDIR=$RPM_BUILD_ROOT

# Prepare lists of files for packaging
cd %{_builddir}/%name-%version
touch ghc6.files ghc6-prof.files ghc6-all.files
find $RPM_BUILD_ROOT -type f -name "*.p_hi" > ghc6-prof.files
find $RPM_BUILD_ROOT -type f -name "*_p.a" >> ghc6-prof.files

find $RPM_BUILD_ROOT/usr/lib -type f -name "*" > ghc6-all.files

sort ghc6-prof.files > ghc6-prof-sort.files
sort ghc6-all.files > ghc6-all-sort.files
comm -23 ghc6-all-sort.files ghc6-prof-sort.files > ghc6.files

# Clean up syntax for %files section
cat ghc6.files | sed 's:'"$RPM_BUILD_ROOT"'::' > TEMP && mv TEMP ghc6.files
cat ghc6-prof-sort.files | sed 's:'"$RPM_BUILD_ROOT"'::' > TEMP && mv TEMP ghc6-prof.files

# Remove extra documentation
#rm -r $RPM_BUILD_ROOT/usr/share*
# Manpages aren't building for some reason... steal from prebuilt!
cp -r %{_builddir}/%name-%version/postbuilt/share/man* $RPM_BUILD_ROOT/usr/share/

%clean
rm -rf $RPM_BUILD_ROOT


%files -f ghc6.files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_bindir}
%{_bindir}/*
%{_mandir}/man1/*

%files prof -f ghc6-prof.files
%defattr (-, root, bin)

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Sun Sep 6 2009 - jchoi42@pha.jhu.edu
- Initial spec
