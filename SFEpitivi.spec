#
# spec file for package SFEpitivi
#
# includes module(s): pitivi
#

%include Solaris.inc

%define pythonver 2.6

Name:                    SFEpitivi
Summary:                 Non-Linear video editor
URL:                     http://ftp.gnome.org/pub/GNOME/sources/pitivi
Version:                 0.13.4
Source:                  http://ftp.gnome.org/pub/GNOME/sources/pitivi/0.13/pitivi-%{version}.tar.bz2
Patch1:                  pitivi-01-solaris.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython26-devel
BuildRequires:           SUNWgnome-python26-extras-devel
BuildRequires:           SUNWgst-python26-devel
Requires:                SFEpy26goocanvas-devel
BuildRequires:           SUNWgnonlin-devel
Requires:                SUNWPython26
Requires:                SUNWgnome-python26-extras
Requires:                SUNWgst-python26
Requires:                SUNWpython26-setuptools
Requires:                SUNWpython26-zope-interface
Requires:                SFEpy26goocanvas
Requires:                SUNWgnonlin

%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n pitivi-%version
%patch1 -p1

%build
export PYTHON=/usr/bin/python%{pythonver}
./configure --prefix=%{_prefix} \
            --enable-gstreamer
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/pitivi
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16
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
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/apps/
%{_datadir}/icons/hicolor/scalable/apps/*
%dir %attr (-, root, root) %{_datadir}/mime
%attr (-, root, root) %{_datadir}/mime/*
%{_datadir}/pitivi

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Wed Mar 10 2010 - brian.cameron@sun.com
- Bump to 0.13.4.
* Wed Sep 23 2009 - brian.cameron@sun.com
- Bump to 0.13.3.
* Mon Jun 08 2009 - brian.cameron@sun.com
- Bump to 0.13.1.  Update packaging.
* Thu Mar 19 2009 - brian.cameron@sun.com
- Bump to 0.11.3.
* Mon Oct 27 2008 - brian.cameron@sun.com
- Bump to 0.11.2.
* Thu Apr 10 2008 - brian.cameron@sun.com
- Change SFEgst-python to SUNWgst-python.
* Mon Apr 07 2008 - brian.cameron@sun.com
- Change SFEgnome-python-extras to SUNWgnome-python-extras.
* Thu Jan 10 2008 - irene.huang@sun.com
- Add two new requirements: SFEpython-setuptools and 
  SFEzope-interface
* Fri Nov 30 2007 - brian.cameron@sun.com
- Bump to 0.11.1
* Fri Oct 19 2007 - brian.cameron@sun.com
- Bump to 0.11.0
* Mon Aug 06 2007 - brian.cameron@sun.com
- Bump to 0.10.3
* Wed Mar 21 2007 - daymobrew@users.sourceforge.net
- Add l10n package and correct file permissions.
* Fri Feb  9 2007  - irene.huang@sun.com
- Created.
