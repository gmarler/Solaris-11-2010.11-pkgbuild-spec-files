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
BuildRequires:           SFEclutter09-devel
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
Requires:                SFEclutter09
Requires:                SFEgir-repository
Requires:                SFEgjs
Requires:                SFEgobject-introspection
Requires:                SFEmutter
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
   --libexecdir=%{_libexecdir}
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

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/gnome-shell
%{_libdir}/gnomeshell-taskpanel
%{_libdir}/mutter/plugins
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gnome-shell
%{_datadir}/xsessions

%changelog
* Tue Jul 07 2009 - Brian Cameron  <brian.cameron@sun.com>
- Remove patch gnome-shell-02-overlay.diff which no longer applies.
* Tue Apr 28 2009 - Brian Cameron  <brian.cameron@sun.com>
- Install dekstop file for GNOME Shell.
* Sat Apr 06 2009 - Brian Cameron  <brian.cameron@sun.com>
- Created.
