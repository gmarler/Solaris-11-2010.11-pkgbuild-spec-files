#
# spec file for package SFEquick-lounge-applet
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#
%include Solaris.inc
%use qlounge = quick-lounge-applet.spec

Name:                    SUNWquick-lounge-applet
IPS_package_name:        gnome/applet/quick-lounge-applet
Meta(info.classification): %{classification_prefix}:Applications/Panels and Applets
Summary:                 GNOME Quick Lounge applet
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
License:                 %{deskbar_applet.license}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgtk2-devel
BuildRequires: SUNWlibart-devel
BuildRequires: SUNWlibglade-devel
BuildRequires: SUNWgnome-media
BuildRequires: SUNWgnome-media-devel
BuildRequires: SUNWgnome-character-map-devel
BuildRequires: SUNWgnome-doc-utils
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWgnome-panel-devel
BuildRequires: SUNWgnome-python26-desktop-devel
BuildRequires: SUNWpython26-setuptools
BuildRequires: SUNWsolnm
BuildRequires: SUNWarc
BuildRequires: SUNWevolution-data-server-devel
Requires: SUNWgtk2
Requires: SUNWgnome-python26-desktop
Requires: SUNWgnome-character-map
Requires: SUNWgnome-panel
Requires: SUNWgnome-libs
Requires: SUNWgnome-config
Requires: SUNWgnome-vfs
Requires: SUNWgnome-component
Requires: SUNWlibpopt

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%if %build_l10n
%package l10n
IPS_package_name:        system/display-manager/gdm/l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir(relocate_from:%{_prefix}): %{_gnome_il10n_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version
%qlounge.prep -d %name-%version

%build
%qlounge.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%qlounge.install -d %name-%version

chmod 0644 $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/C/*.xml

# Never install English locales because should support full functions
# on English locales as same as Solaris. See SUNWzz-gnome-l10n.spec.
rm -r $RPM_BUILD_ROOT%{_datadir}/locale/en_GB

%if %build_l10n
%else
# REMOVE l10n FILES
rm -r $RPM_BUILD_ROOT%{_datadir}/locale
rm -r $RPM_BUILD_ROOT%{_datadir}/gnome/help/[e-z]*/[a-z]*
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post 
%restart_fmri icon-cache gconf-cache

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/bonobo/servers/GNOME_QuickLoungeApplet_Factory.server
%{_libexecdir}/quick-lounge-applet
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/quick-lounge/C
%{_datadir}/gnome-2.0/ui/GNOME_QuickLoungeApplet.xml
%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%{_datadir}/icons/hicolor/48x48/apps/quick-lounge*
%{_datadir}/quick-lounge-applet

%files root
%defattr(-, root, sys)
%dir %attr(0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/quick-lounge.schemas

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/[a-c]*/[a-z]*
%{_datadir}/gnome/help/[e-z]*/[a-z]*
%{_datadir}/omf/*/*-[a-z][a-z].omf
%{_datadir}/omf/*/*-[a-z][a-z]_[A-Z][A-Z].omf
%endif

%changelog
* Tue Dec 07 2010 - brian.cameron@oracle.com
- Created.
