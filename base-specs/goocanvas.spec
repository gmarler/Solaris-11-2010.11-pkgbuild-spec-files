#
# spec file for package goocanvas
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner:halton
#

Name:           goocanvas
License:        LGPL
Group:          System/Libraries
Version:        0.14
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:            http://sourceforge.net/projects/goocanvas
Summary:        A Cairo Canvas Widget for GTK+
Source:         http://download.gnome.org/sources/%{name}/%{version}/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
BuildRequires:  autoconf >= 2.50
BuildRequires:  automake >= 1:1.7
BuildRequires:  cairo-devel
BuildRequires:  glib2-devel >= 1:2.10.0
BuildRequires:  gtk+2-devel >= 2:2.10.0
BuildRequires:  gtk-doc >= 1.8
BuildRequires:  libtool
BuildRequires:  pkgconfig
Requires:       glib2 >= 1:2.10.0
Requires:       gtk+2 >= 2:2.10.0

%description
GooCanvas is a new canvas widget for GTK+ that uses the Cairo 2D
library for drawing. It has a model/view split, and uses interfaces
for canvas items and views, so you can easily turn any application
object into canvas items.

%package devel
Summary: Headers for developing programs that will use %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the static libraries and header files needed for
developing with tracker

%prep
%setup -q

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

#intltoolize --force --automake
libtoolize --force
aclocal $ACLOCAL_FLAGS -I .
autoheader
automake -a -c -f
autoconf

./configure --prefix=%{_prefix} \
			--bindir=%{_bindir} \
			--mandir=%{_mandir} \
			--libdir=%{_libdir} \
			--datadir=%{_datadir} \
			--includedir=%{_includedir} \
			--sysconfdir=%{_sysconfdir} \
			%{gtk_doc_option} \

make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-, root, root)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/*.so.*
%{_datadir}/gtk-doc/html/*

%files devel
%defattr(-, root, root)
%attr(755,root,root) %{_libdir}/libgoocanvas.so
%{_includedir}/goocanvas-1.0
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Apr 24 2009 - brian.cameron@sun.com
- Bump to 0.14.
* Wed Sep 10 2008 - halton.huo@sun.com
- Bump to 0.11.
* Mon Sep 01 2008 - halton.huo@sun.com
- Add patch remove-GtkSignalFunc.diff to fix build issue under glib 2.17.7
* Mon May 26 2008 - nonsea@users.sourceforge.net
- change SOURCE to download.gnome.org
* Tue May 13 2008 - nonsea@users.sourceforge.net
- Bump to 0.10.
* Tue Dec 11 2007 - nonsea@users.sourceforge.net
- Initial version.
