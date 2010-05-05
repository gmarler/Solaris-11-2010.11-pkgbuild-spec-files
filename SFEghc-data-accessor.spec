#
# spec file for package SFEghc-data-accessor
#
# Copyright 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%define ghc_version 6.12.1

Name:                    data-accessor
Summary:                 data-accessor - Utilities for accessing and manipulating fields of records
Version:                 0.2.1.3
Release:                 1
License:                 BSD
Group:                   Development/Languages/Haskell
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
URL:                     http://hackage.haskell.org/platform/
Source:                  http://hackage.haskell.org/packages/archive/%{name}/%{version}/%{name}-%{version}.tar.gz
SUNW_Pkg:		 SFEghc-data-accessor
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SFEgcc
Requires: SFEghc
Requires: SFEghc-haskell-platform
Requires: SFEghc-transformers

%description
In Haskell 98 the name of a record field is automatically also the
name of a function which gets the value of the according
field. E.g. if we have

data Pair a b = Pair first :: a, second :: b 

then 
 first  :: Pair a b -> a
 second :: Pair a b -> b

However for setting or modifying a field value we need to use some
syntactic sugar, which is often clumsy.

modifyFirst :: (a -> a) -> (Pair a b -> Pair a b) modifyFirst f r@(Pair first=a ) = r first = f a 

With this package you can define record field accessors which allow
setting, getting and modifying values easily. The package clearly
demonstrates the power of the functional approach: You can combine
accessors of a record and sub-records, to make the access look like
the fields of the sub-record belong to the main record.

Example: 
 *Data.Accessor.Example> (first^:second^=10) (('b',7),"hallo")
 (('b',10),"hallo")

You can easily manipulate record fields in a Control.Monad.State.State
monad, you can easily code Show instances that use the Accessor syntax
and you can parse binary streams into records. See
Data.Accessor.Example for demonstration of all features.

It would be great if in revised Haskell versions the names of record
fields are automatically Data.Accessor.Accessors rather than plain get
functions. For now, the package data-accessor-template provides
Template Haskell functions for automated generation of
Data.Acesssor.Accessors.

For similar packages see lenses and fclabel. A related concept are editors
http://conal.net/blog/posts/semantic-editor-combinators/. Editors only
consist of a modify method (and modify applied to a const function is
a set function). This way, they can modify all function values of a
function at once, whereas an accessor can only change a single
function value, say, it can change f 0 = 1 to f 0 = 2. This way,
editors can even change the type of a record or a function. An Arrow
instance can be define for editors, but for accessors only a Category
instance is possible ('(.)' method). The reason is the arr method of
the Arrow class, that conflicts with the two-way nature (set and get)
of accessors.

%package -n SFEghc-data-accessor-prof
Summary:                 %{summary} - profiling libraries
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SFEghc-data-accessor

%package -n SFEghc-data-accessor-doc
Summary:                 %{summary} - doc files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SFEghc-data-accessor

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

%post -n SFEghc-data-accessor-doc
cd %{_docdir}/ghc/html/libraries && [ -x "./gen_contents_index" ] && ./gen_contents_index

%preun
# Need to unregister the package with ghc-pkg for the rebuild of the spec file to work
/usr/bin/ghc-pkg unregister --global --force %{name}-%{version}

%postun -n SFEghc-data-accessor-doc
if [ "$1" -eq 0 ] ; then
  cd %{_docdir}/ghc/html/libraries && [ -x "./gen_contents_index" ] && ./gen_contents_index
fi

%files -f pkg.files
%defattr (-, root, bin)

%files -n SFEghc-data-accessor-prof -f pkg-prof.files
%defattr (-, root, bin)

%files  -n SFEghc-data-accessor-doc -f pkg-doc.files
%defattr(-,root,root,-)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_docdir}/ghc
%dir %attr (0755, root, bin) %{_docdir}/ghc/html
%dir %attr (0755, root, bin) %{_docdir}/ghc/html/libraries
%dir %attr (0755, root, bin) %{_docdir}/ghc/html/libraries/%{name}-%{version}

%changelog
* Wed May 05 2010 - markwright@internode.on.net
- Bump to 0.2.1.3
* Thu Apr 8 2010 - markwright@internode.on.net
- Initial Solaris version 0.2.1.2
