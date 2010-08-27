#
# spec file for package SFElightdm
#
# includes module(s): lightdm
#
# bugdb: bugzilla.freedesktop.org
#

%include Solaris.inc
Name:                    SFElightdm
License:                 GPL v3
Version:                 0.1.1
Source:                  http://people.ubuntu.com/~robert-ancell/lightdm/releases/lightdm-%version.tar.gz
Source1:                 lightdm.xml
Source2:                 svc-lightdm
Patch1:                  lightdm-01-branding.diff
Patch2:                  lightdm-02-compile.diff
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
Summary:                 Light Display manager
URL:                     https://launchpad.net/~robert-ancell/+archive/lightdm
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:            %{_basedir}

%include default-depend.inc
Requires:                SUNWglib2
Requires:                SUNWgtk2
Requires:                SUNWconsolekit
Requires:                SUNWdbus-glib
Requires:                SFElibxklavier
Requires:                SFEwebkitgtk
Requires:                SFElibxcb
Requires:                SFExcb-proto
Requires:                SFElibpthread-stubs
BuildRequires:           SUNWglib2-devel
BuildRequires:           SUNWgtk2-devel
BuildRequires:           SUNWdbus-glib-devel
BuildRequires:           SFElibxklavier-devel
BuildRequires:           SFEwebkitgtk-devel
BuildRequires:           SFEwebkitgtk-devel
BuildRequires:           SFElibxcb-devel
BuildRequires:           SFExcb-proto-devel
BuildRequires:           SFElibpthread-stubs

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%prep
%setup -q -n lightdm-%version
%patch1 -p0
%patch2 -p0

%build
libtoolize --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf
./configure \
   --prefix=%{_prefix} \
   --libexecdir=%{_libexecdir} \
   --sysconfdir=%{_sysconfdir}
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'

rm -rf $RPM_BUILD_ROOT%{_datadir}/locale

install -d $RPM_BUILD_ROOT/lib/svc/manifest/application/graphical-login
install --mode=0444 %SOURCE1 $RPM_BUILD_ROOT/lib/svc/manifest/application/graphical-login
install -d $RPM_BUILD_ROOT/lib/svc/method
cp %SOURCE2 $RPM_BUILD_ROOT/lib/svc/method/

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache gconf-cache

%postun
%restart_fmri desktop-mime-cache

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%attr (0755, root, bin)%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/*
%dir %attr (0755, root, bin) %{_libexecdir}/ldm-gtk-greeter
%dir %attr (0755, root, bin) %{_libexecdir}/ldm-webkit-greeter
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gir-1.0/*
%{_datadir}/gtk-doc/*
%{_datadir}/lightdm/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/lightdm.1

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%dir %attr (0755, root, bin) %{_sysconfdir}/dbus-1
%dir %attr (0755, root, bin) %{_sysconfdir}/dbus-1/system.d
%{_sysconfdir}/dbus-1/system.d/*
%{_sysconfdir}/lightdm.conf
# SVC method file
%dir %attr (0755, root, bin) /lib
%dir %attr (0755, root, bin) /lib/svc
%dir %attr (0755, root, bin) /lib/svc/method
%dir %attr (0755, root, sys) /lib/svc/manifest
%dir %attr (0755, root, sys) /lib/svc/manifest/application
%dir %attr (0755, root, sys) /lib/svc/manifest/application/graphical-login
%attr (0555, root, bin) /lib/svc/method/svc-lightdm
%attr (0444, root, sys) /lib/svc/manifest/application/graphical-login/lightdm.xml

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Thu Aug 26 2010 - Brian Cameron  <brian.cameron@oracle.com>
- Created with version 0.1.1.
