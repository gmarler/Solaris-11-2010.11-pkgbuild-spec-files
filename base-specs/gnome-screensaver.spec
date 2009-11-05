#
# spec file for package gnome-screensaver 
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: me, me, me, I want it!
#
Name:         gnome-screensaver
License:      GPL
Group:        System/GUI/GNOME
Version:      2.28.0
Release:      1
Distribution: Java Desktop System
Vendor:	      Sun Microsystems, Inc.
Summary:      The GNOME screen saver 
Source:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.28/%{name}-%{version}.tar.bz2
# date:2009-05-11 owner:johnf type:feature
Patch1:       gnome-screensaver-01-pam-audit.diff
URL:          www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Autoreqprov:  on

# TODO: Get full list of dependencies.
# See: http://packages.ubuntu.com/breezy/gnome/gnome-screensaver
%define dbus_version 0.30
%define libxml_version 2.6.0
%define GConf_version 2.6.1
%define gdk_version 2.7.0
%define gtk2_version 2.7.0
%define gnome_vfs_version 2.6.0
%define libgnomeui_versin 2.6.0
%define glade_version 2.5.0
%define libgnome_menu_version 2.11.1
%define libexif_version 0.6.12
Requires:	dbus >= %{dbus_version}
Requires:	libxml >= %{libxml_version}
Requires:	GConf >= %{GConf_version}
Requires:	gdk >= %{gdk_version}
Requires:	gtk2 >= %{gtk2_version}
Requires:	gnome-vfs >= %{gnome_vfs_version}
Requires:	libgnomeui >= %{libgnomeui_version}
Requires:	glade >= %{glade_version}
Requires:	gnome-menus >= %{libgnome_menu_version}
Requires:	libexif >= %{libexif_version}
BuildRequires: gtk2-devel >= %{gtk2_version}

%description
gnome-screensaver is a screen saver and locker that aims to have
simple, sane, secure defaults and be well integrated with the desktop.
It is designed to support:
        * the ability to lock down configuration settings
        * translation into many languages
        * user switching

%prep
%setup -q
%patch1 -p1

# Fix for 332967.
for po in po/*.po; do
  dos2unix -ascii $po $po
done

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


libtoolize --force
intltoolize --force --copy
aclocal $ACLOCAL_FLAGS
autoconf
autoheader
automake -a -c -f
./configure \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir} \
    --libexecdir=%{_libexecdir} \
    --localstatedir=/var/lib \
    --enable-locking
make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%{_bindir}/*
%{_datadir}/*
%{_libdir}/*

%changelog
* Tue May 19 2009 - brian.cameron@sun.com
- Bump to 2.26.1.  Add patch gnome-screensaver-01-pam-audit.diff which
  John Fischer wrote to add Sun Audit and Sun PAM interfaces.

* Tue Dec 23 2008 - jedy.wang@sun.com
- Bump to 2.24.1.
- Remove patch 01-gthread.diff.

* Tue Mar 11 2008 - damien.carbery@sun.com
- Bump to 2.22.0.

* Thu Jan 31 2008 - damien.carbery@sun.com
- Bump to 2.21.6.

* Fri Jan 11 2008 - damien.carbery@sun.com
- Add patch 01-gthread to Add gthread-2 to list of modules add to
  GNOME_SCREENSAVER CFLAGS and LIBS. This is a better fix than adding gthread-2
  to the GConf .pc file. Bugzilla 508547.

* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.20.0.

* Tue Aug 28 2007 - damien.carbery@sun.com
- Bump to 2.19.7. Remove upstream patch 01-X-libs.

* Tue Jul 31 2007 - damien.carbery@sun.com
- Bump to 2.19.6.

* Wed May 09 2007 - damien.carbery@sun.com
- Bump to 2.19.1.1. Add patch 01-X-libs to include libX11 and libXext during
  build. Fixes 437225 .

* Thu Apr 12 2007 - damien.carbery@sun.com
- Bump to 2.18.1.

* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 2.18.0.

* Tue Feb 27 2007 - damien.carbery@sun.com
- Bump to 2.17.8.

* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.17.7.

* Mon Jan 22 2007 - damien.carbery@sun.com
- Bump to 2.17.6.

* Tue Jan 09 2007 - damien.carbery@sun.com
- Bump to 2.17.5.

* Tue Dec 19 2006 - damien.carbery@sun.com
- Bump to 2.17.4.

* Thu Dec 07 2006 - damien.carbery@sun.com
- Bump to 2.17.3.

* Mon Nov 20 2006 - damien.carbery@sun.com
- Bump to 2.17.2.

* Mon Oct 23 2006 - glynn.foster@sun.com
- Remove src-libs patch since it's now upstream.

* Tue Oct 03 2006 - damien.carbery@sun.com
- Bump to 2.16.1.

* Tue Sep 05 2006 - damien.carbery@sun.com
- Bump to 2.16.0.

* Tue Aug 22 2006 - brian.cameron@sun.com
- Bump to 2.15.7.

* Tue Aug 08 2006 - brian.cameron@sun.com
- Bump to 2.15.6.

* Tue Jul 25 2006 - damien.carbery@sun.com
- Bump to 2.15.5.

* Thu Apr 13 2006 - dermot.mccluskey@sun.com
- replace sed with dos2unix to work around ^M problem in SVN

* Mon Apr 10 2006 - damien.carbery@sun.com
- Bump to 2.14.1.

* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.14.0.

* Thu Mar  2 2006 - damien.carbery@sun.com
- Correct sed conversion code.

* Wed Mar  1 2006 - damien.carbery@sun.com
- Use sed to convert po files from DOS to Unix line ending format.

* Tue Feb 28 2006 - damien.carbery@sun.com
- Bump to 2.13.92.

* Wed Feb 15 2006 - damien.carbery@sun.com
- Bump to 2.13.91.

* Tue Jan 31 2006 - damien.carbery@sun.com
- Bump to 2.13.90.

* Wed Jan 18 2006 - damien.carbery@sun.com
- Add intltoolize call.

* Sun Jan 15 2006 - damien.carbery@sun.com
- Bump to 0.0.24.

* Mon Nov 28 2005 - laca@sun.com
- update to 0.0.20

* Fri Nov 04 2005 - damien.carbery@sun.com
- Bump to 0.0.18. Remove autofoo and patches.

* Tue Nov 01 2005 - damien.carbery@sun.com
- Add autofoo for configure.ac patch.

* Wed Oct 26 2005 - damien.carbery@sun.com
- Bump to 0.0.17.

* Mon Oct 24 2005 - damien.carbery@sun.com
- Add patches, add 'locale.h' to two files and extra libs to src/Makefile.*.

* Fri Oct 21 2005 - damien.carbery@sun.com
- Initial version.
