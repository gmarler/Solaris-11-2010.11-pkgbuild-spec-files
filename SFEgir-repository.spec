# spec file for package SFEgir-repository
#
# includes module(s): gir-repository
#
%include Solaris.inc

%define pythonver 2.6

Name:                    SFEgir-repository
Summary:                 GIR Repository
Version:                 0.6.3
Patch1:                  gir-repository-01-nogst.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:           SUNWPython26-devel
BuildRequires:           SUNWbabl-devel
BuildRequires:           SUNWdbus-devel
BuildRequires:           SUNWgegl-devel
BuildRequires:           SUNWlibsoup-devel
BuildRequires:           SUNWlibunique-devel
BuildRequires:           SUNWgnome-base-libs-devel
BuildRequires:           SUNWgnome-config-devel
BuildRequires:           SUNWgnome-file-mgr-devel
BuildRequires:           SUNWgnome-gtksourceview-devel
BuildRequires:           SUNWgnome-libs-devel
BuildRequires:           SUNWgnome-media-devel
BuildRequires:           SUNWgnome-panel-devel
BuildRequires:           SUNWgnome-pdf-viewer-devel
BuildRequires:           SUNWgnome-terminal-devel
BuildRequires:           SFEgobject-introspection-devel
Requires:                SUNWPython26
Requires:                SUNWbabl
Requires:                SUNWdbus
Requires:                SUNWgegl
Requires:                SUNWlibsoup
Requires:                SUNWlibunique
Requires:                SUNWgnome-base-libs
Requires:                SUNWgnome-config
Requires:                SUNWgnome-file-mgr
Requires:                SUNWgnome-gtksourceview
Requires:                SUNWgnome-libs
Requires:                SUNWgnome-media
Requires:                SUNWgnome-panel
Requires:                SUNWgnome-pdf-viewer
Requires:                SUNWgnome-terminal
Requires:                SFEgobject-introspection
%include default-depend.inc

%prep
mkdir -p gir-repository-%version
cd gir-repository-%version
rm -fR gir-repository
git-clone git://git.gnome.org/gir-repository
cd gir-repository
%patch1 -p1

%build
cd gir-repository-%version
cd gir-repository
# The VTE bindings uses libncurses.  The VTE bindings do not build
# if it can't find libncurses.
export LD_LIBRARY_PATH="/usr/gnu/lib"
export PYTHON=/usr/bin/python%{pythonver}
./autogen.sh --prefix=%{_prefix}
make

%install
rm -rf $RPM_BUILD_ROOT
cd gir-repository-%version
cd gir-repository
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
* Sat Apr 04 2009 - Brian.Cameron  <brian.cameron@sun.com>
- Created.
