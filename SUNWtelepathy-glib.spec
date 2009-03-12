#
# spec file for packages SUNWtelepathy-glib
#
# includes module(s): telepathy-glib
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: elaine
#
%include Solaris.inc

%use telepathy_glib = telepathy-glib.spec

Name:                    SUNWtelepathy-glib
Summary:                 A GLib-based helper library for clients and connection managers
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
#Requires: 

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version
%telepathy_glib.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export RPM_OPT_FLAGS="$CFLAGS"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"

%telepathy_glib.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT

%telepathy_glib.install -d %name-%version

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%{_libdir}/lib*.so*
%{_datadir}/gtk-doc/*/*/*
%doc(bzip2) telepathy-glib-%{telepathy_glib.version}/COPYING
%doc(bzip2) telepathy-glib-%{telepathy_glib.version}/NEWS
%doc(bzip2) telepathy-glib-%{telepathy_glib.version}/ChangeLog
%doc telepathy-glib-%{telepathy_glib.version}/AUTHORS
%doc telepathy-glib-%{telepathy_glib.version}/README
%dir %attr (0755, root, other) %{_datadir}/doc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%dir %attr (0755, root, bin) %{_includedir}
%{_libdir}/pkgconfig/*.pc
%attr(755, root, bin) %{_includedir}/telepathy-1.0/*

%changelog
* Thu Mar 12 2009 - elaine.xiong@sun.com
- Move from spec-fies/trunk
* Wed Nov 05 2008 - rick.ju@sun.com
- Initial spec-file created
