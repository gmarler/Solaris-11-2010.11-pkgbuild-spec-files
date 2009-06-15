#
# spec file for package conduit
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner:halton
#

Name:           conduit
License:        GPL
Group:          System/GUI/GNOME
Version:        0.3.15
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:            http://www.conduit-project.org/
Summary:        Synchronization for GNOME
Source:         http://download.gnome.org/sources/%{name}/0.3/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
BuildRequires:  dbus-devel >= 0.93
BuildRequires:  pkgconfig
BuildRequires:  python >= 1:2.4
BuildRequires:  python-dateutil
BuildRequires:  python-pygoocanvas >= 0.8.0
BuildRequires:  python-pygtk-devel >= 2:2.10
BuildRequires:  python-vobject
BuildRequires:  rpm-pythonprov
BuildRequires:  rpmbuild(macros) >= 1.219
Requires:       pydoc
Requires:       python-PyXML
Requires:       python-dateutil
Requires:       python-evolution >= 0.0.3
Requires:       python-gdata
Requires:       python-pygoocanvas >= 0.8.0
Requires:       python-pygtk-gtk >= 2:2.10
Requires:       python-vobject

%description
Conduit is a synchronization solution for GNOME which allows the user
to take their emails, files, bookmarks, and any other type of personal
information and synchronize that data with another computer, an online
service, or even another electronic device.

Conduit manages the synchronization and conversion of data into other
formats. For example, conduit allows you to;
 - Synchronize your tomboy notes to a file on a remote computer
 - Synchronize your emails to your mobile phone
 - Synchronize your bookmarks to delicious, gmail, or even your own
   webserver

%package devel
Summary: Headers for developing programs that will use %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%prep
%setup -q

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

intltoolize --force --automake
libtoolize --force
aclocal $ACLOCAL_FLAGS -I . -I m4
automake -a -c -f
autoconf

./configure --prefix=%{_prefix} \
        --mandir=%{_mandir} \
        --datadir=%{_datadir} \
        --includedir=%{_includedir} \
        --sysconfdir=%{_sysconfdir} \
        --enable-nautilus-extension=yes \
        --enable-eog-plugin=yes \
        --enable-totem-plugin=yes \

make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-, root, root)
%doc AUTHORS ChangeLog NEWS README TODO
%{_bindir}/conduit
%{_bindir}/conduit-client
%{_bindir}/conduit.real
%dir %{_libdir}/conduit
%{_libdir}/conduit/dataproviders
%{_datadir}/applications/conduit.desktop
%dir %{_datadir}/conduit
%{_datadir}/conduit/*.png
%{_datadir}/conduit/*.glade
%{_datadir}/dbus-1/services/*.service
%{_datadir}/gnome/autostart/*.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/icons/hicolor/*/*/*.svg
%{_datadir}/omf/conduit/conduit-C.omf
%dir %{_libdir}/python2.4/site-packages/conduit/conduit
%{_libdir}/python2.4/site-packages/conduit/*.py[co]
%dir %{_libdir}/python2.4/site-packages/conduit/datatypes
%{_libdir}/python2.4/site-packages/conduit/datatypes/*.py[co]
%{_datadir}/gtk-doc/html/*

%files devel
%defattr(-, root, root)
%{_libdir}/pkgconfig/*.pc

%changelog
* Mon Jun 15 2009 - halton.huo@sun.com
- Enable nautilus extension, eog plugin and totem plugin
* Tue Oct 21 2008 - halton.huo@sun.com
- Bump to 0.3.15
- Remove upstreamed patch test-fail.diff
* Mon Sep 01 2008 - halton.huo@sun.com
- Bump to 0.3.14
- Add patch test-fail.diff to fix bugzilla #550165
* Tue Aug 26 2008 - halton.huo@sun.com
- Bump to 0.3.13.1
* Thu Aug 4 2008 - jijun.yu@sun.com
- Bump to 0.3.13.
* Thu July 24 2008 - jijun.yu@sun.com
- Bump to 0.3.12.
* Wed Jun 04 2008 - nonsea@users.sourceforge.net
- Bump to 0.3.11.2
* Tue Jun 03 2008 - nonsea@users.sourceforge.net
- Bump to 0.3.11
* Mon May 26 2008 - nonsea@users.sourceforge.net
- Bump to 0.3.10
* Wed Mar 19 2008 - nonsea@users.sourceforge.net
- Bump to 0.3.9
* Mon Feb 18 2008 - nonsea@users.sourceforge.net
- Bump to 0.3.8
* Fri Feb 15 2008 - jijun.yu@sun.com
- Bump to 0.3.7
- Modify the source.
* Tue Dec 11 2007 - nonsea@users.sourceforge.net
- Initial version
