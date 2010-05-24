#
# spec file for package lapack
#
# includes module(s): lapack
#

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Tag definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
Name:		lapack
Summary:	LAPACK - Linear Algebra PACKage
Version:	3.2.1
Source:		ftp://ftp.netlib.org/lapack/lapack-%{version}.tgz
Group:		Math
URL:		http://www.netlib.org/lapack/

Requires: SUNWcsl
Requires: SUNWlibms
Requires: SFEblas

%prep
%setup -q -c -n %{name}

%build
cd lapack-%{version}
mv make.inc.example make.inc
ln -s %{_libdir}/libblas.a blas.a
if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
  make CC=cc CXX=CC F77=f77 FORTRAN=f90 LOADER=f90 PLAT="" OPTS="-O3 -m64" LOADOPTS=-m64 NOOPT=-m64
else
  make CC=cc CXX=CC F77=f77 FORTRAN=f90 LOADER=f90 PLAT="" OPTS=-O3
fi

%install
cd lapack-%{version}
mv lapack.a liblapack.a
install -d -m 0755 $RPM_BUILD_ROOT/%{_libdir}
install -m 0755 liblapack.a $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon May 24 2010 - Milan Jurik
- multiarch support
* Wed Dec 10 2008 - dauphin@enst.fr
- Initial version
