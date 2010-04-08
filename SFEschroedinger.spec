#
# spec file for package SFElibschroedinger.spec
#
# includes module(s): libschroedinger
#

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use schroedinger_64 = schroedinger.spec
%endif

%if %arch_sse2
%define arch_opt --cpu=i686 --enable-mmx --enable-mmx2
%include x86_sse2.inc
%use schroedinger_sse2 = schroedinger.spec
%endif

%include base.inc

%use schroedinger = schroedinger.spec


Name:           SFElibschroedinger
Version:        %{schroedinger.version}
Summary:        %{schroedinger.summary}

Group:          %{schroediner.group}
License:        %{schroedinger.license}
URL:            %{schroedinger.url}

SUNW_BaseDir:            %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-build

%description
Library for decoding and encoding video in the Dirac format. It is implemented
in ANSI C and optimized through the us of liboil. libschro is written as a
collaboration between the BBC Research and Development, David Schleef and
Fluendo.

%include default-depend.inc

BuildRequires:  SFEorc
BuildRequires:  SUNWgtk-doc
BuildRequires:  SUNWliboil
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
%schroedinger_64.prep -d %name-%version/%_arch64
%endif

%if %arch_sse2
mkdir %name-%version/%sse2_arch
%schroedinger_sse2.prep -d %name-%version/%sse2_arch
%endif

mkdir %name-%version/%base_arch
%schroedinger.prep -d %name-%version/%base_arch

%build
%ifarch amd64 sparcv9
%schroedinger_64.build -d %name-%version/%_arch64
%endif

%if %arch_sse2
%schroedinger_sse2.build -d %name-%version/%sse2_arch
%endif

%schroedinger.build -d %name-%version/%base_arch


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%schroedinger_64.install -d %name-%version/%_arch64
%endif

%if %arch_sse2
%schroedinger_sse2.install -d %name-%version/%sse2_arch
%endif

%schroedinger.install -d %name-%version/%base_arch

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libschroedinger-1.0.so.*
%if %arch_sse2
%{_libdir}/%{sse2_arch}/libschroedinger-1.0.so.*
%endif
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/libschroedinger-1.0.so.*
%endif

%files devel
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/schroedinger-1.0.pc
%if %arch_sse2
%dir %attr (0755, root, other) %{_libdir}/%{sse2_arch}/pkgconfig
%{_libdir}/%{sse2_arch}/pkgconfig/*.pc
%endif
%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*.pc
%endif
%{_libdir}/libschroedinger-1.0.so
%if %arch_sse2
%{_libdir}/%{sse2_arch}/libschroedinger-1.0.so
%endif
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/libschroedinger-1.0.so
%endif
%{_includedir}/schroedinger-1.0/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/gtk-doc
%dir %attr (0755, root, bin) %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/schroedinger

%changelog
* Wed May 7 2008 Christian Schaller <christian.schaller@collabora.co.uk>
- Added Schrovirtframe.h

* Fri Feb 22 2008 David Schleef <ds@schleef.org>
- Update for 1.0

* Fri Feb 1 2008 Christian F.K. Schaller <christian.schaller@collabora.co.uk>
- add schromotionest.h
- remove schropredict.h

* Tue Jan 22 2008 Christian F.K. Schaller <christian.schaller@collabora.co.uk>
- Update for latest changes

* Thu Apr 05 2007 Thomas Vander Stichele <thomas at apestaart dot org>
- Further updates.

* Thu Apr 27 2006 Christian F.K. Schaller <christian@fluendo.com>
- Updates for carid -> schroedinger change
