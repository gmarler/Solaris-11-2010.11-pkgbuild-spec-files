#
# spec file for package SFEgnome-shell
#
# includes module(s): gnome-shell
#

%include Solaris.inc
Name:                    SFEgnome-shell
Summary:                 GNOME Shell
Version:                 0.0.1
#owner:yippi date:2009-04-07 type:bug bugzilla:578196
Patch1:                  gnome-shell-01-launch.diff
#owner:yippi date:2009-04-07 type:bug bugzilla:578197
Patch2:                  gnome-shell-02-overlay.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:           SUNWPython26-devel
BuildRequires:           SUNWdbus-glib-devel
BuildRequires:           SUNWclutter-devel
BuildRequires:           SUNWgnome-base-libs-devel
BuildRequires:           SUNWgnome-media-devel
BuildRequires:           SUNWgnome-panel-devel
BuildRequires:           SUNWlibrsvg-devel
BuildRequires:           SFEgjs-devel
BuildRequires:           SFEgobject-introspection-devel
BuildRequires:           SFEmetacity-clutter-devel
Requires:                SUNWPython26
Requires:                SUNWdbus-glib
Requires:                SUNWclutter
Requires:                SUNWgnome-base-libs
Requires:                SUNWgnome-media
Requires:                SUNWgnome-panel
Requires:                SUNWlibrsvg
Requires:                SFEgjs
Requires:                SFEgobject-introspection
Requires:                SFEmetacity-clutter
%include default-depend.inc

%prep
mkdir -p gnome-shell-%version
cd gnome-shell-%version
rm -fR gnome-shell
git-clone git://git.gnome.org/gnome-shell
cd gnome-shell
%patch1 -p1
%patch2 -p1

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

#find $RPM_BUILD_ROOT/%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
#find $RPM_BUILD_ROOT/%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

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
%{_libdir}/metacity/plugins
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gnome-shell

%changelog
* Sat Apr 06 2009 - Brian.Cameron  <brian.cameron@sun.com>
- Created.
