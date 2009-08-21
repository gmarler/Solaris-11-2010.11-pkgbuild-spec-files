#
# spec file for package SFElibmp4v2
#
# includes module(s): libmp4v2
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use libmp4v2_64 = libmp4v2.spec
%endif

%include base.inc
%use libmp4v2 = libmp4v2.spec

Name:                    SFElibmp4v2
Summary:                 %{libmp4v2.summary}
Version:                 %{libmp4v2.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

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
%libmp4v2_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libmp4v2.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%libmp4v2_64.build -d %name-%version/%_arch64
%endif

%libmp4v2.build -d %name-%version/%{base_arch}


%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%libmp4v2_64.install -d %name-%version/%_arch64
%endif

%libmp4v2.install -d %name-%version/%{base_arch}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Fri Aug 21 2009 - Milan Jurik
- Initial version
