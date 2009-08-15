#
# spec file for package SFEgcc
#
# includes module(s): GNU gcc
#

# to more widely test if this change causes regressions, by default off:
# want this? compile with: --with-handle_pragma_pack_push_pop
%define with_handle_pragma_pack_push_pop %{?_with_handle_pragma_pack_push_pop:1}%{?!_with_handle_pragma_pack_push_pop:0}

%include Solaris.inc
#%define cc_is_gcc 1
#%define _gpp /usr/sfw/bin/g++
%include usr-gnu.inc
%include base.inc

##TODO## should include/arch64.inc consider setting _arch64 that way?
#        gcc builds 64-bit libs/binaries even on 32-bit CPUs/Kernels (e.g. ATOM CPU)
%ifarch amd64 i386
%define _arch64 amd64
%else
%define _arch64 sparcv9
%endif


%define SUNWbinutils    %(/usr/bin/pkginfo -q SUNWbinutils && echo 1 || echo 0)
%define SFEgmp          %(/usr/bin/pkginfo -q SUNWgnu-mp && echo 0 || echo 1)
%define SFEmpfr         %(/usr/bin/pkginfo -q SUNWgnu-mpfr && echo 0 || echo 1)

Name:                SFEgccruntime
Summary:             GNU gcc runtime libraries required by applications
Version:             4.3.3
Source:              ftp://ftp.gnu.org/pub/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.bz2
Patch1:              gcc-01-libtool-rpath.diff
%if %with_handle_pragma_pack_push_pop
Patch2:              gcc-02-handle_pragma_pack_push_pop.diff
%else
%endif
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFElibiconv-devel
Requires:      SFElibiconv
BuildRequires: SUNWbash

%if %SFEgmp
BuildRequires: SFEgmp-devel
Requires: SFEgmp
%define SFEgmpbasedir %(pkgparam SFEgmp BASEDIR)
%else
BuildRequires: SUNWgnu-mp
Requires: SUNWgnu-mp
%endif

%if %SFEmpfr
BuildRequires: SFEmpfr-devel
Requires: SFEmpfr
%define SFEmpfrbasedir %(pkgparam SFEmpfr BASEDIR)
%else
BuildRequires: SUNWgnu-mpfr
Requires: SUNWgnu-mpfr
%endif

#chicken-egg-problem
#also add configure switch below
%if %SUNWbinutils
BuildRequires: SUNWbinutils
Requires: SUNWbinutils
%else
BuildRequires: SFEbinutils
Requires: SFEbinutils
%endif

Requires: SUNWpostrun

%package -n SFEgcc
Summary:                 GNU gcc
Version:                 %{version}
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%if %SFEgmp
BuildRequires: SFEgmp-devel
Requires: SFEgmp
%else
BuildRequires: SUNWgnu-mp
Requires: SUNWgnu-mp
%endif

%if %SFEmpfr
BuildRequires: SFEmpfr-devel
Requires: SFEmpfr
%else
BuildRequires: SUNWgnu-mpfr
Requires: SUNWgnu-mpfr
%endif

%if %SUNWbinutils
BuildRequires: SUNWbinutils
Requires: SUNWbinutils
%else
BuildRequires: SFEbinutils
Requires: SFEbinutils
%endif
Requires: SUNWpostrun


%if %build_l10n
%package -n SFEgcc-l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -c -n %{name}-%version
mkdir gcc
#with 4.3.3 in new directory libjava/classpath/
cd gcc-%{version}/libjava/classpath/
%patch1 -p1
cd ../../..
cd gcc-%{version}
%if %with_handle_pragma_pack_push_pop
%patch2 -p1
%else
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

cd gcc

%if %build_l10n
nlsopt=-enable-nls
%else
nlsopt=-disable-nls
%endif

%define ld_options      -zignore -zcombreloc -Bdirect -i

export CONFIG_SHELL=/usr/bin/bash
export CFLAGS=""
export CPP="cc -E -Xs"
export STAGE1_CFLAGS="$(CFLAGS)"
export CFLAGS_FOR_TARGET="-g -O3"
export LDFLAGS="%_ldflags %gnu_lib_path"
export LD_OPTIONS="%ld_options %gnu_lib_path"

%define build_gcc_with_gnu_ld 0
%if %build_gcc_with_gnu_ld
export LD="/usr/gnu/bin/ld"
%endif

../gcc-%{version}/configure			\
	--prefix=%{_prefix}			\
        --libdir=%{_libdir}			\
        --libexecdir=%{_libexecdir}		\
        --mandir=%{_mandir}			\
	--infodir=%{_infodir}			\
%if %SUNWbinutils
	--with-build-time-tools=/usr/sfw	\
	--with-as=/usr/sfw/bin/gas		\
	--with-gnu-as				\
%else
	--with-as=/usr/gnu/bin/as		\
	--with-gnu-as				\
%endif
%if %build_gcc_with_gnu_ld
	--with-ld=/usr/gnu/bin/ld		\
	--with-gnu-ld				\
%else
	--with-ld=/usr/ccs/bin/ld		\
	--without-gnu-ld			\
%endif
	--enable-languages=c,c++,fortran,objc	\
	--enable-shared				\
	--disable-static			\
	--enable-decimal-float			\
%if %SFEgmp
	--with-gmp=%{SFEgmpbasedir}             \
%else
        --with-gmp_include=/usr/include/gmp \
%endif
%if %SFEmpfr
	--with-mpfr=%{SFEmpfrbasedir}           \
%else
        --with-mpfr_include=/usr/include/mpfr \
%endif
	$nlsopt

make -j$CPUS bootstrap

%install
rm -rf $RPM_BUILD_ROOT

export CONFIG_SHELL=/usr/bin/bash
export CFLAGS="%optflags"
export STAGE1_CFLAGS="$(CFLAGS)"
export CFLAGS_FOR_TARGET="-g -O3"
export LDFLAGS="%_ldflags %gnu_lib_path"
export LD_OPTIONS="%ld_options %gnu_lib_path"

cd gcc
make install DESTDIR=$RPM_BUILD_ROOT

cd $RPM_BUILD_ROOT%{_prefix}
ln -s share/man man

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -n SFEgcc
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'gcc.info cpp.info gccint.info cppinternals.info gccinstall.info gfortran.info' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun -n SFEgcc
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'gcc.info cpp.info gccint.info cppinternals.info gccinstall.info gfortran.info' ;
  echo '"';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} --delete %{_infodir}/$info';
  echo 'done';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/lib*.spec
%ifarch amd64 sparcv9 i386
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%{_libdir}/%{_arch64}/lib*.spec
%endif


%files -n SFEgcc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}
%{_prefix}/man
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_libdir}/gcc
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1
%dir %attr (0755, root, bin) %{_mandir}/man7
%{_mandir}/man7/*.7
%dir %attr(0755, root, sys) %{_std_datadir}
%dir %attr(0755, root, bin) %{_infodir}
%{_infodir}/*
%ifarch amd64 sparcv9 i386
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.a
%{_libdir}/%{_arch64}/lib*.la
%endif
%defattr (-, root, bin)
%{_includedir}


%if %build_l10n
%files -n SFEgcc-l10n
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sun Aug 09 2009 - Thomas Wagner
- BuildRequires: SUNWbash
* Sat Mar 14 2009 - Thomas Wagner
- change logic to require SFEgmp/SFEmpfr only if *no* SUNWgnu-mp/SUNWgnu-mpfr is present (this is on old OS builds)
- make SFEgcc use of new SUNWgnu-mp/SUNWgnu-mpfr (replacement for SFEgmp/SFEmpfr, SFE-versions still work with SFEgcc)
- detect new location of SFEgmp/SFEmpfr now in /usr/gnu and use them only if missing SUNWgnu-mp/SUNWgnu-mpfr
- add (Build)Requires: SFElibiconv(-devel) (thanks to check-deps.pl)
* Sat Feb 21 2009 - Thomas Wagner
- bump to 4.3.3
- make conditional SFEgmp  / SUNWgnu-mp
- make conditional SFEmpfr / SUNWgnu-mpfr
- add extra configure switch if SUNWgnu-mp and/or SUNWgnu-mpfr is used
* Sun Jan 25 2009 - Thomas Wagner
- make default without HANDLE_PRAGMA_PACK_PUSH_POP. switch on with:
  --with-handle_pragma_pack_push_pop
* Sat Jan 24 2009 - Thomas Wagner
- add HANDLE_PRAGMA_PACK_PUSH_POP (might help wine)
- bump to 4.2.4, version SFEgcc wit %{version}
* Wed Jan  7 2009 - Thomas Wagner
- add conditional SUNWbinutils/SFEbinutils to SFEgcc package
* Sun Dec 28 2008 - Thomas Wagner
- work around %files section on i386/32-bit not finding %{_arch64} binaries because _arch64 is unset ... _arch64 only set if running 64-bit OS in include/arch64.inc
* Sat Dec 27 2008 - Thomas Wagner
- add conditional SUNWbinutils/SFEbinutils to re-enable build on old OS
- add configure-switch for SUNWbinutils otherwise left over SFEbinutils catched by configure/compile. SUNWbinuils not found otherwise.
* Wed Aug 06 2008 - andras.barna@gmail.com
- change SFEbinutils to SUNWbinutils, defaulting to SUN ld
* Mon Mar 10 2008 - laca@sun.com
- add missing defattr
* Sun Mar  2 2008 - Mark Wright <markwright@internode.on.net>
- Add gcc-01-libtool-rpath.diff patch for a problem where
- the old, modified libtool 1.4 in gcc 4.2.3 drops
- -rpath /usr/gnu/lib when building libstdc++.so.6.0.9.
* Fri Feb 29 2008 - Mark Wright <markwright@internode.on.net>
- Bump to 4.2.3.  Remove patch for 32787 as it is upstreamed into gcc 4.2.3.
* Sat Jan 26 2008 - Moinak Ghosh <moinak.ghosh@sun.com>
- Refactor package to have SFEgcc and SFEgccruntime.
* Sun Oct 14 2007 - Mark Wright <markwright@internode.on.net>
- Bump to 4.2.2.
* Wed Aug 15 2007 - Mark Wright <markwright@internode.on.net>
- Change from /usr/ccs/bin/ld to /usr/gnu/bin/ld, this change
  requires SFEbinutils built with binutils-01-bug-2495.diff,
  binutils-02-ld-m-elf_i386.diff and binutils-03-lib-amd64-ld-so-1.diff.
  Add objc to --enable-languages, add --enable-decimal-float.
* Wed Jul 24 2007 - Mark Wright <markwright@internode.on.net>
- Bump to 4.2.1, add patch for gcc bug 32787.
* Wed May 16 2007 - Doug Scott <dougs@truemail.co.th>
- Bump to 4.2.0
* Tue Mar 20 2007 - Doug Scott <dougs@truemail.co.th>
- Added LD_OPTIONS so libs in /usr/gnu/lib will be found
* Sun Mar  7 2007 - Doug Scott <dougs@truemail.co.th>
- change to use GNU as from SFEbinutils
* Sun Mar  7 2007 - Doug Scott <dougs@truemail.co.th>
- Initial spec
