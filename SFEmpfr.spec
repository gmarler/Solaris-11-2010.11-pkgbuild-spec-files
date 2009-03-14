#
# spec file for package SFEmpfr
#
# includes module(s): GNU mpfr
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

%define SFEgmp   %(/usr/bin/pkginfo -q SFEgmp && echo 1 || echo 0)


Name:                SFEmpfr
Summary:             C library for multiple-precision floating-point computations
Version:             2.4.1
Source:              http://www.mpfr.org/mpfr-current/mpfr-%{version}.tar.bz2
SUNW_BaseDir:        %{_basedir}/%{_subdir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%if %SFEgmp
BuildRequires: SFEgmp-devel
Requires: SFEgmp
Conflicts: SUNWgnu-mpfr
%define SFEgmpbasedir %(pkgparam SFEgmp BASEDIR)
%else
BuildRequires: SUNWgnu-mp
Requires: SUNWgnu-mp
%endif

Requires: SUNWpostrun

%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}/%{_subdir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version
%ifarch amd64 sparcv9
cp -pr mpfr-%{version} mpfr-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS32="%optflags  -L/usr/gnu/lib -R/usr/gnu/lib"
export CFLAGS64="%optflags64 -L/usr/gnu/lib/%{bld_arch} -R/usr/gnu/lib/%{bld_arch}"
export CXXFLAGS32="%cxx_optflags  -L/usr/gnu/lib -R/usr/gnu/lib"
export CXXFLAGS64="%cxx_optflags64 -L/usr/gnu/lib/%{bld_arch} -R/usr/gnu/lib/%{bld_arch}"
export LDFLAGS32="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"
export LDFLAGS64="%_ldflags -L/usr/gnu/lib/%{bld_arch} -R/usr/gnu/lib/%{bld_arch}"

%ifarch amd64 sparcv9
export CC=${CC64:-$CC}
export CXX=${CXX64:-$CXX}
export CFLAGS="$CFLAGS64"
export CXXFLAGS="$CXXFLAGS64"
export LDFLAGS="$LDFLAGS64"

cd mpfr-%{version}-64

./configure --prefix=%{_prefix}			\
            --libdir=%{_libdir}/%{_arch64}	\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}		\
	    --without-emacs			\
	    --enable-shared			\
	    --disable-static			\
%if %SFEgmp
            --with-gmp=%{SFEgmpbasedir}         \
%else
%endif
	    $nlsopt

make -j$CPUS
cd ..
%endif

cd mpfr-%{version}

export CC=${CC32:-$CC}
export CXX=${CXX32:-$CXX}
export CFLAGS="$CFLAGS32"
export CXXFLAGS="$CXXFLAGS32"
export LDFLAGS="$LDFLAGS32"

./configure --prefix=%{_prefix}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}       \
            --mandir=%{_mandir}		\
	    --infodir=%{_infodir}	\
	    --without-emacs		\
	    --enable-shared		\
	    --disable-static		\
%if %SFEgmp
            --with-gmp=%{SFEgmpbasedir}         \
%else
%endif
	    $nlsopt

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
cd mpfr-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{_arch64}/*.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd mpfr-%{version}
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'mpfr.info' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'mpfr.info' ;
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
%dir %attr(0755, root, bin) %{_infodir}
%{_infodir}/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Sat Mar 07 2009 - Thomas Wagner
- Bumped up the version to 2.4.1
- fix packaging error by adding %_datadir to configure
- redefine %{_infodir} to be in /usr/gnu
- add subdir to SUNW_BaseDir:            %{_basedir}/%{_subdir}
- add configure --with-gmp to set gmp basedir
* Sun Feb 22 2009 - Thomas Wagner
- move to /usr/gnu and remove Conflicts: SUNWgnu-mpfr
* Sat Feb 21 2009 - Thomas Wagner
- make SFEgmp / SUNWgnu-mpfr conditional
- add Conflicts: SUNWgnu-mpfr
* Wed Jan  7 2009 - Thomas Wagner
- Bumped up the version to 2.3.2
* Tue Feb 12 2008 <pradhap (at) gmail.com>
- Bumped up the version to 2.3.1
* Wed Oct  3 2007 - Doug Scott <dougs@truemail.co.th>
- bump to 2.3.0
* Tue Mar  7 2007 - Doug Scott <dougs@truemail.co.th>
- Initial spec
