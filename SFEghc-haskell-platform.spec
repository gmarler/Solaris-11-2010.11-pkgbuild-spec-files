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

%define ghc_version 6.12.3

%define GLUT_version 2.1.2.1
%define HTTP_version 4000.0.9
%define HUnit_version 1.2.2.1
%define OpenGL_version 2.2.3.0
%define QuickCheck_version 2.1.1.1
%define alex_version 2.3.3
%define cabal_install_version 0.8.2
%define cgi_version 3001.1.7.3
%define deepseq_version 1.1.0.0
%define fgl_version 5.4.2.3
%define happy_version 1.18.5
%define haskell_src_version 1.0.1.3
%define html_version 1.0.1.2
%define mtl_version 1.1.0.2
%define network_version 2.2.1.7
%define parallel_version 2.2.0.1
%define parsec_version 2.1.0.1
%define regex_base_version 0.93.2
%define regex_compat_version 0.93.1
%define regex_posix_version 0.94.2
%define stm_version 2.1.2.1
%define xhtml_version 3000.2.0.1
%define zlib_version 0.5.2.0

Name:                    haskell-platform
Summary:                 Haskell-Platform
Version:                 2010.2.0.0
Release:                 1
License:                 BSD
Group:                   Development/Languages/Haskell
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
URL:                     http://hackage.haskell.org/platform/
# Note: currently this is a release candidate
# TODO delete the next line and uncomment the second line when it is released
Source:                  http://www.galois.com/~dons/tmp/hp/haskell-platform-%{version}.tar.gz
# Source:                  http://hackage.haskell.org/platform/%{version}/haskell-platform-%{version}.tar.gz
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

install -d ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/haskell-platform-%{version}
gmake install
install -c -m 755 register-haskell-platform.sh ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/haskell-platform-%{version}
install -c -m 755 unregister-haskell-platform.sh ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/haskell-platform-%{version}

install -c -m 755 packages/GLUT-%{GLUT_version}/GLUT-%{GLUT_version}.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/GLUT-%{GLUT_version}/GLUT-%{GLUT_version}.conf
install -c -m 755 packages/HTTP-%{HTTP_version}/HTTP-%{HTTP_version}.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/HTTP-%{HTTP_version}/HTTP-%{HTTP_version}.conf
install -c -m 755 packages/HUnit-%{HUnit_version}/HUnit-%{HUnit_version}.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/HUnit-%{HUnit_version}/HUnit-%{HUnit_version}.conf
install -c -m 755 packages/OpenGL-%{OpenGL_version}/OpenGL-%{OpenGL_version}.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/OpenGL-%{OpenGL_version}/OpenGL-%{OpenGL_version}.conf
install -c -m 755 packages/QuickCheck-%{QuickCheck_version}/QuickCheck-%{QuickCheck_version}.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/QuickCheck-%{QuickCheck_version}/QuickCheck-%{QuickCheck_version}.conf
install -c -m 755 packages/cgi-%{cgi_version}/cgi-%{cgi_version}.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/cgi-%{cgi_version}/cgi-%{cgi_version}.conf
install -c -m 755 packages/deepseq-%{deepseq_version}/deepseq-%{deepseq_version}.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/deepseq-%{deepseq_version}/deepseq-%{deepseq_version}.conf
install -c -m 755 packages/fgl-%{fgl_version}/fgl-%{fgl_version}.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/fgl-%{fgl_version}/fgl-%{fgl_version}.conf
install -c -m 755 packages/haskell-platform-%{version}/haskell-platform-%{version}.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/haskell-platform-%{version}/haskell-platform-%{version}.conf
install -c -m 755 packages/haskell-src-%{haskell_src_version}/haskell-src-%{haskell_src_version}.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/haskell-src-%{haskell_src_version}/haskell-src-%{haskell_src_version}.conf
install -c -m 755 packages/html-%{html_version}/html-%{html_version}.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/html-%{html_version}/html-%{html_version}.conf
install -c -m 755 packages/mtl-%{mtl_version}/mtl-%{mtl_version}.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/mtl-%{mtl_version}/mtl-%{mtl_version}.conf
install -c -m 755 packages/network-%{network_version}/network-%{network_version}.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/network-%{network_version}/network-%{network_version}.conf
install -c -m 755 packages/parallel-%{parallel_version}/parallel-%{parallel_version}.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/parallel-%{parallel_version}/parallel-%{parallel_version}.conf
install -c -m 755 packages/parsec-%{parsec_version}/parsec-%{parsec_version}.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/parsec-%{parsec_version}/parsec-%{parsec_version}.conf
install -c -m 755 packages/regex-base-%{regex_base_version}/regex-base-%{regex_base_version}.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/regex-base-%{regex_base_version}/regex-base-%{regex_base_version}.conf
install -c -m 755 packages/regex-compat-%{regex_compat_version}/regex-compat-%{regex_compat_version}.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/regex-compat-%{regex_compat_version}/regex-compat-%{regex_compat_version}.conf
install -c -m 755 packages/regex-posix-%{regex_posix_version}/regex-posix-%{regex_posix_version}.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/regex-posix-%{regex_posix_version}/regex-posix-%{regex_posix_version}.conf
install -c -m 755 packages/stm-%{stm_version}/stm-%{stm_version}.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/stm-%{stm_version}/stm-%{stm_version}.conf
install -c -m 755 packages/xhtml-%{xhtml_version}/xhtml-%{xhtml_version}.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/xhtml-%{xhtml_version}/xhtml-%{xhtml_version}.conf
install -c -m 755 packages/zlib-%{zlib_version}/zlib-%{zlib_version}.conf ${RPM_BUILD_ROOT}%{_cxx_libdir}/ghc-%{ghc_version}/zlib-%{zlib_version}/zlib-%{zlib_version}.conf

# Prepare lists of files for packaging
find $RPM_BUILD_ROOT -type f -name "*.p_hi" > pkg-prof.files
find $RPM_BUILD_ROOT -type f -name "*_p.a" >> pkg-prof.files
find $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT%{_libdir} -type f -name "*" > pkg-all.files
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

%post
# The %install section above will only install files
# We need to register the package with ghc-pkg for ghc to find it
cd %{_cxx_libdir}/ghc-%{ghc_version}
%{_cxx_libdir}/ghc-%{ghc_version}/haskell-platform-%{version}/register-haskell-platform.sh

%post -n SFEghc-haskell-platform-doc
cd %{_docdir}/ghc/html/libraries && [ -x "./gen_contents_index" ] && ./gen_contents_index

%preun
# Need to unregister the package with ghc-pkg for the rebuild of the spec file to work
cd %{_cxx_libdir}/ghc-%{ghc_version}
%{_cxx_libdir}/ghc-%{ghc_version}/haskell-platform-%{version}/unregister-haskell-platform.sh

%postun -n SFEghc-haskell-platform-doc
if [ "$1" -eq 0 ] && [ -x %{_docdir}/ghc/html/libraries/gen_contents_index ] ; then
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
* Tue July 20 2010 - markwright@internode.on.net
- Fix postun to work if SFEghc has been uninstalled. Compile with ghc 6.12.3.
- Bump to 2010.2.0.0 RC
* Thu Apr 8 2010 - markwright@internode.on.net
- Initial Solaris version
