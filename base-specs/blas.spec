#
# spec file for package blasc
#
# includes module(s): blas
#

Name:		blas
Summary:	BLAS - Basic Linear Algebra Subprograms
# In fact there is no version , we give it
Version:	1.1
Source:		ftp://ftp.netlib.org/blas/blas.tgz
#Source1:	blas.Makefile
Group:		Math
URL:		http://www.netlib.org/blas/

Requires: SUNWcsl
Requires: SUNWlibms

%prep
%setup -q -c -n %{name}

%build
export PATH=/usr/gcc/4.3/bin:$PATH
cd BLAS
if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
  make CC=cc CXX=CC F77=f77 FORTRAN=f77 LOADER=f77 PLAT="" OPTS="-03 -m64"
else
  make F77=gfortran FORTRAN=gfortran LOADER=gfortran PLAT="" OPTS="-03"
fi

%install
cd BLAS
mv blas.a libblas.a
install -d -m 0755 $RPM_BUILD_ROOT/%{_libdir}
install -m 0755 libblas.a $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue May 25 2010 - Milan Jurik
- disable multiarch support, not stable with Sun studio Fortran and unsupported with gfortran yet
* Mon May 24 2010 - Milan Jurik
- multiarch support
* Wed Dec 10 2008 - dauphin@enst.fr
- Initial version
