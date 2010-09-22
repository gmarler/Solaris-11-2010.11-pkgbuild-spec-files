#
# spec file for package SFElibnice
#
# includes module(s): libnice
#

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use libnice_64 = libnice.spec
%endif

%use libnice = libnice.spec

Name:           SFElibnice
Version:        %{libnice.version}
Summary:        %{libnice.summary}

Group:          %{libnice.group}
License:        %{libnice.license}
URL:            %{libnice.url}

SUNW_BaseDir:            %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-build

%description
Libnice is an implementation of the IETF's Interactive Connectivity
Establishment (ICE) standard (RFC 5245) and the Session Traversal Utilities for
NAT (STUN) standard (RFC 5389). It provides a GLib-based library, libnice and a
Glib-free library, libstun as well as GStreamer elements. 

%include default-depend.inc

BuildRequires:  SUNWgnome-media-devel

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
%libnice_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%base_arch
%libnice.prep -d %name-%version/%base_arch

%build
%ifarch amd64 sparcv9
%libnice_64.build -d %name-%version/%_arch64
%endif

%libnice.build -d %name-%version/%base_arch


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%libnice_64.install -d %name-%version/%_arch64
%endif

%libnice.install -d %name-%version/%base_arch

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libnice-1.0.so.*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/libnice-1.0.so.*
%endif

%files devel
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/libnice-1.0.pc
%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*.pc
%endif
%{_libdir}/libnice-1.0.so
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/libnice-1.0.so
%endif
%{_includedir}/nice-1.0/*

%changelog
* Mon Sep 20 2010 - Albert Lee <trisk@opensolaris.org>
- Initial spec
