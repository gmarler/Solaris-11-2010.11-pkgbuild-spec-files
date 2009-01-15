#
# spec file for package ggz-gtk-client
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#

Name:           ggz-gtk-client
License:        GPLv2+
Group:          Development/Libraries
Version:        0.0.14.1
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:            http://www.ggzgamingzone.org/
Summary:        Gtk+ client libraries for GGZ gaming zone
Source:         http://mirrors.ibiblio.org/pub/mirrors/ggzgamingzone/ggz/%{version}/%{name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Docdir:         %{_defaultdocdir}/doc


BuildRequires:  libggz-devel
BuildRequires:  ggz-client-libs-devel
BuildRequires:  gtk2-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gettext

%description
The GGZ Gaming Zone GTK+ Client provides a GTK+ 2.x user interface
for logging into a GGZ server, chatting with other players, and
locating and launching game tables.

%package devel
Summary:        Development files for %{name}
Group:	        Development/Libraries
Requires:       %{name} = %{version}
Requires:       libggz-devel
Requires:       ggz-client-libs-devel
Requires:       gtk2-devel

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

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

libtoolize --force
aclocal $ACLOCAL_FLAGS -I . -I m4 -I m4/ggz
autoheader
automake -a -c -f
autoconf

./configure --prefix=%{_prefix}         \
            --sysconfdir=%{_sysconfdir} \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --includedir=%{_includedir} \
            --libexecdir=%{_libexecdir} \
            --enable-static=no \
%if %debug_build
            --enable-debug=yes \
%else
            --enable-debug=no \
%endif

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README README.GGZ NEWS COPYING
%{_bindir}/ggz-gtk
%{_libdir}/libggz-gtk.so.*
%{_datadir}/applications/fedora-ggz-gtk.desktop
%{_datadir}/ggz/
%{_mandir}/man6/ggz-gtk.6.gz


%files devel
%defattr(-,root,root,-)
%{_libdir}/libggz-gtk.so
%{_includedir}/ggz-*.h

%changelog
* Thu Jan 15 2009 - halton.huo@sun.com
- Initial version
