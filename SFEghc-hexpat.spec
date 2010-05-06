#
# spec file for package SFEghc-hexpat
#
# Copyright 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%define ghc_version 6.12.1

Name:                    hexpat
Summary:                 hexpat - wrapper for expat, the fast XML parser
Version:                 0.15
Release:                 1
License:                 BSD
Group:                   Development/Languages/Haskell
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
URL:                     http://hackage.haskell.org/platform/
Source:                  http://hackage.haskell.org/packages/archive/%{name}/%{version}/%{name}-%{version}.tar.gz
SUNW_Pkg:		 SFEghc-hexpat
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SFEgcc
Requires: SFEghc
Requires: SFEghc-haskell-platform
Requires: SFEghc-List
Requires: SFEghc-text

%description
This package provides a general purpose Haskell XML library using
Expat to do its parsing (http://expat.sourceforge.net/ - a fast
stream-oriented XML parser written in C). It is extensible to any
string type, with String, ByteString and Text provided out of the box.

Basic usage: Parsing a tree (Tree), formatting a tree (Format).

Other features: Helpers for processing XML trees (Proc), trees
annotated with XML source location (Annotated), XML cursors (Cursor),
more intelligent handling of qualified tag names (Qualified), tags
qualified with namespaces (Namespaced), SAX-style parse (SAX), and
access to the low-level interface in case speed is paramount
(IO). And, NodeClass contains type classes for generalized tree
processing.

The design goals are speed, speed, speed, interface simplicity and
modularity (in that order).

For introduction and examples, see the Text.XML.Expat.Tree module. For
benchmarks, http://haskell.org/haskellwiki/Hexpat/

This package provides pure lazy parsing. However, Haskell's lazy I/O
is problematic in some applications because it doesn't handle I/O
errors properly and can give no guarantee of timely resource
cleanup. In these cases, chunked I/O is a better approach: Take a look
at the hexpat-iteratee package.

Credits to Iavor Diatchki and the xml (XML.Light) package for Proc and
Cursor.

INSTALLATION: Unix install requires an OS package called something
like libexpat-dev. On MacOSX, expat comes with Apple's optional X11
package, or you can install it from source. To install on Windows,
first install the Windows binary that's available from
http://expat.sourceforge.net/, then type (assuming you're using
v2.0.1): cabal install hexpat --extra-lib-dirs=C:\Program Files\Expat
2.0.1\Bin --extra-include-dirs=C:\Program Files\Expat 2.0.1\Source\Lib

Ensure libexpat.dll can be found in your system PATH (or copy it into
your executable's directory).

ChangeLog: 0.15 changes intended to fix a (rare) "error: a C finalizer
called back into Haskell." that seemed only to happen only on
ghc6.12.X.

%package -n SFEghc-hexpat-prof
Summary:                 %{summary} - profiling libraries
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SFEghc-hexpat

%package -n SFEghc-hexpat-doc
Summary:                 %{summary} - doc files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SFEghc-hexpat

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
export LD_OPTIONS='-L/usr/gnu/lib -R/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib'
export LDFLAGS='-L/usr/gnu/lib -R/usr/gnu/lib'
%else
export LDFLAGS="-L%{_cxx_libdir} -R%{_cxx_libdir}"
%endif
export PERL="/usr/perl5/bin/perl"

GHC=/usr/bin/ghc
GHC_PKG=/usr/bin/ghc-pkg
HSC2HS=/usr/bin/hsc2hs
VERBOSE=--verbose=3

chmod a+x ./Setup.lhs
runghc ./Setup.lhs configure --prefix=%{_prefix} \
    --libdir=%{_cxx_libdir} \
    --docdir=%{_docdir}/%{name}-%{version} \
    --htmldir=%{_docdir}/ghc/html/libraries/%{name}-%{version} \
    --libsubdir='$compiler/$pkgid' \
    --with-compiler=${GHC} --with-hc-pkg=${GHC_PKG} --with-hsc2hs=${HSC2HS} \
    --haddock-option="--html" \
    ${VERBOSE}

%build
export LD_LIBRARY_PATH='/usr/gnu/lib'
%if %{is_s10}
export LD_OPTIONS='-L/usr/gnu/lib -R/usr/gnu/lib'
%endif
runghc ./Setup.lhs build ${VERBOSE}
runghc ./Setup.lhs haddock ${VERBOSE} --executables --hoogle --hyperlink-source

%install
export LD_LIBRARY_PATH=/usr/gnu/lib:$LD_LIBRARY_PATH
%if %{is_s10}
export LD_OPTIONS='-L/usr/gnu/lib -R/usr/gnu/lib'
%endif
rm -rf $RPM_BUILD_ROOT

install -d ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}
runghc ./Setup.lhs register ${VERBOSE} --gen-pkg-config=%{name}-%{version}.conf
runghc ./Setup.lhs copy ${VERBOSE} --destdir=${RPM_BUILD_ROOT}

install -d ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/%{name}-%{version}/
install -c -m 755 %{name}-%{version}.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/%{name}-%{version}/%{name}-%{version}.conf

# Prepare lists of files for packaging
cd %{_builddir}/%{name}-%{version}
find $RPM_BUILD_ROOT -type f -name "*.p_hi" > pkg-prof.files
find $RPM_BUILD_ROOT -type f -name "*_p.a" >> pkg-prof.files
find $RPM_BUILD_ROOT/usr/lib -type f -name "*" > pkg-all.files
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

%post -n SFEghc-hexpat-doc
cd %{_docdir}/ghc/html/libraries && [ -x "./gen_contents_index" ] && ./gen_contents_index

%preun
# Need to unregister the package with ghc-pkg for the rebuild of the spec file to work
/usr/bin/ghc-pkg unregister --global --force %{name}-%{version}

%postun -n SFEghc-hexpat-doc
if [ "$1" -eq 0 ] ; then
  cd %{_docdir}/ghc/html/libraries && [ -x "./gen_contents_index" ] && ./gen_contents_index
fi

%files -f pkg.files
%defattr (-, root, bin)

%files -n SFEghc-hexpat-prof -f pkg-prof.files
%defattr (-, root, bin)

%files  -n SFEghc-hexpat-doc -f pkg-doc.files
%defattr(-,root,root,-)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_docdir}/ghc
%dir %attr (0755, root, bin) %{_docdir}/ghc/html
%dir %attr (0755, root, bin) %{_docdir}/ghc/html/libraries
%dir %attr (0755, root, bin) %{_docdir}/ghc/html/libraries/%{name}-%{version}

%changelog
* Thu May 06 2010 - markwright@internode.on.net
- Initial Solaris version 0.15
