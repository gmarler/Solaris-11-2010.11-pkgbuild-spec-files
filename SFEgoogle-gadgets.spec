#
# spec file for package SFEgoogle-gadgets
#
# includes module(s): google-gadgets
#
%include Solaris.inc

Name:                    SFEgoogle-gadgets
Summary:                 Google Gadgets - a platform for running desktop gadgets.
Version:                 0.11.0
Source:                  http://google-gadgets-for-linux.googlecode.com/files/google-gadgets-for-linux-%{version}.tar.bz2
URL:                     http://code.google.com/p/google-gadgets-for-linux/

# owner:alfred date:2009-01-12 type:bug
Patch1:                  google-gadgets-01-solaris-build.diff

Patch2:                  google-gadgets-02-firefox-3-1.diff

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

#####################################
##  Package Requirements Section   ##
#####################################

%include default-depend.inc
Requires: SUNWfirefox
Requires: SUNWlibstdcxx4
Requires: SUNWzlib
Requires: SUNWmlib
Requires: SUNWdbus-libs
Requires: SUNWgnome-base-libs
Requires: SUNWfontconfig
Requires: SUNWfreetype2
Requires: SUNWgnome-libs

BuildRequires: SUNWfirefox-devel
BuildRequires: SUNWgnome-common-devel
BuildRequires: SUNWgnome-base-libs-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}

%prep
%setup -q -n google-gadgets-for-linux-%{version}
%patch1 -p0
%patch2 -p1

%build
export PKG_CONFIG_PATH=/opt/sfw/lib/pkgconfig:%{_pkg_config_path}

export CPPFLAGS=`pkg-config --cflags-only-I libstdcxx4`
export CXXFLAGS=`pkg-config --cflags-only-other libstdcxx4`
export LDFLAGS=`pkg-config --libs libstdcxx4`

gnome-autogen.sh --prefix=/usr --disable-werror
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# doesn't ship *.a and *.la
cd $RPM_BUILD_ROOT%{_libdir}
rm -f libggadget-*a
cd google-gadgets/modules
rm -f *a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, other)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/ggl-gtk
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/google-gadgets
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*
%dir %attr (0755, root, root)  %{_datadir}/mime
%dir %attr (0755, root, root)  %{_datadir}/mime/packages
%{_datadir}/mime/packages/00-google-gadgets.xml
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libggadget-*.so*
%{_libdir}/google-gadgets/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/pkgconfig/*

%changelog
* Thu Jun 25 2009 - alfred.peng@sun.com
- Bump to 0.11.0.
  Add patch to build with Firefox 3.5.
* Mon Jan 14 2009 - alfred.peng@sun.com
- Initial version
