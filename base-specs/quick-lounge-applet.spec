#
# spec file for package quick-lounge-applet
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%define OSR LFI#105446 (gnome Exec. summary):n/a

Name:         quick-lounge-applet
License:      GPL
Group:        Productivity/Graphics/Viewers
Version:      2.14.0
Release:      2
Distribution: Java Desktop System
Vendor:       Gnome Community
Summary:      Quick Lounge Panel Applet
Source:       http://ftp.gnome.org/pub/GNOME/sources/quick-lounge-applet/2.14/%{name}-%{version}.tar.bz2
%if %build_l10n
Source1:                 l10n-configure.sh
%endif
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/quick-lounge-applet
Autoreqprov:  on

%define gnome_vfs_version 2.4.0
%define libgnome_version 2.4.0
%define libgnomeui_version 2.4.0.1
%define gnome_panel_version 2.4.0
%define gnome_desktop_version 2.4.0
%define gnome_menus_version 2.12.0

Requires:      gnome-vfs >= %{gnome_vfs_version}
Requires:      libgnome >= %{libgnome_version}
Requires:      libgnomeui >= %{libgnomeui_version}
Requires:      gnome-panel >= %{gnome_panel_version}
Requires:      gnome-desktop >= %{gnome_desktop_version}
Requires:      gnome-menus >= %{gnome_menus_version}
BuildRequires: gnome-vfs-devel >= %{gnome_vfs_version}
BuildRequires: libgnome-devel >= %{libgnome_version}
BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: gnome-panel-devel >= %{gnome_panel_version}
BuildRequires: gnome-desktop-devel >= %{gnome_desktop_version}
BuildRequires: gnome-menus-devel >= %{gnome_menus_version}

%description
Quick Lounge Applet allows you to group launchers on your panel.

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

libtoolize --force
intltoolize --force --copy --automake

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS" \
  ./configure \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir} \
    --libexecdir=%{_libexecdir} \
    --localstatedir=/var/lib
make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL  

rm -rf $RPM_BUILD_ROOT/var


%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="quick-lounge.schemas"
for S in $SCHEMAS; do
        gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%files
%doc AUTHORS COPYING ChangeLog NEWS README
%defattr (-, root, root)
%{_datadir}/pixmaps/*.png
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/gnome-2.0/ui/*
%{_datadir}/quick-lounge/*
%{_sysconfdir}/gconf/schemas/*.schemas
%{_libdir}/bonobo/servers/*
%{_datadir}/gnome/help/quick-lounge/*
%{_datadir}/omf/%{name}/*.omf
%{_libexecdir}/*

%changelog
* Tue Dec 07 2010 - brian.cameron@oracle.com
- Created.
