#
# spec file for package telepathy-glib
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: elaine
#

Name:			  telepathy-glib
License:		GPL
Group:			Applications/Internet
Version:		0.7.19
Release:	 	1
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:	  A GLib-based helper library for clients and connection managers	
Source:			http://telepathy.freedesktop.org/releases/%{name}/%{name}-%{version}.tar.gz
# date:2008-11-04 owner:rickju type:branding bugster:6710470
Patch1:		telepathy-glib-01-struct.diff
URL:			   http://telepathy.freedesktop.org/wiki/Telepathy%20GLib
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/telepathy-glib
Autoreqprov: on
Prereq:      /sbin/ldconfig

#BuildPreReq:   openssl-devel >= 0.9.8a, ncurses-devel
#BuildRequires: openssl-devel >= %{openssl_version}

%description
GLib-based helper library for clients and connection managers

%package devel
Summary:      A GLib-based helper library for clients and connection managers	
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

rm -rf m4/lt*.m4
rm -rf m4/libtool.m4

CFLAGS="$RPM_OPT_FLAGS"			            \
./autogen.sh --prefix=%{_prefix}        \
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
%{_libdir}/lib*.so.*
%{_datadir}/gtk-doc/*/*/*

%files devel
%defattr(-, root, root)
%{_libdir}/pkgconfig/*.pc
%attr(755, root, root) %{_includedir}/telepathy-1.0/*

%changelog
* Thu Mar 12 2009 - elaine.xiong@sun.com
- Move from spec-files/trunk.
* Tus Dec 08 2008 - rick.ju@sun.com
- bump to 0.7.19
* Wed Nov 05 2008 - rick.ju@sun.com
- Initial spec-file created
