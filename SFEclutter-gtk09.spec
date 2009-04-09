#
# spec file for package SFEclutter-gtk09
#
# includes module(s): clutter-gtk
#

%include Solaris.inc
Name:                    SFEclutter-gtk09
Summary:                 GNOME JavaScript bindings
Version:                 0.9
# Patch taken from here:
# http://bugzilla.o-hand.com/show_bug.cgi?id=1490
Patch1:                  clutter-gtk9-01-introspection.diff
SUNW_BaseDir:            %{_basedir}
Requires: SUNWgnome-base-libs
Requires: SUNWclutter
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWclutter-devel
%include default-depend.inc

%ifnarch sparc
#packages are only for x86

BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-base-libs
Requires: SUNWclutter
BuildRequires: SUNWgnome-base-libs-devel

%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-base-libs-devel
Requires: SUNWclutter-devel

%prep
mkdir -p clutter-gtk-%version
cd clutter-gtk-%version
rm -fR clutter-gtk
git-clone git://git.clutter-project.org/clutter-gtk
cd clutter-gtk
%patch1 -p1

%build
cd clutter-gtk-%version
cd clutter-gtk
./autogen.sh --prefix=%{_prefix} \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --disable-static
make

%install
rm -rf $RPM_BUILD_ROOT
cd clutter-gtk-%version
cd clutter-gtk
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT/%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT/%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/girepository-1.0/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gir-1.0

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%endif

%changelog
* Sat Apr 04 2009 - Brian.Cameron  <brian.cameron@sun.com>
- Created.
