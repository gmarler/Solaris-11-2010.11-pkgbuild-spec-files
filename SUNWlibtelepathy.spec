#
# spec file for packages SUNWlibtelepathy
#
# includes module(s): libtelepathy
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: elaine
#
%include Solaris.inc

%use libtelepathy= libtelepathy.spec

Name:                    SUNWlibtelepathy
Summary:                 A GLib library to ease writing Telepathy clients in glib
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:            SUNWtelepathy-glib
BuildRequires:       SUNWtelepathy-glib-devel

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires:            SUNWtelepathy-glib

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version
%libtelepathy.prep -d %name-%version

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export RPM_OPT_FLAGS="$CFLAGS"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"

%libtelepathy.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT

%libtelepathy.install -d %name-%version

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%doc(bzip2) libtelepathy-%{libtelepathy.version}/COPYING
%doc(bzip2) libtelepathy-%{libtelepathy.version}/NEWS
%doc(bzip2) libtelepathy-%{libtelepathy.version}/ChangeLog
%doc libtelepathy-%{libtelepathy.version}/AUTHORS
%doc libtelepathy-%{libtelepathy.version}/README
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc

%files devel
%defattr(-, root, bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%dir %attr (0755, root, bin) %{_includedir}
%{_libdir}/pkgconfig/*.pc
%attr(755, root, root) %{_includedir}/telepathy-1.0/*

%changelog
* Thu Mar 12 2009 - elaine.xiong@sun.com
- Move from spec-files/trunk.
* Wed Nov 05 2008 - rick.ju@sun.com
- Initial spec-file created
