#
# spec file for package SFEgobject-introspection
#
# includes module(s): gobject-introspection
#
%include Solaris.inc

%define pythonver 2.6

Name:                    SFEgobject-introspection
Summary:                 GObject introspection support
Version:                 0.6.3
#owner:yippi date:2009-04-07 type:bug bugzilla:578199
Patch1:                  gobject-introspection-01-union.diff
#owner:yippi date:2009-04-07 type:bug bugzilla:578200
Patch2:                  gobject-introspection-02-scanner.diff
#owner:yippi date:2009-04-07 type:bug bugzilla:578202
Patch3:                  gobject-introspection-03-fixshave.diff
Patch4:                  gobject-introspection-04-dumper.diff
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
mkdir -p gobject-introspection-%version
cd gobject-introspection-%version
rm -fR gobject-introspection
git-clone git://git.gnome.org/gobject-introspection
cd gobject-introspection
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
cd gobject-introspection-%version
cd gobject-introspection
export PYTHON=/usr/bin/python%{pythonver}
./autogen.sh \
   --prefix=%{_prefix} \
   --mandir=%{_mandir}
make

%install
rm -rf $RPM_BUILD_ROOT
cd gobject-introspection-%version
cd gobject-introspection
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
* Sat Apr 04 2009 - Brian.Cameron  <brian.cameron@sun.com>
- Created.
