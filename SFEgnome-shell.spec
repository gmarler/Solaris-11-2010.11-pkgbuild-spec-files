#
# spec file for package SFEgnome-shell
#
# includes module(s): gnome-shell
#

%define pythonver 2.6

%include Solaris.inc
Name:                    SFEgnome-shell
Summary:                 GNOME Shell
Version:                 2.29.1
Source:                  http://ftp.gnome.org/pub/GNOME/sources/gnome-shell/2.29/gnome-shell-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:           SUNWPython26-devel
BuildRequires:           SUNWdbus-glib-devel
BuildRequires:           SUNWgnome-base-libs-devel
BuildRequires:           SUNWgnome-media-devel
BuildRequires:           SUNWgnome-panel-devel
BuildRequires:           SUNWlibrsvg-devel
BuildRequires:           SUNWclutter-devel
BuildRequires:           SUNWgir-repository
BuildRequires:           SUNWgobject-introspection-devel
BuildRequires:           SFEgjs-devel
BuildRequires:           SFEmutter-devel
Requires:                SUNWPython26
Requires:                SUNWdbus-glib
Requires:                SUNWgnome-base-libs
Requires:                SUNWgnome-media
Requires:                SUNWgnome-panel
Requires:                SUNWlibrsvg
Requires:                SUNWclutter
Requires:                SUNWgir-repository
Requires:                SUNWgobject-introspection
Requires:                SFEgjs
Requires:                SFEmutter
%include default-depend.inc

%package root
Summary:		 %{summary} - / filesystem
SUNW_BaseDir:		 /
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n gnome-shell-%version

%build
export PYTHON=/usr/bin/python%{pythonver}
./configure \
   --prefix=%{_prefix} \
   --libexecdir=%{_libexecdir} \
   --mandir=%{_mandir} \
   --sysconfdir=%{_sysconfdir} \
   --with-clutter
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT/%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache icon-cache gconf-cache

%post root
cat >> $BASEDIR/var/svc/profile/upgrade <<\EOF

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/gnome-shell
%{_libdir}/mutter/plugins
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_datadir}/gnome-shell
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/man1/*


%files root
%defattr(-, root, sys)
%attr(0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/gnome-shell.schemas

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Tue Apr 27 2010 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 2.29.1.
* Wed Mar 10 2010 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 2.29.0.
* Thu Nov 05 2009 - Brian Cameron  <brian.cameron@sun.com>
- No longer install the shell.desktop file since this is not an appropriate
  way to launch GNOME Shell.  Instead users should run "gnome-shell --replace"
  after starting their session.
* Sun Oct 11 2009 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 2.28.0.
* Wed Sep 16 2009 - Halton Huo <halton.huo@sun.com>
- Bump to 2.27.3.
* Sat Sep 05 2009 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 2.27.2.
* Wed Aug 05 2009 - Brian Cameron  <brian.cameron@sun.com>
- Remove missing-dash.diff and missing-svg.diff patches since they are now
  upstream.
* Wed Aug 05 2009 - Halton Huo  <halton.huo@sun.com>
- Remove upstreamed patch lookingglass.diff
- Add patch missing-dash.diff to fix bugzilla #590813
- Add patch missing-svg.diff to fix bugzilla #590814
* Mon Aug 03 2009 - Brian Cameron  <brian.cameron@sun.com>
- Add gnome-shell-03-lookingglass.diff so this javascript file gets installed.
  Otherwise gnome-shell won't start up.
* Tue Jul 07 2009 - Brian Cameron  <brian.cameron@sun.com>
- Remove patch gnome-shell-02-overlay.diff which no longer applies.
* Tue Apr 28 2009 - Brian Cameron  <brian.cameron@sun.com>
- Install dekstop file for GNOME Shell.
* Sat Apr 06 2009 - Brian Cameron  <brian.cameron@sun.com>
- Created.
