#
# spec file for package SFEgobject-introspection
#
# includes module(s): gobject-introspection
#
# Note that there are some issues that you need to address to avoid build
# issues when building this module:
#
# 1) For some reason SUNWPython26.spec has a problem with ctypes that causes
#    gobject-introspection to fail to build.  Uninstalling and rebuilding this
#    package from spec-files seems to fix this problem. Need to figure this
#    out and get it fixed in the SUNWPython26 package.
#

%include Solaris.inc

%define pythonver 2.6

Name:                    SFEgobject-introspection
Summary:                 GObject introspection support
Version:                 0.6.3
Source:                  http://download.gnome.org/sources/gobject-introspection/0.6/gobject-introspection-%{version}.tar.bz2
#owner:yippi date:2009-04-07 type:bug bugzilla:578200
Patch1:                  gobject-introspection-01-scanner.diff
#owner:yippi date:2009-04-07 type:bug bugzilla:578202
Patch2:                  gobject-introspection-02-fixshave.diff
Patch3:                  gobject-introspection-03-dumper.diff
#owner:halton date:2009-04-07 type:bug bugzilla:587823 status:upstreamed
Patch4:                  gobject-introspection-04-crash-compiler.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:           SUNWPython26-devel
BuildRequires:           SUNWgnome-base-libs-devel
BuildRequires:           SUNWlibffi
Requires:                SUNWgnome-base-libs
Requires:                SUNWlibffi
Requires:                SUNWPython26
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir: %{_basedir}
%include default-depend.inc

%prep
%setup -q -n gobject-introspection-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

#FIXME: When #590802 fixed in next release, remove following lines 
rm -f m4/lt~obsolete.m4
rm -f m4/ltoptions.m4
rm -f m4/libtool.m4
rm -f m4/ltsugar.m4
rm -f m4/ltversion.m4

%build
export PYTHON=/usr/bin/python%{pythonver}

libtoolize --force
aclocal $ACLOCAL_FLAGS -I m4
autoheader
automake -a -c -f
autoconf
./configure \
   --prefix=%{_prefix} \
   --mandir=%{_mandir}
make

%install
rm -rf $RPM_BUILD_ROOT
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
%{_libdir}/girepository-1.0/*
%{_libdir}/gobject-introspection/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gir-1.0
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%changelog
* Wed Aug 05 2009 - Halton Huo  <halton.huo@sun.com>
- Use 0.6.3 tarball release 
- Add crash-compiler.diff to fix #587823
* Fri Jul 03 2009 - Brian Cameron  <brian.cameron@sun.com
- Remove upstream patch gobject-introspection-01-union.diff,
  renumber rest.
* Sat Apr 04 2009 - Brian Cameron  <brian.cameron@sun.com>
- Created.
