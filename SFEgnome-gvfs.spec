#
# spec file for package SFEgnome-gvfs
#
# includes module(s): gvfs
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: gheet
#
%include Solaris.inc

%use gvfs = gvfs.spec

Name:                    SFEgnome-gvfs
Summary:                 GNOME virtual file system framework
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-base-libs
Requires: SUNWdbus
Requires: SUNWlibmsr
Requires: SFEgio
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWdbus-devel
BuildRequires: SFEgio-devel
%if %option_with_gnu_iconv
Requires: SUNWgnu-libiconv
Requires: SUNWgnu-gettext
%else
Requires: SUNWuiu8
%endif

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%gvfs.prep -d %name-%version

%build
# -D_XPG4_2 is to get CMSG_SPACE declaration in <sys/socket.h>.
export CFLAGS="%optflags -D_XPG4_2 -D__EXTENSIONS__"
%if %option_with_gnu_iconv
export CFLAGS="$CFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl"
%endif
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags"
%gvfs.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gvfs.install -d %name-%version
rm $RPM_BUILD_ROOT%{_cxx_libdir}/libgvfscommon.la
rm $RPM_BUILD_ROOT%{_cxx_libdir}/gio/modules/libgvfsdbus.la

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}/gvfs*
%dir %attr (0755, root, bin) %{_cxx_libdir}
%{_cxx_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/dbus-1/services/gvfs*
%{_datadir}/gvfs*
%dir %attr (-, root, other) %{_datadir}/locale
%{_datadir}/locale/[a-z]*/LC_MESSAGES/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/profile.d/*


%changelog
* Fri Feb 12 2010 - jchoi42@pha.jhu.edu
- modify files to reflect version update
* Sun Nov 18 2007 - daymobrew@users.sourceforge.net
- Add support for building on Indiana systems. Add changes for gvfs 0.0.2.
* Fri Nov 09 2007 - nonsea@users.sourceforge.net
- Add SFEgio to Requires, add SFEgio-devel to BuildRequires.
* Thu Nov 07 2007 - damien.carbery@sun.com
- Initial version.
