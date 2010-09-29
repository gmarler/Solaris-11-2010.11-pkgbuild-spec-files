#
# spec file for package telepathy-mission-control
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: 
# bugdb: https://bugs.freedesktop.org/
#

Name:     telepathy-mission-control
License:  GPL
Group:    Applications/Internet
Version:  5.6.0
Release:  1
Distribution: Java Desktop System
Vendor:    Sun Microsystems, Inc.
Summary:   Control the launching of connection managers and clients
Source:    http://dl.sourceforge.net/mission-control/%{name}-%{version}.tar.gz

# date:2010-09-29 owner:jefftsai bugid:30447 type:bug
Patch1:   telepathy-mission-control-01-void.diff
# date:2010-09-29 owner:jefftsai bugid:30448 type:bug
Patch2:   telepathy-mission-control-02-account-storage.diff

URL:         http://mission-control.sourceforge.net/
BuildRoot:   %{_tmppath}/%{name}-%{version}-build
Docdir:    %{_defaultdocdir}/telpathy-mission-control
Autoreqprov: on
Prereq:      /sbin/ldconfig

# BuildPreReq: openssl-devel >= 0.9.8a, ncurses-devel

%define openssl_version 0.9.8a
BuildRequires: openssl-devel >= %{openssl_version}

%description
W3m is a pager adapted to World Wide Web. W3m is a text-based WWW
browser as well as a pager.

%package devel
Summary:      Control the launching of connection managers and clients
Group:        System/GUI/GNOME
Autoreqprov:  on
Requires:     %name = %version

%prep
%setup -q
%patch1 -p1
%patch2 -p1

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

CFLAGS="$RPM_OPT_FLAGS"                 \
./configure --prefix=%{_prefix}         \
            --mandir=%{_mandir}         \
            --libdir=%{_libdir}         \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
	    --enable-keyring=yes

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr (-, root, bin)
%{_bindir}/*
%{_libdir}/lib*.so*
%{_datadir}/gtk-doc/*/*/*
%{_libexecdir}/mission-control
%{_datadir}/dbus-1/*

%files devel
%defattr(-, root, root)
%{_libdir}/pkgconfig/*.pc
%attr(755, root, root) %{_includedir}/libmcclient
%attr(755, root, root) %{_includedir}/libmissioncontrol
%attr(755, root, root) %{_includedir}/mission-control

%changelog
* Wed Sep 29 2010 - jeff.cai@oracle.com
- Bump to 5.6.0
- Add patch -01-void to fix bug #30447
- Add patch -02-account-storage to fix bug #30448
* Thu Mar 12 2009 - elaine.xiong@sun.com
- Move from spec-files/trunk.
* Wed Nov 05 2008 - rick.ju@sun.com
- Initial spec-file created
