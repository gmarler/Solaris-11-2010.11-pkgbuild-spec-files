#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# spec file for package SUNWgmp
#
# includes module(s): GNU gmp
#
%include Solaris.inc
%include usr-gnu.inc



##TODO## need propper integration of arch64.inc
%ifarch amd64
%define opt_amd64 1
%define bld_arch        amd64
%else
%define opt_sparcv9 1
%define bld_arch        sparcv9
%endif


##TODO## think on usr-gnu.inc define infodir inside /usr/gnu/share to avoid conflicts
%define _infodir           %{_datadir}/info


Name:                    SFEgmp
Summary:                 GNU Multiple Presicion Arithmetic Library
Group:                   libraries/math
Version:                 4.2.1
Source:                  http://ftp.sunet.se/pub/gnu/gmp/gmp-%{version}.tar.bz2
%ifarch amd64
Source1:                 http://www.loria.fr/~gaudry/mpn_AMD64/mpn_amd64.42.tgz
%endif
Patch1:                  gmp-01-solaris.diff
URL:                     http://gmplib.org/
SUNW_BaseDir:            %{_basedir}/%{_subdir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}/%{_subdir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version
%ifarch amd64 sparcv9
cp -pr gmp-%{version} gmp-%{version}-64
%endif
%ifarch amd64
gtar fxz %{SOURCE1}
cd mpn_amd64.42
./install ../gmp-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC32=${CC32:-$CC}
export CFLAGS32="%optflags  -L/usr/gnu/lib -R/usr/gnu/lib"
export CFLAGS64="%optflags64 -L/usr/gnu/lib/%{bld_arch} -R/usr/gnu/lib/%{bld_arch}"
export CXXFLAGS32="%cxx_optflags  -L/usr/gnu/lib -R/usr/gnu/lib"
export CXXFLAGS64="%cxx_optflags64 -L/usr/gnu/lib/%{bld_arch} -R/usr/gnu/lib/%{bld_arch}"
export LDFLAGS32="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"
export LDFLAGS64="%_ldflags -L/usr/gnu/lib/%{bld_arch} -R/usr/gnu/lib/%{bld_arch}"
export ACLOCAL_FLAGS="                       -I ."
#export ACLOCAL_FLAGS="-I %{_datadir}/aclocal -I ."

%ifarch sparcv9
export CC=${CC64:-$CC}
export CXX=${CXX64:-$CXX}
export LDFLAGS="$LDFLAGS64"
%define host --host=sparcv9-sun-solaris2.11
%endif

%ifarch amd64
export CC="gcc"
export CXX=${CXX64:-$CXX}
export CFLAGS="-mtune=opteron -m64 -O3 -fomit-frame-pointer -fPIC -DPIC"
export CXXFLAGS="$CXXFLAGS64"
export LDFLAGS="$LDFLAGS64"
%endif


%ifarch amd64 sparcv9
cd gmp-%{version}-64
%patch1 -p1

libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f 
autoconf
export ABI=64
./configure --prefix=%{_prefix}				\
	    --mandir=%{_mandir}				\
            --libdir=%{_libdir}/%{bld_arch}		\
            --infodir=%{_infodir}			\
            --datadir=%{_datadir}			\
            --libexecdir=%{_libexecdir}/%{bld_arch}      \
            --sysconfdir=%{_sysconfdir}      		\
            --disable-cxx %{?host}
make -j$CPUS 
cd ..
%endif

cd gmp-%{version}
%patch1 -p1

export CC=${CC32:-$CC}
export CXX=${CXX32:-$CXX}
export CFLAGS="$CFLAGS32"
export CXXFLAGS="$CXXFLAGS32"
export LDFLAGS="$LDFLAGS32"

export ABI=32
./configure --prefix=%{_prefix}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}         \
            --infodir=%{_infodir}       \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --disable-cxx
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
cd gmp-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{_arch64}/*.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd gmp-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'gmp.info gmp.info-1 gmp.info-2' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'gmp.info gmp.info-1 gmp.info-2' ;
  echo '"';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} --delete %{_infodir}/$info';
  echo 'done';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/info
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Sat Mar 14 2009 - Thomas Wagner
- shorten ACLOCAL flags by removing -I %{_datadir}/aclocal (fails if diry not present)
- fix packaging error by adding %_datadir to configure
- redefine %{_infodir} to be in /usr/gnu
- configure add %{bld_arch}
- add subdir to SUNW_BaseDir:            %{_basedir}/%{_subdir}
* Sun Feb 22 2009 - Thomas Wagner
- move to /usr/gnu and remove Conflicts: SUNWgnu-mp
* Sat Feb 21 2009 - Thomas Wagner
- add Conflicts: SUNWgnu-mp
* Tue Sep 02 2008 - halton.huo@sun.com
- Add /usr/share/aclocal to ACLOCAL_FLAGS to fix build issue
* Mon Feb 25 2008 - laca@sun.com
- fix sparcv9 build
* Fri Nov 02 2007 - nonsea@users.sourceforge.net
- Remove Requires/BuildRequires to SFEreadline
* Fri Aug 17 2007 - trisk@acm.jhu.edu
- Fix amd64 build
* Sat Jun 30 2007 - nonsea@users.sourceforge.net
- Use http url in Source.
* Tue mar  7 2007 - dougs@truemail.co.th
- enabled 64-bit build and added speedup patch for AMD64
* Fri Jun 23 2006 - laca@sun.com
- rename to SFEgmp
- bump to 4.2.1
- create devel subpkg
- update attributes
* Thu Nov 17 2005 - laca@sun.com
- create
