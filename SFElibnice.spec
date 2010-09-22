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

Requires: SUNWlxml
Requires: SUNWglib2
Requires: SUNWgnome-media
BuildRequires: SUNWgtk-doc
BuildRequires: SUNWglib2-devel
BuildRequires: SUNWgnome-media-devel

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

%if %{!?_without_gtk_doc:0}%{?_without_gtk_doc:1}
rm -rf $RPM_BUILD_ROOT%{_datadir}/gtk-doc
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/stunbdc
%{_bindir}/stund
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libnice.so.*
%{_libdir}/gstreamer-*/*.so
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/libnice.so.*
%{_libdir}/%{_arch64}/gstreamer-*/*.so
%endif

%files devel
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/nice.pc
%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/nice.pc
%endif
%{_libdir}/libnice.so
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/libnice.so
%endif
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/stun
%{_includedir}/nice
%if %{!?_without_gtk_doc:1}%{?_without_gtk_doc:0}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc
%endif

%changelog
* Tue Sep 21 2010 - Albert Lee <trisk@opensolaris.org>
- Fix %files, %install, and dependencies
* Mon Sep 20 2010 - Albert Lee <trisk@opensolaris.org>
- Initial spec
