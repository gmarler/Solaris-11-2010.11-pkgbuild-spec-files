#
# spec file for package empathy
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner:rickju
#

Name:            empathy
License:         GPL
Group:           Applications/Internet
Version:         2.25.2
Release:         1
Distribution:    Java Desktop System
Vendor:          Sun Microsystems, Inc.
Summary:         A Gnome IM/voice/video client
Source:          http://download.gnome.org/sources/empathy/2.25/%{name}-%{version}.tar.gz

# date:2008-06-04 owner:rickju type:branding
Patch1:         empathy-01-branding.diff

URL:            http://live.gnome.org/Empathy
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Docdir:         %{_defaultdocdir}/empathy
Autoreqprov:    on
Prereq:         /sbin/ldconfig

%description
A Gnome IM/voice/video client reusing Gossip's UI and using Nokia's Mission Control

%package devel
Summary:      A Gnome IM/voice/video client
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

CFLAGS="$RPM_OPT_FLAGS"                   \
./autogen.sh --prefix=%{_prefix}          \
              --mandir=%{_mandir}         \
              --libdir=%{_libdir}         \
              --libexecdir=%{_libexecdir} \
              --sysconfdir=%{_sysconfdir} \
              --enable-megaphone=no       \
              --enable-python=no          \
              --enable-nothere=no         \
              --disable-tests

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
%{_bindir}/*
%{_libdir}/lib*.so*
%{_libdir}/bonobo/*
%{_libdir}/python*
%{_libexecdir}/megaphone-applet
%{_libexecdir}/nothere-applet
%{_datadir}/locale/*/*/*
%{_datadir}/icons/*
%{_datadir}/empathy/*
%{_datadir}/applications/*
%{_datadir}/mission-control/*
%{_datadir}/man/man1/*
%attr(755, root, root) %{_datadir}/gtk-doc/html/libempathy/*
%attr(755, root, root) %{_datadir}/gtk-doc/html/libempathy-gtk/*
%attr(755, root, root) %{_datadir}/gnome/help/empathy/*
%attr(755, root, root) %{_datadir}/omf/empathy/*
%{_sysconfdir}/gconf/schemas/*

%files devel
%defattr(-, root, root)
%{_libdir}/pkgconfig/*.pc
%attr(755, root, root) %{_includedir}/libempathy/*
%attr(755, root, root) %{_includedir}/libempathy-gtk/*

%changelog
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 2.25.2
* Fri Nov 28 2008 - rick.ju@sun.com
- disable megaphone
* Wed Nov 05 2008 - rick.ju@sun.com
- Initial spec-file created
