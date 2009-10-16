#
# spec file for package SFEopencore-amr
#
# includes module(s): opencore-amr
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use opencoreamr_64 = opencore-amr.spec
%endif

%if %arch_sse2
%define arch_opt --cpu=i686 --enable-mmx --enable-mmx2
%include x86_sse2.inc
%use opencoreamr_sse2 = opencore-amr.spec
%endif

%include base.inc
%use opencoreamr = opencore-amr.spec

Name:		SFEopencore-amr
Summary:	%{opencoreamr.summary}
Version:	%{opencoreamr.version}
URL:		%{opencoreamr.url}

SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%description
Library of OpenCORE Framework implementation of Adaptive Multi Rate Narrowband and Wideband speech codec.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%opencoreamr_64.prep -d %name-%version/%_arch64
%endif

%if %arch_sse2
mkdir %name-%version/%sse2_arch
%opencoreamr_sse2.prep -d %name-%version/%sse2_arch
%endif

mkdir %name-%version/%base_arch
%opencoreamr.prep -d %name-%version/%base_arch

%build
%ifarch amd64 sparcv9
%opencoreamr_64.build -d %name-%version/%_arch64
%endif

%if %arch_sse2
%opencoreamr_sse2.build -d %name-%version/%sse2_arch
%endif

%opencoreamr.build -d %name-%version/%base_arch


%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%opencoreamr_64.install -d %name-%version/%_arch64
%endif

%if %arch_sse2
%opencoreamr_sse2.install -d %name-%version/%sse2_arch
%endif

%opencoreamr.install -d %name-%version/%base_arch


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
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
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif
%if %arch_sse2
%dir %attr (0755, root, other) %{_libdir}/%{sse2_arch}/pkgconfig
%{_libdir}/%{sse2_arch}/pkgconfig/*.pc
%endif


%changelog
* Sun Oct 16 2009 - Milan Jurik
- Initial spec
