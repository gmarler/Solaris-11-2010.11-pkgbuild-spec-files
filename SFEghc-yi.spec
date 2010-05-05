#
# spec file for package SFEghc-yi
#
# Copyright 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%define ghc_version 6.12.1

Name:                    yi
Summary:                 yi - The Haskell-Scriptable Editor
Version:                 0.6.2.2
Release:                 1
License:                 GPL
Group:                   Development/Languages/Haskell
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
URL:                     http://hackage.haskell.org/platform/
Source:                  http://hackage.haskell.org/packages/archive/%{name}/%{version}/%{name}-%{version}.tar.gz
SUNW_Pkg:		 SFEghc-yi
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

Patch1:                  ghc-yi-01-cabal.diff

%include default-depend.inc
Requires: SFEgcc
Requires: SFEghc
Requires: SFEghc-haskell-platform
Requires: SFEghc-Diff
Requires: SFEghc-binary
Requires: SFEghc-data-accessor
Requires: SFEghc-data-a-monads-fd
Requires: SFEghc-data-a-template
Requires: SFEghc-derive
Requires: SFEghc-dlist
Requires: SFEghc-dyre
Requires: SFEghc-executable-path
Requires: SFEghc-fingertree
Requires: SFEghc-ghc-paths
Requires: SFEghc-haskell-src-exts
Requires: SFEghc-monads-fd
Requires: SFEghc-pointedlist
Requires: SFEghc-pureMD5
Requires: SFEghc-regex-tdfa
Requires: SFEghc-rosezipper
Requires: SFEghc-split
Requires: SFEghc-transformers
Requires: SFEghc-uniplate
Requires: SFEghc-unix-compat
Requires: SFEghc-vty

%description
Yi is a text editor written in Haskell and extensible in Haskell. The goal of
the Yi project is to provide a flexible, powerful, and correct editor for
haskell hacking.

%package -n SFEghc-yi-prof
Summary:                 %{summary} - profiling libraries
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SFEghc-yi

%package -n SFEghc-yi-doc
Summary:                 %{summary} - doc files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SFEghc-yi

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1
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

chmod a+x ./Setup.hs
runghc ./Setup.hs configure --prefix=%{_prefix} \
    --libdir=%{_cxx_libdir} \
    --docdir=%{_docdir}/%{name}-%{version} \
    --htmldir=%{_docdir}/ghc/html/libraries/%{name}-%{version} \
    --libsubdir='$compiler/$pkgid' \
    --with-compiler=${GHC} --with-hc-pkg=${GHC_PKG} --with-hsc2hs=${HSC2HS} \
    --haddock-option="--html" \
    -fvty \
    ${VERBOSE}

%build
export LD_LIBRARY_PATH='/usr/gnu/lib'
%if %{is_s10}
export LD_OPTIONS='-L/usr/gnu/lib -R/usr/gnu/lib'
%endif
runghc ./Setup.hs build ${VERBOSE}
# The html documentation fails to build with the haddock --executables option.
runghc ./Setup.hs haddock ${VERBOSE} --hoogle --hyperlink-source

%install
export LD_LIBRARY_PATH=/usr/gnu/lib:$LD_LIBRARY_PATH
%if %{is_s10}
export LD_OPTIONS='-L/usr/gnu/lib -R/usr/gnu/lib'
%endif
rm -rf $RPM_BUILD_ROOT

install -d ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}
runghc ./Setup.hs register ${VERBOSE} --gen-pkg-config=%{name}-%{version}.conf
runghc ./Setup.hs copy ${VERBOSE} --destdir=${RPM_BUILD_ROOT}

install -d ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/%{name}-%{version}/
install -c -m 755 %{name}-%{version}.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/%{name}-%{version}/%{name}-%{version}.conf

# Prepare lists of files for packaging
cd %{_builddir}/%{name}-%{version}
find $RPM_BUILD_ROOT -type f -name "*.p_hi" > pkg-prof.files
find $RPM_BUILD_ROOT -type f -name "*_p.a" >> pkg-prof.files
find $RPM_BUILD_ROOT/usr/bin $RPM_BUILD_ROOT/usr/lib -type f -name "*" > pkg-all.files
sort pkg-prof.files > pkg-prof-sort.files
sort pkg-all.files > pkg-all-sort.files
comm -23 pkg-all-sort.files pkg-prof-sort.files > pkg.files
find $RPM_BUILD_ROOT/usr/share -type f -name "*" > pkg-doc.files
sort pkg-doc.files > pkg-doc-sort.files
# Clean up syntax for %files section
cat pkg.files | sed 's:'"$RPM_BUILD_ROOT"'::' > TEMP && mv TEMP pkg.files
cat pkg-prof-sort.files | sed 's:'"$RPM_BUILD_ROOT"'::' > TEMP && mv TEMP pkg-prof.files
cat pkg-doc-sort.files | sed 's:'"$RPM_BUILD_ROOT"'::' > TEMP && mv TEMP pkg-doc.files

%clean
rm -rf $RPM_BUILD_ROOT

%post
# The %install section above will only install files
# We need to register the package with ghc-pkg for ghc to find it
/usr/bin/ghc-pkg register --global --force %{_cxx_libdir}/ghc-%{ghc_version}/%{name}-%{version}/%{name}-%{version}.conf

%post -n SFEghc-yi-doc
cd %{_docdir}/ghc/html/libraries && [ -x "./gen_contents_index" ] && ./gen_contents_index

%preun
# Need to unregister the package with ghc-pkg for the rebuild of the spec file to work
/usr/bin/ghc-pkg unregister --global --force %{name}-%{version}

%postun -n SFEghc-yi-doc
if [ "$1" -eq 0 ] ; then
  cd %{_docdir}/ghc/html/libraries && [ -x "./gen_contents_index" ] && ./gen_contents_index
fi

%files -f pkg.files
%defattr (-, root, bin)

%files -n SFEghc-yi-prof -f pkg-prof.files
%defattr (-, root, bin)

%files  -n SFEghc-yi-doc -f pkg-doc.files
%defattr(-,root,root,-)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_docdir}/ghc
%dir %attr (0755, root, bin) %{_docdir}/ghc/html
%dir %attr (0755, root, bin) %{_docdir}/ghc/html/libraries
%dir %attr (0755, root, bin) %{_docdir}/ghc/html/libraries/%{name}-%{version}

%changelog
* Wed May 05 2010 - markwright@internode.on.net
- Build with SFEghc-transformers 0.2.1.0, build docs without
  haddock --executables option (as the documentation build fails
  with the --executables option).
* Thu Apr 8 2010 - markwright@internode.on.net
- Initial Solaris version
