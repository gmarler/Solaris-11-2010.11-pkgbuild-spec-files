#
# spec file for package SFEclutter-gtk10
#
# includes module(s): clutter-gtk
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%use cluttergtk = clutter-gtk10.spec

Name:                    SFEclutter-gtk10
Summary:                 clutter-gtk - GTK+ integration library for clutter
Version:                 %{cluttergtk.version}
URL:                     http://www.clutter-project.org/
SUNW_BaseDir:            %{_basedir}

%ifnarch sparc
#packages are only for x86

BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEclutter1

%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SFEclutter1-devel

%prep
rm -rf %name-%version
mkdir %name-%version
%cluttergtk.prep -d %name-%version

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
%cluttergtk.build -d %name-%version

%install
%cluttergtk.install -d %name-%version
rm $RPM_BUILD_ROOT%{_libdir}/lib*.la

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
* Mon Aug 03 2009  Brian.Cameron@sun.com
- Bump to 0.10.
* Thu Mar 26 2009  Chris.wang@sun.com
- Correct copyright file in file section
* Fri Feb 20 2009  chris.wang@sun.com
- Add manpage
* Tue Jul  1 2008  chris.wang@sun.com 
- Initial build.
