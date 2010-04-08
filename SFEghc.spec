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
Version:                 6.12.1
Release:                 1
License:                 BSD
Group:                   Development/Languages/Haskell
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
URL:                     http://www.haskell.org/ghc
Source:                  http://www.haskell.org/ghc/dist/%{version}/ghc-%{version}-src.tar.bz2
Source1:                 http://www.haskell.org/ghc/dist/%{bootstrap}/maeder/ghc-%{bootstrap}-i386-unknown-solaris2.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%define SFEgmp          %(/usr/bin/pkginfo -q SUNWgnu-mp && echo 0 || echo 1)
%define SFEmpfr         %(/usr/bin/pkginfo -q SUNWgnu-mpfr && echo 0 || echo 1)
%define SFEreadline     %(/usr/bin/pkginfo -q SUNWgnu-readline && echo 0 || echo 1)
%define SFEncurses      %(/usr/bin/pkginfo -q SUNWncurses && echo 0 || echo 1)

%include default-depend.inc
Requires: SFEgcc

%if %SFEgmp
BuildRequires: SFEgmp-devel
Requires: SFEgmp
%else
BuildRequires: SUNWgnu-mp
Requires: SUNWgnu-mp
%endif

%if %SFEmpfr
BuildRequires: SFEmpfr-devel
Requires: SFEmpfr
%else
BuildRequires: SUNWgnu-mpfr
Requires: SUNWgnu-mpfr
%endif

BuildRequires: SUNWgtar
BuildRequires: SUNWesu

%if %SFEreadline
Requires: SFEreadline
%else
Requires: SUNWgnu-readline
%endif

%if %SFEncurses
BuildRequires: SFEncurses
%else
BuildRequires: SUNWncurses
%endif

%package prof
Summary:                 %{summary} - profiling libraries
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}

%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}

%define is_s10		%( test "`uname -r`" = "5.10" && echo 1 || echo 0 )
%define is_amd64        %( test "`isalist | cut -d' ' -f1`" = "amd64" && echo 1 || echo 0 )

%if %{is_s10}
%define gnu_tar /usr/sfw/bin/gtar
%else
%define gnu_tar /usr/gnu/bin/tar
%endif

%prep
rm -rf %{name}-%{version}
mkdir %{name}-%{version}
cd %{name}-%{version}
# ghc requires ghc to compile ghc omg
# bootstrap from prebuilt ghc (version %{bootstrap})
mkdir prebuilt
cd prebuilt
# need to use gnu tar to deal with filenames >100ch
%{gnu_tar} -xjf %SOURCE1
cd ghc-%{bootstrap}
mkdir %{_builddir}/%{name}-%{version}/postbuilt
./configure CC=gcc CXX=g++ --prefix=%{_builddir}/%{name}-%{bootstrap}/postbuilt
gmake install


%build
cd %{_builddir}/%{name}-%{version}
%{gnu_tar} -xjf %SOURCE0
export PATH=%{_builddir}/%{name}-%{bootstrap}/postbuilt/bin/:$PATH
export LD_LIBRARY_PATH=%{_builddir}/%{name}-%{bootstrap}/postbuilt/lib/ghc-%{bootstrap}/:/usr/gnu/lib:$LD_LIBRARY_PATH

# use gcc 4.x
export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++
%if %{is_amd64}
export CXXFLAGS="%{gcc_cxx_optflags} -mtune=opteron-sse3"
export CFLAGS="%optflags -mtune=opteron-sse3"
%else
export CXXFLAGS="%{gcc_cxx_optflags}"
export CFLAGS="%optflags"
%endif
export PKG_CONFIG_PATH="%{_cxx_libdir}/pkgconfig"
%if %{is_s10}
export LD_OPTIONS='-L/usr/gnu/lib -R/usr/gnu/lib'
export LDFLAGS='-L/usr/gnu/lib -R/usr/gnu/lib'
%else
export LDFLAGS="-L%{_cxx_libdir} -R%{_cxx_libdir}"
%endif
export PERL_PATH=/usr/perl5/bin/perl
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

# Note GHC conf does not support differing host/target (i.e., cross-compiling)
cd %{_builddir}/%{name}-%{version}/ghc-%{version}
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_cxx_libdir}          \
            --libexecdir=%{_libexecdir}      \
            --infodir=%{_infodir}            \
            --sysconfdir=%{_sysconfdir}      \
%if %{is_s10}
            --with-gmp-includes=/usr/gnu/include    \
            --with-gmp-libraries=/usr/gnu/lib
%else
            --with-gmp-includes=/usr/include/gmp    \
            --with-gmp-libraries=/usr/include/gmp   
%endif

# gmake -j$CPUS 
gmake VERBOSE=1

%install
rm -rf $RPM_BUILD_ROOT
cd %{_builddir}/%{name}-%{version}/ghc-%{version}
%if %{is_s10}
export LD_OPTIONS='-L/usr/gnu/lib -R/usr/gnu/lib'
%endif
gmake install DESTDIR=$RPM_BUILD_ROOT VERBOSE=1

# Need to create this symlink so that the hyperlink from file://localhost/usr/share/doc/ghc/html/index.html
# to the GHC API file://localhost/usr/share/doc/ghc/html/libraries/ghc/index.html will find it at:
# file://localhost/usr/share/doc/ghc/html/libraries/ghc-6.12.1/index.html
pushd $RPM_BUILD_ROOT%{_docdir}/ghc/html/libraries
ln -s ghc-%{version} ghc
popd

# Prepare lists of files for packaging
cd %{_builddir}/%{name}-%{version}
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
### cp -r %{_builddir}/%{name}-%{version}/postbuilt/share/man* $RPM_BUILD_ROOT/usr/share/

%clean
rm -rf $RPM_BUILD_ROOT


%files -f ghc6.files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}/man1/*

%files prof -f ghc6-prof.files
%defattr (-, root, bin)

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Thu Apr 8 2010 - markwright@internode.on.net
- Bump to 6.12.1
* Sun Sep 6 2009 - jchoi42@pha.jhu.edu
- Initial spec
