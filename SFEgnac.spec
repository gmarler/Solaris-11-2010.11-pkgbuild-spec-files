#
# spec file for package SFEgnac.spec
#
# includes module(s): gnac
#
%include Solaris.inc

%define src_name	gnac

Name:		SFEgnac
Version:	0.2.2
Summary:	Audio converter for GNOME
Group:		Applications/Multimedia
License:	GPLv2+
URL:		http://gnac.sourceforge.net/
Source:		%{sf_download}/%{src_name}/%{src_name}-%{version}.tar.bz2
Patch1:		gnac-01-export-dynamic.diff
BuildRoot:	%{_tmppath}/%{src_name}-%{version}-build
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc

Requires:	SUNWgnome-media
BuildRequires:	SUNWgnome-media-devel
BuildRequires:	SUNWgnome-common-devel

%description
Gnac is an easy to use audio conversion program for the Gnome desktop.
It is designed to be powerful but simple! It provides easy audio files
conversion between all GStreamer supported audio formats. 

%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/
%include default-depend.inc
Requires:	SUNWpostrun-root
Requires:	SUNWgnome-config

%package l10n
Summary:	%{summary} - l10n files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%{name}

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
./configure --prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir}

%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1;
make DESTDIR=$RPM_BUILD_ROOT install
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

desktop-file-validate $RPM_BUILD_ROOT/%{_datadir}/applications/%{src_name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%{_bindir}/%{src_name}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/%{src_name}/
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/%{src_name}/
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/%{src_name}.desktop
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/%{src_name}.png
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/apps/
%{_datadir}/icons/hicolor/scalable/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16/apps/
%{_datadir}/icons/hicolor/16x16/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/apps/
%{_datadir}/icons/hicolor/22x22/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/apps/
%{_datadir}/icons/hicolor/24x24/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/apps/
%{_datadir}/icons/hicolor/32x32/apps/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/apps/
%{_datadir}/icons/hicolor/48x48/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/64x64/
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/64x64/apps/
%{_datadir}/icons/hicolor/64x64/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/72x72/
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/72x72/apps/
%{_datadir}/icons/hicolor/72x72/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/96x96/
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/96x96/apps/
%{_datadir}/icons/hicolor/96x96/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/128x128/
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/128x128/apps/
%{_datadir}/icons/hicolor/128x128/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/192x192/
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/192x192/apps/
%{_datadir}/icons/hicolor/192x192/apps/*
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/256x256/
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/256x256/apps/
%{_datadir}/icons/hicolor/256x256/apps/*
%{_mandir}/man1/%{src_name}.1

%files root
%defattr (-, root, sys)
%{_sysconfdir}/gconf/schemas/%{src_name}.schemas

%files l10n
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/locale
%{_datadir}/locale/*

%changelog
* Sat Jul 24 2010 - Milan Jurik
- Initial spec
