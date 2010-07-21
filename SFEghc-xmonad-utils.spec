#
# spec file for package SFEghc-xmonad-utils
#
# Copyright 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%define ghc_version 6.12.3

Name:                    xmonad-utils
Summary:                 xmonad-utils - Third party extensions for xmonad with wacky dependencies
Version:                 0.1.2
Release:                 1
License:                 BSD
Group:                   Development/Languages/Haskell
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
URL:                     http://hackage.haskell.org/platform/
Source:                  http://hackage.haskell.org/packages/archive/%{name}/%{version}/%{name}-%{version}.tar.gz
SUNW_Pkg:		 SFEghc-xmonad-utils
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SFEgcc
Requires: SFEghc
Requires: SFEghc-haskell-platform
BuildRequires: SUNWgzip
Requires: SUNWxorg-clientlibs
Requires: SUNWxorg-headers
Requires: SFEghc-X11

%description
Third party extensions for xmonad with wacky dependencies

%package -n SFEghc-xmonad-utils-prof
Summary:                 %{summary} - profiling libraries
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SFEghc-xmonad-utils

%package -n SFEghc-xmonad-utils-doc
Summary:                 %{summary} - doc files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SFEghc-xmonad-utils

%prep
%setup -q -n %{name}-%{version}
export LD_LIBRARY_PATH=/usr/gnu/lib:$LD_LIBRARY_PATH

# Need to use same gcc as we used to build ghc (gcc 4.x)
export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++
export CXXFLAGS="%{gcc_cxx_optflags}"
export CFLAGS="%optflags"
export PKG_CONFIG_PATH="%{_cxx_libdir}/pkgconfig"
%if %{is_s10}
export LD_OPTIONS='-L/usr/gnu/lib -R/usr/gnu/lib'
export LDFLAGS='-L/usr/gnu/lib -R/usr/gnu/lib'
%else
export LDFLAGS="-L%{_cxx_libdir} -R%{_cxx_libdir}"
%endif
export PERL="/usr/perl5/bin/perl"

GHC=/usr/bin/ghc
GHC_PKG=/usr/bin/ghc-pkg
HSC2HS=/usr/bin/hsc2hs
VERBOSE=--verbose=3

%if %{is_s10}
sed -i -e 's,crypt,crypt_d,' xmonad-utils.cabal
%endif

chmod a+x ./Setup.lhs
runghc ./Setup.lhs configure --prefix=%{_prefix} \
    --libdir=%{_cxx_libdir} \
    --docdir=%{_docdir}/%{name}-%{version} \
    --htmldir=%{_docdir}/ghc/html/libraries/%{name}-%{version} \
    --libsubdir='$compiler/$pkgid' \
    --with-compiler=${GHC} --with-hc-pkg=${GHC_PKG} --with-hsc2hs=${HSC2HS} \
    --haddock-option="--html" \
    --enable-library-profiling \
    ${VERBOSE}

%build
export LD_LIBRARY_PATH='/usr/gnu/lib'
%if %{is_s10}
export LD_OPTIONS='-L/usr/gnu/lib -R/usr/gnu/lib'
%endif
runghc ./Setup.lhs build ${VERBOSE}
runghc ./Setup.lhs haddock ${VERBOSE} --hoogle --hyperlink-source

%install
export LD_LIBRARY_PATH=/usr/gnu/lib:$LD_LIBRARY_PATH
%if %{is_s10}
export LD_OPTIONS='-L/usr/gnu/lib -R/usr/gnu/lib'
%endif
rm -rf $RPM_BUILD_ROOT

runghc ./Setup.lhs copy ${VERBOSE} --destdir=${RPM_BUILD_ROOT}

# Prepare lists of files for packaging
cd %{_builddir}/%{name}-%{version}
find $RPM_BUILD_ROOT -type f -name "*.p_hi" > pkg-prof.files
find $RPM_BUILD_ROOT -type f -name "*_p.a" >> pkg-prof.files
find $RPM_BUILD_ROOT%{_bindir} -type f -name "*" > pkg-all.files
sort pkg-prof.files > pkg-prof-sort.files
sort pkg-all.files > pkg-all-sort.files
comm -23 pkg-all-sort.files pkg-prof-sort.files > pkg.files
find $RPM_BUILD_ROOT%{_datadir} -type f -name "*" > pkg-doc.files
sort pkg-doc.files > pkg-doc-sort.files
# Clean up syntax for %files section
cat pkg.files | sed 's:'"$RPM_BUILD_ROOT"'::' > TEMP && mv TEMP pkg.files
cat pkg-prof-sort.files | sed 's:'"$RPM_BUILD_ROOT"'::' > TEMP && mv TEMP pkg-prof.files
cat pkg-doc-sort.files | sed 's:'"$RPM_BUILD_ROOT"'::' > TEMP && mv TEMP pkg-doc.files

%clean
rm -rf $RPM_BUILD_ROOT

%post -n SFEghc-xmonad-utils-doc
cd %{_docdir}/ghc/html/libraries && [ -x "./gen_contents_index" ] && ./gen_contents_index

%postun -n SFEghc-xmonad-utils-doc
if [ "$1" -eq 0 ] && [ -x %{_docdir}/ghc/html/libraries/gen_contents_index ] ; then
  cd %{_docdir}/ghc/html/libraries && [ -x "./gen_contents_index" ] && ./gen_contents_index
fi

%files -f pkg.files
%defattr (-, root, bin)

%files -n SFEghc-xmonad-utils-prof -f pkg-prof.files
%defattr (-, root, bin)

%files  -n SFEghc-xmonad-utils-doc -f pkg-doc.files
%defattr(-,root,root,-)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}

%changelog
* Wed July 21 2010 - markwright@internode.on.net
- Initial spec
