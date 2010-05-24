#
# spec file for package SFElapack.spec
#
# includes module(s): lapack
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use lapack64 = lapack.spec
%endif

%include base.inc
%use lapack = lapack.spec

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Tag definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
Name:		SFElapack
Summary:	%{lapack.summary}
Version:	%{lapack.version}
Group:		%{lapack.group}
URL:		%{lapack.url}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWcsl
Requires: SUNWlibms
Requires: SFEblas

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%lapack64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%lapack.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%lapack64.build -d %name-%version/%_arch64
%endif

%lapack.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%lapack64.install -d %name-%version/%_arch64
%endif

%lapack.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755,root,bin) %{_libdir}
%{_libdir}/lib*.a
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.a
%endif

%changelog
* Mon May 24 2010 - Milan Jurik
- multiarch support
* Wed Dec 10 2008 - dauphin@enst.fr
- Initial version
