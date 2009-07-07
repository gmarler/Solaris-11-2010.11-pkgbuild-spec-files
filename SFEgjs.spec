#
# spec file for package SFEgjs
#
# includes module(s): gjs
#

%include Solaris.inc
Name:                    SFEgjs
Summary:                 GNOME JavaScript bindings
Version:                 0.3
Patch1:                  gjs-01-solaris.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:           SUNWfirefox-devel
BuildRequires:           SFEgobject-introspection-devel
Requires:                SUNWfirefox
Requires:                SFEgobject-introspection
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir: %{_basedir}
%include default-depend.inc

%prep
mkdir -p gjs-%version
cd gjs-%version
rm -fR gjs
git-clone git://git.gnome.org/gjs
cd gjs
%patch1 -p1

%build
cd gjs-%version
cd gjs
export LDFLAGS="-L/usr/lib/firefox"
export LD=cc
./autogen.sh --prefix=%{_prefix}
make

%install
rm -rf $RPM_BUILD_ROOT
cd gjs-%version
cd gjs
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT/%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT/%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%{_libdir}/gjs-1.0/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gjs-1.0/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*

%changelog
* Tue Jul 07 2009 - Brian.Cameron  <brian.cameron@sun.com>
- Add patch gjs-01-solaris.diff.
* Sat Apr 04 2009 - Brian.Cameron  <brian.cameron@sun.com>
- Created.
