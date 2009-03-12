#
# spec file for package libtelepathy
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: elaine
#

Name:			  libtelepathy
License:		LGPL
Group:			Applications/Internet
Version:		0.3.3
Release:	 	1
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:	  A GLib library to ease writing Telepathy clients in glib
Source:			http://telepathy.freedesktop.org/releases/%{name}/%{name}-%{version}.tar.gz

# date:2008-11-04 owner:rickju type:branding
Patch1:		libtelepathy-01-check-compat.diff

URL:			   http://telepathy.freedesktop.org/wiki
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/libtelepathy
Autoreqprov: on
Prereq:      /sbin/ldconfig

%description
A GLib library to ease writing Telepathy clients in glib

%package devel
Summary:      A GLib library to ease writing Telepathy clients in glib
Group:        System/GUI/GNOME
Autoreqprov:  on
Requires:     %name = %version

%prep
%setup -q
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

CFLAGS="$RPM_OPT_FLAGS"			           \
./configure --prefix=%{_prefix}        \
            --mandir=%{_mandir}         \
            --libdir=%{_libdir}         \
            --sysconfdir=%{_sysconfdir}

make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%{_libdir}/lib*.so*

%files devel
%defattr(-, root, root)
%{_libdir}/pkgconfig/*.pc
%attr(755, root, root) %{_includedir}/telepathy-1.0/*

%changelog
* Thu Mar 12 2009 - elaine.xiong@sun.com
- Move from spec-files/trunk.
* Wed Nov 05 2008 - rick.ju@sun.com
- Initial spec-file created
