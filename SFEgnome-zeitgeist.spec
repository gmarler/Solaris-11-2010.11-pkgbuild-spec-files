#
# spec file for package SFEgnome-zeitgeist
#
# includes module(s): gnome-zeitgeist
#

%include Solaris.inc
Name:                    SFEgnome-zeitgeist
Summary:                 GNOME Shell
Version:                 0.0.1
Source1:                 shell.desktop
Patch1:                  gnome-zeitgeist-01-makefile.diff
Patch2:                  gnome-zeitgeist-02-python.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
# SFEbzr is needed since there isn't a release yet, and the spec-file
# pulls the data directly from bzr.
BuildRequires:           SFEbzr
BuildRequires:           SUNWdbus-python26
BuildRequires:           SUNWgnome-python26-libs-devel
Requires:                SUNWdbus-python26
Requires:                SUNWgnome-python26-libs

%include default-depend.inc

%prep
mkdir -p gnome-zeitgeist-%version
cd gnome-zeitgeist-%version
rm -fR gnome-zeitgeist
bzr branch lp:gnome-zeitgeist
cd gnome-zeitgeist
%patch1 -p1 
%patch2 -p1 

%build

%install
rm -rf $RPM_BUILD_ROOT
cd gnome-zeitgeist-%version
cd gnome-zeitgeist
make install DESTDIR=$RPM_BUILD_ROOT

# the makefile doesn't install the logo files, so do it here
cp -r data/logo $RPM_BUILD_ROOT/usr/share/gnome-zeitgeist/data/logo

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/services
%{_datadir}/dbus-1/services/org.gnome.Zeitgeist.service
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%{_datadir}/gnome-zeitgeist
%dir %attr (0755, root, other) %{_datadir}/pixmaps

%changelog
* Mon May 11 2009 - Brian Cameron  <brian.cameron@sun.com>
- Created.
