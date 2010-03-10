#
# spec file for package SFEsugar
#
# includes module(s): sugar
#

%define pythonver 2.6

%include Solaris.inc
Name:                    SFEsugar
Summary:                 Sugar Learning Platform
URL:                     http://www.sugarlabs.org/
Version:                 0.87.8
Source:                  http://download.sugarlabs.org/sources/sucrose/glucose/sugar/sugar-%{version}.tar.bz2
Source1:                 sugar.desktop
Patch1:                  sugar-01-python.diff
Patch2:                  sugar-02-mouse.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:                SUNWgtk2
Requires:                SUNWgnome-config
Requires:                SUNWgnome-python26-libs
Requires:                SFEsugar-base
Requires:                SFEsugar-toolkit
Requires:                SFEhippodraw
Requires:                SFEpython26-telepathy
BuildRequires:           SUNWgtk2-devel
BuildRequires:           SUNWgnome-config-devel
BuildRequires:           SUNWgnome-python26-libs-devel
BuildRequires:           SFEhippodraw-devel
BuildRequires:           SFEpython26-telepathy

%package root
Summary:      %{summary} - / filesystem
SUNW_BaseDir: /
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:      %{summary} - l10n files
SUNW_BaseDir: %{_basedir}
%include default-depend.inc
Requires:     %{name}
%endif

%prep
%setup -q -n sugar-%version
%patch1 -p1
%patch2 -p1

%build
export PYTHON=/usr/bin/python%{pythonver}
./configure --prefix=%{_prefix} \
            --sysconfdir=%{_sysconfdir}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

mkdir -p $RPM_BUILD_ROOT/usr/share/xsessions
cp %{SOURCE1} $RPM_BUILD_ROOT/usr/share/xsessions

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z]*.omf
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/jarabe
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/apps
%attr (-, root, other) %{_datadir}/icons/hicolor/scalable/apps/*
%dir %attr (0755, root, root) %{_datadir}/mime
%dir %attr (0755, root, root) %{_datadir}/mime/packages
%attr(644,root,bin) %{_datadir}/mime/packages/sugar.xml
%{_datadir}/sugar
%{_datadir}/xsessions/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%attr(0755, root, bin) %dir %{_sysconfdir}/dbus-1
%attr(0755, root, bin) %dir %{_sysconfdir}/dbus-1/system.d
%{_sysconfdir}/dbus-1/system.d/*
%{_sysconfdir}/gconf/schemas/sugar.schemas

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/*/[a-z]*
%{_datadir}/omf/*/*-[a-z]*.omf
%endif

%changelog
* Wed Mar 10 2010 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.87.8.
* Tue Feb 02 2010 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.87.3.
* Sun Jul 08 2009 - Brian Cameron  <brian.cameron@sun.com>
- Created with 0.84.6.
