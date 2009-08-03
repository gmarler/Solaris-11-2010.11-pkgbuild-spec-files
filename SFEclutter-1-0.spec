#
#
# spec file for package SFEclutter-1-0
#
# includes module(s): clutter
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: bewitche

%include Solaris.inc

%use clutter = clutter-1-0.spec

Name:                    SFEclutter-1-0
Summary:                 clutter - a library for creating fast, visually rich and animated graphical user interfaces.
Version:                 %{clutter.version}
URL:                     http://www.clutter-project.org/
SUNW_BaseDir:            %{_basedir}

%ifnarch sparc
#the packages are only on x86
# ============================================

BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-base-libs
Requires: SUNWxorg-mesa
Requires: SFEgobject-introspection
Requires: SFEgir-repository
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SFEgobject-introspection-devel
BuildRequires: SFEgir-repository

%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-base-libs-devel

%prep
rm -rf %name-%version
mkdir %name-%version
%clutter.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
%clutter.build -d %name-%version

%install
%clutter.install -d %name-%version
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

rm -rf $RPM_BUILD_ROOT%{_datadir}/gtk-doc

#cd %{_builddir}/%name-%version/sun-manpages
#make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc -d clutter-%{clutter.version} AUTHORS README
%doc(bzip2) -d clutter-%{clutter.version} ChangeLog COPYING NEWS
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/girepository-1.0
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gir-1.0

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

# endif for "ifnarch sparc"
%endif

%changelog
* Mon Aug 03 2009  Brian.Cameron@sun.com
- Bump to 1.0.
* Thu Mar 26 2009  Chris.wang@sun.com
- Correct copyright file in file section
* Tue Mar 24 2009  chris.wang@sun.com
- Add SUNWxorg-mesa to Require
* Fri Feb 20 2009  chris.wang@sun.com
- Add manpage
* Tue Jul  1 2008  chris.wang@sun.com 
- Initial build.

