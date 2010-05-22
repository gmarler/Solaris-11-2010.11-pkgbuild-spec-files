#
# spec file for package xblas
#
# includes module(s): xblas
#

Name:		xblas
Version:	1.0.248
Summary:	Extra Precise Basic Linear Algebra Subroutines
Group:		System Environment/Libraries
License:	BSD
URL:		http://www.netlib.org/xblas
Source:		http://www.netlib.org/%{name}/%{name}-%{version}.tar.gz
Patch1:		xblas-01-shared.diff

%description
The XBLAS library of routines is part of a reference implementation for 
the Dense and Banded Basic Linear Algebra Subroutines, along with their 
Extended and Mixed Precision versions, as documented in Chapters 2 and 4 
of the new BLAS Standard.

%package devel
Summary:	Development files for xblas
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Headers and libraries for developing code that uses xblas.

%prep
%setup -q
%patch1 -p1 -b .shared

%build
autoconf

export CFLAGS="%optflags"
export FCFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export FC=f77

if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
	export LDFLAGS="-Wl,-64 $LDFLAGS"
	export FCFLAGS="-m64"
fi

./configure --prefix=%{_prefix}	\
            --libdir=%{_libdir}
make makefiles
# smp_mflags doesn't work
make lib

%install
mkdir -p $RPM_BUILD_ROOT%{_libdir}
install -m0755 libxblas.so.1.0.0 $RPM_BUILD_ROOT%{_libdir}
pushd $RPM_BUILD_ROOT%{_libdir}
ln -s libxblas.so.1.0.0 libxblas.so.1
ln -s libxblas.so.1.0.0 libxblas.so
popd
mkdir -p $RPM_BUILD_ROOT%{_includedir}
install -m0644 src/*.h $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Aug 21 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.0.248-2
- drop README.devel, move README to -devel
- don't bother deleting buildroot at the beginning of install
- no need to define BuildRoot anymore

* Thu Apr 23 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.0.248-1
- update to 1.0.248

* Mon Apr 20 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.0.247-1
- initial package
