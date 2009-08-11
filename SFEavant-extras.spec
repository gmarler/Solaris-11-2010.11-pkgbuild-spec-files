#
# Spec file for package awn-extras
#
# Future versions of awn-extras WILL require Python > 2.4...
#

%include Solaris.inc

%define X11_DIR %{_prefix}/X11
%define source_name awn-extras-applets
%define SUNWavant %(/usr/bin/pkginfo -q SUNWavant && echo 1 || echo 0)

Name:           SFEavant-extras
Summary:        Avant Window Navigator Extras - Applets and Plugins
Version:        0.3.2.2
Source:		http://launchpad.net/awn-extras/0.2/%{version}/+download/awn-extras-applets-%{version}.tar.gz
License:        GPL v3, LGPL v2, Apache, Other
URL:            http://launchpad.net/awn-extras/
SUNW_BaseDir:   %{_basedir}
SUNW_Copyright: %{name}.copyright
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

# Patch notes.
#
# Patch1 ought to go away at 0.3.3, when alsaaudio is not a "hard" requirement at configure-time. At this time, the volume applet is ALSA-only.
# Patch2 ought to go away at 0.3.9, when proper backend detection is done.
# Patch3 is because the mount applet relies on /etc/fstab (which isn't on Solaris) and doesn't know about ZFS.
# Patch4 is due to file-browser-launcher trying to enumerate filesystems via /etc/fstab.
# Patch5 is because ThinkHDAPS is Linux-specific.
# Patch6 may be unneeded with a *Kit upgrade. Error: "gnomevfs.GenericError: Generic error"
# Patch7 is due to too-new python syntax, and can go away with a move to 2.6.
# Patch8 is likely to be unneeded with 0.3.9
# Patch9 is not yet diagnosed.
# Patch10 is not yet diagnosed.
# Patch11 is not yet diagnosed.
# Patch12 can probably be reworked or removed with python 2.6.

Patch1:         avant-extras-01-alsaaudio.diff
Patch2:         avant-extras-02-disable-volume-applet.diff
Patch3:         avant-extras-03-disable-mount-applet.diff
Patch4:         avant-extras-04-disable-file-browser-launcher.diff
Patch5:         avant-extras-05-disable-thinkhdaps.diff
Patch6:         avant-extras-06-disable-stacks.diff
Patch7:         avant-extras-07-disable-cairo-clock.diff
Patch8:         avant-extras-08-disable-cairo-main-menu.diff
Patch9:         avant-extras-09-disable-cpufreq-monitor.diff
Patch10:        avant-extras-10-disable-desktop-manager.diff
Patch11:        avant-extras-11-disable-digital-clock.diff
Patch12:        avant-extras-12-rss-sqlite.diff

%ifnarch sparc
# these packages are only available on i386/x64
# =============================================

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include	default-depend.inc
Requires:       SFEtomboy
Requires:       SUNWbash
Requires:       SUNWcompiz
Requires:       SUNWdbus
Requires:       SUNWdesktop-cache
Requires:       SUNWdesktop-search
Requires:       SUNWgnome-themes
Requires:       SUNWgtk2
Requires:       SFEgdata-python
Requires:       SFEpython-dateutil
Requires:       SFEpython-feedparser
Requires:       SFEpython-sqlalchemy
Requires:       SFEpython-vobject
Requires:       SFEpython-xlib
Requires:       SUNWPython
Requires:       SUNWgnome-python-desktop
Requires:       SUNWgnome-python-extras
Requires:       SUNWgnome-python-libs
Requires:       SUNWgst-python
Requires:       SUNWpython-notify
Requires:       SUNWpython-xdg
Requires:       SUNWsexy-python
# Requires:       SFEgdata-python26
# Requires:       SFEpython-vobject26
# Requires:       SFEpython26-dateutil
# Requires:       SFEpython26-feedparser
# Requires:       SFEpython26-sqlalchemy
# Requires:       SFEpython26-sqlite
# Requires:       SFEpython26-xlib
# Requires:       SUNWPython26
# Requires:       SUNWgnome-python26-desktop
# Requires:       SUNWgnome-python26-extras
# Requires:       SUNWgnome-python26-libs
# Requires:       SUNWgst-python26
# Requires:       SUNWpython26-notify
# Requires:       SUNWpython26-xdg
# Requires:       SUNWsexy-python26
Requires:       %{name}-root
%if %SUNWavant
Requires:       SUNWavant
%else
Requires:       SFEavant
%endif
BuildRequires:  SUNWcompiz-devel
BuildRequires:  SUNWdbus-devel
BuildRequires:  SUNWdesktop-search-devel
BuildRequires:  SUNWgtk2-devel
BuildRequires:  SUNWxwinc
BuildRequires:  SUNWgst-python
BuildRequires:  SUNWpython-setuptools
# BuildRequires:  SUNWgst-python26-devel
# BuildRequires:  SUNWpython26-setuptools
%if %SUNWavant
Requires:       SUNWavant-devel
%else
Requires:       SFEavant-devel
%endif

%package devel
Summary:		 %summary - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:		 %name

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%define python_version 2.4
# %define python_version 2.6

%prep
%setup -q -c -n %name-%{version}
cd %{source_name}-%{version}
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0
%patch6 -p0
%patch7 -p0
%patch8 -p0
%patch9 -p0
%patch10 -p0
%patch11 -p0
%patch12 -p0
cd %{_builddir}/%name-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT
export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig:%{X11_DIR}/lib/pkgconfig

PROTO_LIB=$RPM_BUILD_DIR/%{name}/usr/X11/lib

export CFLAGS="%optflags -I%{X11_DIR}/include" 
export LDFLAGS="-L$PROTO_LIB -L%{X11_DIR}/lib -R%{X11_DIR}/lib"

cd %{source_name}-%{version}
intltoolize --force --copy --automake

autoconf
CFLAGS="-g -fast" PYTHON_VERSION=%{python_version} \
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}         \
	    --sysconfdir=%{_sysconfdir}	\
	    --libdir=%{_libdir}         \
            --includedir=%{_includedir} \
            --mandir=%{_mandir}   \
	    --datadir=%{_datadir}	

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
cd %{source_name}-%{version}
make install DESTDIR=$RPM_BUILD_ROOT

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages

rm -f ${RPM_BUILD_ROOT}/x11.pc
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

rm -rf $RPM_BUILD_ROOT%{_datadir}/locale

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri icon-cache gconf-cache

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}/vendor-packages
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}/vendor-packages/awn/
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}/vendor-packages/awn/extras/
%dir %attr (0755, root, bin) %{_libdir}/awn
%dir %attr (0755, root, bin) %{_libdir}/awn/applets
%dir %attr (0755, root, bin) %{_libdir}/awn/applets/*/
%{_libdir}/lib*so*
%{_libdir}/awn/applets/*/*
%{_libdir}/python%{python_version}/vendor-packages/awn/extras/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/avant-window-navigator
%{_datadir}/avant-window-navigator/*
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/apps/
%{_datadir}/icons/hicolor/scalable/apps/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/libawn-extras
%{_includedir}/libawn-extras/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/*

# endif for "ifnarch sparc"
%endif

%changelog
* Mon Aug 10 2009 - matt@greenviolet.net
- Initial spec
