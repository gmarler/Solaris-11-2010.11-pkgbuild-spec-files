#
# spec file for package SFEcairo-dock
# Mon premier package, soyez indulgent...
# Gilles Dauphin
#

%include Solaris.inc

%if %(pkginfo -q FSWxorg-clientlibs && echo 1 || echo 0)
# FOX
%define old_x11 0
%else
# Nevada X
%define old_x11     %(pkgchk -l SUNWxwinc 2>/dev/null | grep compositeproto >/dev/null && echo 0 || echo 1)
%endif

#%define gnome_2_20  %(pkg-config --atleast-version=2.19.0 libgnome-2.0 && echo 1 || echo 0)

Name:           SFEcairo-dock
Summary:        cairo-dock
Version:        20080408
Source:		http://public.enst.fr/SFE/SOURCES/cairo-dock-sources-%{version}.tar.gz
Patch1:		cairo-dock-patch01-configure.diff
Patch2:		cairo-dock-patch02-Makefile.diff
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include	default-depend.inc
#Requires:	%name-root
Requires: 	SUNWpng
Requires: 	SUNWdbus
Requires: 	SUNWgnome-base-libs
Requires: 	SUNWgnome-wm
BuildRequires: 	SUNWpng-devel
BuildRequires: 	SUNWdbus-devel
BuildRequires: 	SUNWgnome-base-libs-devel
BuildRequires: 	SUNWgnome-wm-devel
BuildRequires: 	SUNWcompiz
BuildRequires: 	CBEgettext
# TODO require at least a 3D desktop

#%package root
#Summary:         %summary - platform dependent files, / filesystem
#SUNW_BaseDir:            /
#%include default-depend.inc

%package devel
Summary:		 %summary - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:		 %name

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:        %{name}
%endif

%prep
%setup -q -c -n %{name}
cd cairo-dock
%patch1 -p1
cd src
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

PROTO_LIB=$RPM_BUILD_DIR/%{name}/usr/X11/lib
PROTO_INC=$RPM_BUILD_DIR/%{name}/usr/X11/include
PROTO_PKG=$RPM_BUILD_DIR/%{name}/usr/X11/lib/pkgconfig

export PKG_CONFIG_PATH="$PROTO_PKG"
export CC=/usr/sfw/bin/gcc
export LDFLAGS="-L$PROTO_LIB -L/usr/X11/lib -R/usr/X11/lib"
export CFLAGS=-D__EXTENSIONS__

cd cairo-dock

rm -f config.* configure configure.lineno intltool-extract intltool-merge intltool-update libtool ltmain.sh Makefile.in Makefile aclocal.m4 install-sh install depcomp missing compile cairo-dock.pc stamp-h1 cairo-dock.conf 
rm -rf autom4te.cache src/.deps src/.libs src/Makefile src/Makefile.in po/Makefile po/Makefile.in po/*.gmo src/*.o src/*.lo src/*.la

autoreconf -isf 

export CC=/usr/sfw/bin/gcc
export LDFLAGS="-L$PROTO_LIB -L/usr/X11/lib -L/usr/openwin/lib -R/usr/X11/lib -R/usr/openwin/lib -lX11 -lXext"

/bin/bash ./configure CONFIG_SHELL=/bin/bash --prefix=%{_prefix}		\
	    --bindir=%{_bindir}         \
	    --sysconfdir=%{_sysconfdir}	\
	    --libdir=%{_libdir}         \
            --includedir=%{_includedir} \
	    --datadir=%{_datadir}	

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig

cd cairo-dock
make install DESTDIR=$RPM_BUILD_ROOT
cd ..


%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/cairo-dock
%dir %attr(0755, root, other) %{_datadir}/cairo-dock/gauges
%dir %attr(0755, root, other) %{_datadir}/cairo-dock/gauges/battery
%dir %attr(0755, root, other) %{_datadir}/cairo-dock/gauges/old-square
%dir %attr(0755, root, other) %{_datadir}/cairo-dock/gauges/radium
%dir %attr(0755, root, other) %{_datadir}/cairo-dock/gauges/radium-fuel
%dir %attr(0755, root, other) %{_datadir}/cairo-dock/gauges/rainbow
%dir %attr(0755, root, other) %{_datadir}/cairo-dock/gauges/tomato
%dir %attr(0755, root, other) %{_datadir}/cairo-dock/gauges/turbo-night
%dir %attr(0755, root, other) %{_datadir}/cairo-dock/gauges/turbo-night-dual
%dir %attr(0755, root, other) %{_datadir}/cairo-dock/gauges/turbo-night-fuel
%{_datadir}/cairo-dock/gauges/*/*
%dir %attr(0755, root, other) %{_datadir}/cairo-dock/themes
%dir %attr(0755, root, other) %{_datadir}/cairo-dock/themes/_default_
%dir %attr(0755, root, other) %{_datadir}/cairo-dock/themes/_default_/launchers
%{_datadir}/cairo-dock/themes/*/*/*
%{_datadir}/cairo-dock/*.conf
%{_datadir}/cairo-dock/*.png
%{_datadir}/cairo-dock/*.svg
%{_datadir}/cairo-dock/readme-default-view
%{_datadir}/cairo-dock/ChangeLog.txt
%{_datadir}/cairo-dock/License
%{_datadir}/cairo-dock/themes/_default_/readme
%{_datadir}/cairo-dock/themes/_default_/background-snow.svg
%{_datadir}/cairo-dock/themes/_default_/separateur.svg
%{_datadir}/cairo-dock/themes/_default_/preview
%{_datadir}/cairo-dock/themes/_default_/cairo-dock.conf


%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/cairo-dock
%dir %attr (0755, root, bin) %{_includedir}/cairo-dock/cairo-dock
%{_includedir}/cairo-dock/*.h
%{_includedir}/cairo-dock/cairo-dock/*.h
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Aug 04 2009 - Gilles Dauphin ( Gilles POINT Dauphin A enst POINT fr)
- require CBEgettext , SUNWgnu-gettext is not enough.
* April 22 2008 - Gilles Dauphin ( Gilles POINT Dauphin A enst POINT fr)
- Initial spec
