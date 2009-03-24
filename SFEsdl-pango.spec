#
# spec file for package SFEsdl-pango
#
# includes module(s): SDL
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use sdl_64 = sdl-pango.spec
%endif

%if %arch_sse2
%include x86_sse2.inc
%use sdl_sse2 = sdl-pango.spec
%endif

%include base.inc
%use sdl = sdl-pango.spec

%define SUNWlibsdl	%(/usr/bin/pkginfo -q SUNWlibsdl && echo 1 || echo 0)

Name:			SFEsdl-pango
Summary: 		%{sdl.summary}
Version:		%{sdl.version}
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%if %SUNWlibsdl
BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl
%else
BuildRequires: SFEsdl-devel
Requires: SFEsdl
%endif

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%sdl_64.prep -d %name-%version/%_arch64
%endif

%if %arch_sse2
mkdir %name-%version/%sse2_arch
%sdl_sse2.prep -d %name-%version/%sse2_arch
%endif

mkdir %name-%version/%base_arch
%sdl.prep -d %name-%version/%base_arch

%build
%ifarch amd64 sparcv9
%sdl_64.build -d %name-%version/%_arch64
%endif

%if %arch_sse2
%sdl_sse2.build -d %name-%version/%sse2_arch
%endif

%sdl.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%sdl_64.install -d %name-%version/%_arch64
%endif

%if %arch_sse2
%sdl_sse2.install -d %name-%version/%sse2_arch
%endif

%sdl.install -d %name-%version/%base_arch

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif
%if %arch_sse2
%dir %attr (0755, root, bin) %{_libdir}/%{sse2_arch}
%{_libdir}/%{sse2_arch}/lib*.so*
%endif

%files devel
%defattr(-,root,bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc
%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*.pc
%endif
%if %arch_sse2
%dir %attr (0755, root, other) %{_libdir}/%{sse2_arch}/pkgconfig
%{_libdir}/%{sse2_arch}/pkgconfig/*.pc
%endif

%changelog
* Tue Mar 24 2009 - andras.barna@gmail.com
- remove %doc
* Wed Aug 15 2007 - dougs@truemail.co.th
- Initial version
