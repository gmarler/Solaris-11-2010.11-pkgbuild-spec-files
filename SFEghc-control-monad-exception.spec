#
# spec file for package SFEghc-control-monad-exception
#
# Copyright 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%define ghc_version 6.12.1

Name:                    control-monad-exception
Summary:                 control-monad-exception - Explicitly typed, checked exceptions with stack traces
Version:                 0.9.0
Release:                 1
License:                 Public Domain
Group:                   Development/Languages/Haskell
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
URL:                     http://pepeiborra.github.com/control-monad-exception
Source:                  http://hackage.haskell.org/packages/archive/%{name}/%{version}/%{name}-%{version}.tar.gz
SUNW_Pkg:		 SFEghc-c-monad-e
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SFEgcc
Requires: SFEghc
Requires: SFEghc-haskell-platform
Requires: SFEghc-failure
Requires: SFEghc-monadloc
Requires: SFEghc-safe-failure

%description
This package provides explicitly typed, checked exceptions as a library. 

Computations throwing different types of exception can be combined seamlessly. 

Example 
 data Expr = Add Expr Expr | Div Expr Expr | Val Double
 eval (Val x)     = return x
 eval (Add a1 a2) = do
    v1 <- eval a1
    v2 <- eval a2
    let sum = v1 + v2
    if sum < v1 || sum < v2 then throw SumOverflow else return sum
 eval (Div a1 a2) = do
    v1 <- eval a1
    v2 <- eval a2
    if v2 == 0 then throw DivideByZero else return (v1 / v2)
 data DivideByZero = DivideByZero deriving (Show, Typeable)
 data SumOverflow  = SumOverflow  deriving (Show, Typeable)
 instance Exception DivideByZero
 instance Exception SumOverflow

GHCi infers the following types 
 eval :: (Throws DivideByZero l, Throws SumOverflow l) => Expr -> EM l Double
 eval `catch` \ (e::DivideByZero) -> return (-1)  :: Throws SumOverflow l => Expr -> EM l Double
 runEM(eval `catch` \ (e::SomeException) -> return (-1))  :: Expr -> Double

In addition to explicitly typed exceptions his package provides: 

Support for explicitly documented, unchecked exceptions (via Control.Monad.Exception.tryEMT). 

Support for selective unchecked exceptions (via Control.Monad.Exception.UncaughtException). 

Support for exception call traces via Control.Monad.Loc.MonadLoc. Example: 
 f () = do throw MyException
 g a  = do f a

 main = runEMT $ do g () `catchWithSrcLoc`
                        \loc (e::MyException) -> lift(putStrLn$ showExceptionWithTrace loc e)

 -- Running main produces the output:

 *Main> main
  MyException
    in f, Main(example.hs): (1,6)
       g, Main(example.hs): (2,6)
       main, Main(example.hs): (5,9)
       main, Main(example.hs): (4,16)

%package -n SFEghc-c-monad-e-prof
Summary:                 %{summary} - profiling libraries
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SFEghc-c-monad-e

%package -n SFEghc-c-monad-e-doc
Summary:                 %{summary} - doc files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SFEghc-c-monad-e

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

%post -n SFEghc-c-monad-e-doc
cd %{_docdir}/ghc/html/libraries && [ -x "./gen_contents_index" ] && ./gen_contents_index

%preun
# Need to unregister the package with ghc-pkg for the rebuild of the spec file to work
/usr/bin/ghc-pkg unregister --global --force %{name}-%{version}

%postun -n SFEghc-c-monad-e-doc
if [ "$1" -eq 0 ] ; then
  cd %{_docdir}/ghc/html/libraries && [ -x "./gen_contents_index" ] && ./gen_contents_index
fi

%files -f pkg.files
%defattr (-, root, bin)

%files -n SFEghc-c-monad-e-prof -f pkg-prof.files
%defattr (-, root, bin)

%files  -n SFEghc-c-monad-e-doc -f pkg-doc.files
%defattr(-,root,root,-)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_docdir}/ghc
%dir %attr (0755, root, bin) %{_docdir}/ghc/html
%dir %attr (0755, root, bin) %{_docdir}/ghc/html/libraries
%dir %attr (0755, root, bin) %{_docdir}/ghc/html/libraries/%{name}-%{version}

%changelog
* Thu May 27 2010 - markwright@internode.on.net
- Initial Solaris version 0.9.0
