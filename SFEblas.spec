#
# spec file for package SFEblas.spec
#
# includes module(s): blas
#
%include Solaris.inc

#%ifarch amd64 sparcv9
#%include arch64.inc
#%use blas64 = blas.spec
#%endif

%include base.inc
%use blas = blas.spec

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Tag definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
Name:		SFEblas
Summary:	%{blas.summary}
Version:	%{blas.version}
Group:		%{blas.group}
URL:		%{blas.url}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc

Requires: SUNWcsl
Requires: SUNWlibms

%prep
rm -rf %name-%version
mkdir %name-%version
#%ifarch amd64 sparcv9
#mkdir %name-%version/%_arch64
#%blas64.prep -d %name-%version/%_arch64
#%endif

mkdir %name-%version/%{base_arch}
%blas.prep -d %name-%version/%{base_arch}

%build
#%ifarch amd64 sparcv9
#%blas64.build -d %name-%version/%_arch64
#%endif

%blas.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
#%ifarch amd64 sparcv9
#%blas64.install -d %name-%version/%_arch64
##%endif

%blas.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)

%dir %attr(0755,root,bin) %{_libdir}
%{_libdir}/lib*.a
#%ifarch amd64 sparcv9
#%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
#%{_libdir}/%{_arch64}/lib*.a
#%endif


%changelog
* Tue May 25 2010 - Milan Jurik
- disable multiarch support, not stable with Sun studio Fortran and unsupported with gfortran yet
* Mon May 24 2010 - Milan Jurik
- multiarch support
* Wed Dec 10 2008 - dauphin@enst.fr
- Initial version
