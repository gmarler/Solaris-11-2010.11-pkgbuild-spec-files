#
# spec file for package SFEmpc
#
# includes module(s): GNU mpc
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

#%define SFEgmp   %(/usr/bin/pkginfo -q SFEgmp && echo 1 || echo 0)
#SFEmpfr without SFEgmp makes no sense! Make it a hard Reqirement for now
##TODO## ##FIXME## need a clever decision here
%define SFEgmp 1

#%define SFEgmp   %(/usr/bin/pkginfo -q SFEgmp && echo 1 || echo 0)
#SFEmpfr without SFEgmp makes no sense! Make it a hard Reqirement for now
##TODO## ##FIXME## need a clever decision here
%define SFEmpfr 1

Name:                SFElibmpc
Summary:             C library for for the arithmetic of complex numbers with arbitrarily high precision and correct rounding of the result
Version:             0.8.2
Source:              http://www.multiprecision.org/mpc/download/mpc-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}/%{_subdir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%if %SFEgmp
BuildRequires: SFEgmp-devel
Requires: SFEgmp
#IPS doesn't honour SUNW_BaseDir 
##TODO## ##FIXME##
#%define SFEgmpbasedir %(pkgparam SFEgmp BASEDIR)
%define SFEgmpbasedir %{_prefix} 
%else
BuildRequires: SUNWgnu-mp
Requires: SUNWgnu-mp
%endif

%if %SFEmpfr
BuildRequires: SFEmpfr-devel
Requires: SFEmpfr
#IPS doesn't honour SUNW_BaseDir 
##TODO## ##FIXME##
#%define SFEmpfrbasedir %(pkgparam SFEmpfr BASEDIR)
%define SFEmpfrbasedir %{_prefix} 
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
cp -pr mpc-%{version} mpc-%{version}-64
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

cd mpc-%{version}-64

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
%if %SFEmpfr
            --with-mpfr=%{SFEmpfrbasedir}         \
%else
%endif
	    $nlsopt

make -j$CPUS
cd ..
%endif

cd mpc-%{version}

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
%if %SFEmpfr
            --with-mpfr=%{SFEmpfrbasedir}         \
%else
%endif
	    $nlsopt

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
cd mpc-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{_arch64}/*.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd mpc-%{version}
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'mpc.info' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'mpc.info' ;
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
* Sat Oct 23 2010 - Thomas Wagner
- initial spec (derived from SFEmpfr.spec)
- avoid naming clush by naming the package: "libmpc" (SFEMpc to be removed)
