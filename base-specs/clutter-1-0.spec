#
# spec file for package clutter-1-0
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# bugdb: http://bugzilla.openedhand.com
#
# Owner: yippi
#

Name:         clutter-1-0
License:      LGPL
Group:        System/Libraries
Version:      1.0.0
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      clutter - a library for creating fast, visually rich and animated graphical user interfaces.
Source:	  http://www.clutter-project.org/sources/clutter/1.0/clutter-%{version}.tar.bz2

URL:          http://www.clutter-project.org/
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%description

%prep
%setup -q -n clutter-%version

%build
export CFLAGS="%{optflags} -I/usr/X11/include"
export CXXFLAGS="%{?cxx_optflags}"
export LDFLAGS="%{?_ldflags} -L/usr/X11/lib -R/usr/X11/lib -lX11"
./configure --prefix=%{_prefix}              \
            --libdir=%{_libdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --disable-static                 \
            --enable-gtk-doc			
make 

%install
#rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%changelog
* Mon Aug 03 2009 - brian.cameron@sun.com
- Bump to 1.0.
* Tue Jul 07 2009 - brian.cameron@sun.com
- Created with 0.9.6.

