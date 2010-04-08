#
# spec file for package SFEghc-haskell-platform
#
# Copyright 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%define ghc_version 6.12.1

Name:                    haskell-platform
Summary:                 Haskell-Platform
Version:                 2010.1.0.0
Release:                 1
License:                 BSD
Group:                   Development/Languages/Haskell
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
URL:                     http://hackage.haskell.org/platform/
Source:                  http://hackage.haskell.org/platform/%{version}/haskell-platform-%{version}.tar.gz
SUNW_Pkg:		 SFEghc-haskell-platform
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

Patch1:                  ghc-haskel-platform-01-build.diff
Patch2:                  ghc-haskel-platform-02-install.diff

%include default-depend.inc
Requires: SFEgcc
Requires: SFEghc
Requires: SFEghc-hscolour

%package -n SFEghc-haskell-platform-prof
Summary:                 %{summary} - profiling libraries
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SFEghc-haskell-platform

%package -n SFEghc-haskell-platform-doc
Summary:                 %{summary} - doc files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SFEghc-haskell-platform

%prep
%setup -q -n haskell-platform-%version
%patch1 -p1
%patch2 -p1
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

bash ./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_cxx_libdir} \
            --libexecdir=%{_libexecdir}      \
            --infodir=%{_infodir}            \
            --sysconfdir=%{_sysconfdir}      \
            --enable-profiling               \
            --docdir=%{_docdir}/%{name}-%{version} \
            --htmldir=%{_docdir}/ghc/html/libraries/%{name}-%{version}

sed -i -e 's,scripts/build.sh,bash scripts/build.sh,' Makefile
sed -i -e 's,scripts/install.sh,bash scripts/install.sh,' Makefile

%build
export LD_LIBRARY_PATH='/usr/gnu/lib'
%if %{is_s10}
export LD_OPTIONS='-L/usr/gnu/lib -R/usr/gnu/lib'
%endif
gmake

%install
export LD_LIBRARY_PATH=/usr/gnu/lib:$LD_LIBRARY_PATH
%if %{is_s10}
export LD_OPTIONS='-L/usr/gnu/lib -R/usr/gnu/lib'
%endif
rm -rf $RPM_BUILD_ROOT

echo "#! /bin/sh" >register-haskell-platform.sh
echo "" >>register-haskell-platform.sh
echo "LD_OPTIONS='-L/usr/gnu/lib -R/usr/gnu/lib'; export LD_OPTIONS" >>register-haskell-platform.sh
echo "" >>register-haskell-platform.sh
echo "die () {" >>register-haskell-platform.sh
echo "  echo" >>register-haskell-platform.sh
echo "  echo \"Error:\"" >>register-haskell-platform.sh
echo "  echo $1 >&2" >>register-haskell-platform.sh
echo "  exit 2" >>register-haskell-platform.sh
echo "}" >>register-haskell-platform.sh
echo "" >>register-haskell-platform.sh
echo "ghc-pkg recache" >>register-haskell-platform.sh
echo "" >>register-haskell-platform.sh

echo "#! /bin/sh" >unregister-haskell-platform.sh
echo "" >>unregister-haskell-platform.sh
echo "LD_OPTIONS='-L/usr/gnu/lib -R/usr/gnu/lib'; export LD_OPTIONS" >>unregister-haskell-platform.sh
echo "" >>unregister-haskell-platform.sh
echo "die () {" >>unregister-haskell-platform.sh
echo "  echo" >>unregister-haskell-platform.sh
echo "  echo \"Error:\"" >>unregister-haskell-platform.sh
echo "  echo $1 >&2" >>unregister-haskell-platform.sh
echo "  exit 2" >>unregister-haskell-platform.sh
echo "}" >>unregister-haskell-platform.sh
echo "" >>unregister-haskell-platform.sh

install -d ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/haskell-platform-2010.1.0.0
gmake install
install -c -m 755 register-haskell-platform.sh ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/haskell-platform-2010.1.0.0
install -c -m 755 unregister-haskell-platform.sh ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/haskell-platform-2010.1.0.0

install -c -m 755 packages/GLUT-2.1.2.1/GLUT-2.1.2.1.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/GLUT-2.1.2.1/GLUT-2.1.2.1.conf
install -c -m 755 packages/HTTP-4000.0.9/HTTP-4000.0.9.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/HTTP-4000.0.9/HTTP-4000.0.9.conf
install -c -m 755 packages/HUnit-1.2.2.1/HUnit-1.2.2.1.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/HUnit-1.2.2.1/HUnit-1.2.2.1.conf
install -c -m 755 packages/OpenGL-2.2.3.0/OpenGL-2.2.3.0.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/OpenGL-2.2.3.0/OpenGL-2.2.3.0.conf
install -c -m 755 packages/QuickCheck-2.1.0.3/QuickCheck-2.1.0.3.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/QuickCheck-2.1.0.3/QuickCheck-2.1.0.3.conf
install -c -m 755 packages/cgi-3001.1.7.2/cgi-3001.1.7.2.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/cgi-3001.1.7.2/cgi-3001.1.7.2.conf
install -c -m 755 packages/deepseq-1.1.0.0/deepseq-1.1.0.0.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/deepseq-1.1.0.0/deepseq-1.1.0.0.conf
install -c -m 755 packages/fgl-5.4.2.2/fgl-5.4.2.2.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/fgl-5.4.2.2/fgl-5.4.2.2.conf
install -c -m 755 packages/haskell-platform-2010.1.0.0/haskell-platform-2010.1.0.0.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/haskell-platform-2010.1.0.0/haskell-platform-2010.1.0.0.conf
install -c -m 755 packages/haskell-src-1.0.1.3/haskell-src-1.0.1.3.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/haskell-src-1.0.1.3/haskell-src-1.0.1.3.conf
install -c -m 755 packages/html-1.0.1.2/html-1.0.1.2.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/html-1.0.1.2/html-1.0.1.2.conf
install -c -m 755 packages/mtl-1.1.0.2/mtl-1.1.0.2.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/mtl-1.1.0.2/mtl-1.1.0.2.conf
install -c -m 755 packages/network-2.2.1.7/network-2.2.1.7.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/network-2.2.1.7/network-2.2.1.7.conf
install -c -m 755 packages/parallel-2.2.0.1/parallel-2.2.0.1.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/parallel-2.2.0.1/parallel-2.2.0.1.conf
install -c -m 755 packages/parsec-2.1.0.1/parsec-2.1.0.1.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/parsec-2.1.0.1/parsec-2.1.0.1.conf
install -c -m 755 packages/regex-base-0.93.1/regex-base-0.93.1.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/regex-base-0.93.1/regex-base-0.93.1.conf
install -c -m 755 packages/regex-compat-0.92/regex-compat-0.92.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/regex-compat-0.92/regex-compat-0.92.conf
install -c -m 755 packages/regex-posix-0.94.1/regex-posix-0.94.1.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/regex-posix-0.94.1/regex-posix-0.94.1.conf
install -c -m 755 packages/stm-2.1.1.2/stm-2.1.1.2.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/stm-2.1.1.2/stm-2.1.1.2.conf
install -c -m 755 packages/xhtml-3000.2.0.1/xhtml-3000.2.0.1.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/xhtml-3000.2.0.1/xhtml-3000.2.0.1.conf
install -c -m 755 packages/zlib-0.5.2.0/zlib-0.5.2.0.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/zlib-0.5.2.0/zlib-0.5.2.0.conf

# Prepare lists of files for packaging
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
cd %{_cxx_libdir}/ghc-%{ghc_version}
%{_cxx_libdir}/ghc-%{ghc_version}/haskell-platform-2010.1.0.0/register-haskell-platform.sh

%post -n SFEghc-haskell-platform-doc
cd %{_docdir}/ghc/html/libraries && [ -x "./gen_contents_index" ] && ./gen_contents_index

%preun
# Need to unregister the package with ghc-pkg for the rebuild of the spec file to work
cd %{_cxx_libdir}/ghc-%{ghc_version}
%{_cxx_libdir}/ghc-%{ghc_version}/haskell-platform-2010.1.0.0/unregister-haskell-platform.sh

%postun -n SFEghc-haskell-platform-doc
if [ "$1" -eq 0 ] ; then
  cd %{_docdir}/ghc/html/libraries && [ -x "./gen_contents_index" ] && ./gen_contents_index
fi

%files -f pkg.files
%defattr (-, root, bin)

%files -n SFEghc-haskell-platform-prof -f pkg-prof.files
%defattr (-, root, bin)

%files  -n SFEghc-haskell-platform-doc -f pkg-doc.files
%defattr(-,root,root,-)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_docdir}/ghc
%dir %attr (0755, root, bin) %{_docdir}/ghc/html
%dir %attr (0755, root, bin) %{_docdir}/ghc/html/libraries
%dir %attr (0755, root, bin) %{_docdir}/ghc/html/libraries/%{name}-%{version}

%changelog
* Thu Apr 8 2010 - markwright@internode.on.net
- Initial Solaris version
