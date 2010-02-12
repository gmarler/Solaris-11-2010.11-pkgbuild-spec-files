#
# spec file for package gio
#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner:halton
#


%define real_name gio-standalone

Name:           gio
License:        LGPL
Group:          System/Libraries
Version:        0.1.2
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:            http://mail.gnome.org/archives/gtk-devel-list/2007-February/msg00062.html
Summary:        a set of daemons handling access to various file resources
Source:         http://ftp.gnome.org/pub/GNOME/sources/%{real_name}/0.1/%{real_name}-%{version}.tar.bz2
Patch1:		gio-01-strfunc.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

BuildRequires: gamin-devel
BuildRequires: glibmm-gpp >= 2.16

%description
The gio library is meant to be a part of glib. Its a generic I/O
library similar to e.g. java.io.*. Its a "modern" gobject-based
library using things like inheritance and interfaces. As such it can't
be in the main glib library (since that doesn't link to gobject).

%package devel
Summary: Headers for developing programs that will use %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the .pc files and header files needed for
developing with gio

%prep
%setup -q -n %{real_name}-%{version}
%patch1 -p1

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

#FXIME: call intltoolize will cause continuously make under po.
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
			%{gtk_doc_option}

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
%{_bindir}/gio-*
%{_datadir}/gio/
%{_libdir}/*.so.*
%{_libdir}/gio

%files devel
%defattr(-, root, root)
%{_includedir}/gio*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Feb 12 2010 - jchoi42@pha.jhu.edu
- patch to use G_STRFUNC instead of G_GNUC_PRETTY_FUNCTION, +glib check
* Fri Nov 16 2007 - nonsea@users.sourceforge.net
- Bump to 0.1.2. 
- Remove upstreamed patches void-return, solaris-statfs, pretty-func.
* Wed Nov 07 2007 - nonsea@users.sourceforge.net
- Initial version
