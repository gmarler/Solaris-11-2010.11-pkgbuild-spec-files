#
# spec file for package SFExblas
#
# includes module(s): xblas
#

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use xblas64 = xblas.spec
%endif

%include base.inc
%use xblas = xblas.spec

Name:		SFExblas
Version:	%{xblas.version}
Summary:	%{xblas.summary}
Group:		%{xblas.group}
License:	%{xblas.license}
URL:		%{xblas.url}
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc

%description
The XBLAS library of routines is part of a reference implementation for 
the Dense and Banded Basic Linear Algebra Subroutines, along with their 
Extended and Mixed Precision versions, as documented in Chapters 2 and 4 
of the new BLAS Standard.

%package devel
Summary:	%{summary} - development files
Group:		Development/Libraries
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name

%description devel
Headers and libraries for developing code that uses xblas.

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%xblas64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%xblas.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%xblas64.build -d %name-%version/%_arch64
%endif

%xblas.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%xblas64.install -d %name-%version/%_arch64
%endif

%xblas.install -d %name-%version/%{base_arch}
find $RPM_BUILD_ROOT%{_libdir} -name \*.la -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so.*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif


%files devel
%defattr(-,root,bin)
%{_libdir}/*.so
%{_includedir}/*.h

%changelog
* Sat May 22 2010 - Milan Jurik
- initial import to SFE
* Fri Aug 21 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.0.248-2
- drop README.devel, move README to -devel
- don't bother deleting buildroot at the beginning of install
- no need to define BuildRoot anymore

* Thu Apr 23 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.0.248-1
- update to 1.0.248

* Mon Apr 20 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.0.247-1
- initial package
