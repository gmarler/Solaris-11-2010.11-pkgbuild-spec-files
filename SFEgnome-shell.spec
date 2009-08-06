#
# spec file for package SFEgnome-shell
#
# includes module(s): gnome-shell
#

%include Solaris.inc
Name:                    SFEgnome-shell
Summary:                 GNOME Shell
Version:                 0.0.1
Source1:                 shell.desktop
#owner:yippi date:2009-04-07 type:bug bugzilla:578196
Patch1:                  gnome-shell-01-launch.diff

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:           SUNWPython26-devel
BuildRequires:           SUNWdbus-glib-devel
BuildRequires:           SUNWgnome-base-libs-devel
BuildRequires:           SUNWgnome-media-devel
BuildRequires:           SUNWgnome-panel-devel
BuildRequires:           SUNWlibrsvg-devel
BuildRequires:           SFEclutter-1-0-devel
BuildRequires:           SFEgir-repository
BuildRequires:           SFEgjs-devel
BuildRequires:           SFEgobject-introspection-devel
BuildRequires:           SFEmutter-devel
Requires:                SUNWPython26
Requires:                SUNWdbus-glib
Requires:                SUNWgnome-base-libs
Requires:                SUNWgnome-media
Requires:                SUNWgnome-panel
Requires:                SUNWlibrsvg
# 2009-08-04
# DO NOT use SUNWclutter
# git-master mutter need /usr/share/gir-1.0/Clutter-1.0.gir,
# SFE version ship this file because it is built on top of
# SFEgobject-introspection and SFEgir-repository
Requires:                SFEclutter-1-0
Requires:                SFEgir-repository
Requires:                SFEgjs
Requires:                SFEgobject-introspection
Requires:                SFEmutter
%include default-depend.inc

%package root
Summary:		 %{summary} - / filesystem
SUNW_BaseDir:		 /
%include default-depend.inc

%prep
mkdir -p gnome-shell-%version
cd gnome-shell-%version
rm -fR gnome-shell
git-clone git://git.gnome.org/gnome-shell
cd gnome-shell
%patch1 -p1

%build
cd gnome-shell-%version
cd gnome-shell
./autogen.sh \
   --prefix=%{_prefix} \
   --libexecdir=%{_libexecdir} \
   --sysconfdir=%{_sysconfdir}
make

%install
rm -rf $RPM_BUILD_ROOT
cd gnome-shell-%version
cd gnome-shell
make install DESTDIR=$RPM_BUILD_ROOT

# Install a desktop file so you can log into GNOME Shell.
#
install -d $RPM_BUILD_ROOT%{_datadir}/xsessions
install --mode=0444 %SOURCE1 $RPM_BUILD_ROOT%{_datadir}/xsessions

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%preun root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo 'test -x $PKG_INSTALL_ROOT/usr/bin/gconftool-2 || {';
  echo '  echo "WARNING: gconftool-2 not found; not uninstalling gconf schemas"';
  echo '  exit 0';
  echo '}';
  echo 'umask 0022';
  echo 'GCONF_CONFIG_SOURCE=xml:merged:$BASEDIR/etc/gconf/gconf.xml.defaults';
  echo 'GCONF_BACKEND_DIR=$PKG_INSTALL_ROOT/usr/lib/GConf/2';
  echo 'LD_LIBRARY_PATH=$PKG_INSTALL_ROOT/usr/lib';
  echo 'export GCONF_CONFIG_SOURCE GCONF_BACKEND_DIR LD_LIBRARY_PATH';
  echo 'SDIR=$BASEDIR%{_sysconfdir}/gconf/schemas';
  echo 'schemas="$SDIR/gnome-shell.schemas"';
  echo '$PKG_INSTALL_ROOT/usr/bin/gconftool-2 --makefile-uninstall-rule $schemas'
) | $BASEDIR/var/lib/postrun/postrun -i -c JDS -a

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/gnome-shell
%{_libdir}/mutter/plugins
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gnome-shell
%{_datadir}/xsessions

%files root
%defattr(-, root, sys)
%attr(0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/gnome-shell.schemas

%changelog
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
