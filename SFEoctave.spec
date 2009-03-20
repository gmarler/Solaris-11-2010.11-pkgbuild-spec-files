#
# spec file for package SFEoctave
# Gilles Dauphin
#

%include Solaris.inc

%define SFElibsndfile   %(/usr/bin/pkginfo -q SFElibsndfile && echo 1 || echo 0)

Name:           SFEoctave
Summary:        octave High-level language, intended for numerical computations
Group:		Math
Version:        3.0.3
Source:		ftp://ftp.octave.org/pub/octave/octave-%{version}.tar.bz2
Patch1:		octave-stlport4.diff
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include	default-depend.inc
#Requires:	%name-root

%if %SFElibsndfile
BuildRequires: 	SFElibsndfile-devel
Requires: 	SFElibsndfile
%else
BuildRequires:	SUNWlibsndfile
Requires:	SUNWlibsndfile
%endif

Requires: 	SUNWgsed
Requires: 	SUNWgmake
Requires: 	SUNWgnu-gperf
Requires: 	SFEgnuplot
Requires:	SUNWncurses
Requires:	SFEfftw
Requires:	SFEblas
Requires:	SFEgnuplot
Requires:	SFElapack
Requires:	SUNWzlib
Requires:	SFEreadline
BuildRequires: 	SUNWPython
#TODO
#Requires: suitesparse examples/octave.desktop

SUNW_BaseDir:   %{_basedir}
%include default-depend.inc

%description
GNU Octave is a high-level language, primarily intended for numerical
computations. It provides a convenient command line interface for
solving linear and nonlinear problems numerically, and for performing
other numerical experiments using a language that is mostly compatible
with Matlab. It may also be used as a batch-oriented language. Octave
has extensive tools for solving common numerical linear algebra
problems, finding the roots of nonlinear equations, integrating
ordinary functions, manipulating polynomials, and integrating ordinary
differential and differential-algebraic equations. It is easily
extensible and customizable via user-defined functions written in
Octave's own language, or using dynamically loaded modules written in
C++, C, Fortran, or other languages.


%prep
%setup -q -c -n %{name}
%patch1 -p0

%build
%define enable64 no
#export CFLAGS="%optflags"
#export LDFLAGS="%_ldflags"
export LDFLAGS=" "
export CC=cc 
export CXX=CC
export F77=f77
export FC=f77
export EXTERN_CXXFLAGS="-library=stlport4"
export EXTERN_CFLAGS=" "
export CXXFLAGS="-library=stlport4"
export CFLAGS=" "
export XTRA_CRUFT_SH_LDFLAGS="-library=stlport4"
cd octave-%{version}
./configure --enable-shared --disable-static --enable-64=%enable64 --with-f77=f77 \
	--with-blas=-lblas		\
	--prefix=%{_prefix} 		\
	--mandir=%{_mandir}		\
	--infodir=%{_infodir}		\
	--bindir=%{_bindir}		\
	--libdir=%{_libdir}		\
	--datadir=%{_datadir}		\
	--includedir=%{_includedir}	\
	--docdir=%{_docdir}		\
	--libexecdir=%{_libexecdir}
make



#libtoolize --copy --force
#glib-gettextize --copy --force
#intltoolize --copy --force --automake
#aclocal
#autoconf -f
#automake -a -c -f
#./configure --prefix=%{_prefix}         \
#            $nls
#

%install

rm -rf $RPM_BUILD_ROOT
cd octave-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

#%if %build_l10n
#%else
#rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
#%endif


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/octave-%{version}
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_datadir}/octave
%dir %attr(0755, root, bin) %{_includedir}
%dir %attr(0755, root, bin) %{_includedir}/octave-%{version}
%dir %attr(0755, root, bin) %{_includedir}/octave-%{version}/octave
%dir %attr(0755, root, other) %{_datadir}/applications
%{_bindir}/octave*
%{_bindir}/mkoctfile*
%{_libdir}/octave-%{version}/*
%{_includedir}/octave-%{version}/octave/*
%{_datadir}/octave/*
%{_libexecdir}/octave
%{_mandir}/man*/octave*
%{_mandir}/man*/mkoct*
%{_infodir}/octave.info*
%{_datadir}/applications/*


#%if %build_l10n
#%files l10n
#%defattr (-, root, bin)
#%dir %attr (0755, root, sys) %{_datadir}
#%attr (-, root, other) %{_datadir}/locale
#%endif

%changelog
* Mars 20 2009 - Gilles Dauphin
- stlport4 , patch, bug about reading files
* Tue Feb 17 2009 - Thomas Wagner
- make (Build-)Requires conditional SUNWlibsndfile|SFElibsndfile(-devel)
* Dec 18 2008 - Gilles Dauphin
- Add SFEreadline as Requires
* Dec 10 2008 - Gilles Dauphin ( Gilles DOT Dauphin AT enst DOT fr)
- Initial spec
