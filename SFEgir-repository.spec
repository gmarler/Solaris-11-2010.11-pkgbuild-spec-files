# spec file for package SFEgir-repository
#
# includes module(s): gir-repository
#
%include Solaris.inc

%define pythonver 2.6

Name:                    SFEgir-repository
Summary:                 GIR Repository
Version:                 0.6.3
Source:			 http://ftp.gnome.org/pub/GNOME/sources/gir-repository/0.6/gir-repository-%{version}.tar.bz2
# This patch just hacks gir-repository to avoid building the GStreamer
# files since they do not seem to build properly on Solaris.  Need to
# actually fix this instead of avoiding building them.
Patch1:                  gir-repository-01-nogst.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:           SUNWPython26-devel
BuildRequires:           SUNWavahi-bridge-dsd-devel
BuildRequires:           SUNWbabl-devel
BuildRequires:           SUNWdbus-devel
BuildRequires:           SUNWgegl-devel
BuildRequires:           SUNWgtk2-devel
BuildRequires:           SUNWlibatk-devel
BuildRequires:           SUNWlibsoup-devel
BuildRequires:           SUNWlibunique-devel
BuildRequires:           SUNWgnome-config-devel
BuildRequires:           SUNWgnome-file-mgr-devel
BuildRequires:           SUNWgnome-gtksourceview-devel
BuildRequires:           SUNWgnome-libs-devel
BuildRequires:           SUNWgnome-media-devel
BuildRequires:           SUNWgnome-panel-devel
BuildRequires:           SUNWgnome-pdf-viewer-devel
BuildRequires:           SUNWgnome-terminal-devel
BuildRequires:           SUNWpango-devel
BuildRequires:           SFEgobject-introspection-devel
Requires:                SUNWPython26
BuildRequires:           SUNWavahi-bridge-dsd
Requires:                SUNWbabl
Requires:                SUNWdbus
Requires:                SUNWgegl
Requires:                SUNWgtk2
Requires:                SUNWlibatk
Requires:                SUNWlibsoup
Requires:                SUNWlibunique
Requires:                SUNWgnome-config
Requires:                SUNWgnome-file-mgr
Requires:                SUNWgnome-gtksourceview
Requires:                SUNWgnome-libs
Requires:                SUNWgnome-media
Requires:                SUNWgnome-panel
Requires:                SUNWgnome-pdf-viewer
Requires:                SUNWgnome-terminal
Requires:                SUNWpango
Requires:                SFEgobject-introspection
%include default-depend.inc

%prep
%setup -q -n gir-repository-%version
%patch1 -p1

%build
# The VTE bindings uses libncurses.  The VTE bindings do not build
# if it can't find libncurses.
export LD_LIBRARY_PATH="/usr/gnu/lib"
export PYTHON=/usr/bin/python%{pythonver}

libtoolize --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf
./configure --prefix=%{_prefix}
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT/%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT/%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%{_libdir}/girepository-1.0/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gir-1.0

%changelog
* Mon Aug 03 2009 - Brian Cameron  <brian.cameron@sun.com>
- Now build with 0.6.3 tarball.
* Sat Apr 04 2009 - Brian.Cameron  <brian.cameron@sun.com>
- Created.
