# spec file for package gdl
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner:halton
#

Name:           pcmanx-gtk2
Version:        0.3.8
Release:        1
Summary:        user-friendly telnet client designed for BBS browsing.
Vendor:         Sun Microsystems, Inc.
Distribution:   Java Desktop System
Group:          Applications/Internet
License:        GPL
Url:            http://pcmanx.csie.net
Source:         http://pcmanx.csie.net/release/%{name}-%{version}.tar.bz2
# date:2009-04-10 owner:halton type:bug
Patch1:         %{name}-01-solaris-socket.diff
# date:2009-04-10 owner:halton type:bug
Patch2:         %{name}-02-suncc-char.diff
# date:2009-04-10 owner:halton type:bug
Patch3:         %{name}-03-suncc-init-array.diff
# date:2009-04-10 owner:halton type:bug
Patch4:         %{name}-04-solaris-ld.diff
# date:2009-04-10 owner:halton type:bug
Patch5:         %{name}-05-no-libutils.diff

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:    gettext, pkgconfig, gtk2-devel >= 2.4.0, desktop-file-utils
Requires:         gtk2

%description
An easy-to-use telnet client mainly targets BBS users.
PCMan X is a newly developed GPL'd version of PCMan, a full-featured famous BBS
client formerly designed for MS Windows only. It aimed to be an easy-to-use yet
full-featured telnet client facilitating BBS browsing with the ability to
process double-byte characters.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

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

aclocal $ACLOCAL_FLAGS -I .
autoheader
libtoolize --force
intltoolize -c --automake --force
automake -a -c -f
autoconf

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --datadir=%{_datadir} \
            --includedir=%{_includedir} \
            --sysconfdir=%{_sysconfdir} \
            --disable-external \
            --enable-wget \
            --enable-iplookup \
            --enable-proxy

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT

export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc ABOUT-NLS AUTHORS COPYING INSTALL NEWS README TODO
%{_bindir}/pcmanx
%{_libdir}/libpcmanx*
%{_datadir}/applications/pcmanx.desktop
%{_datadir}/pcmanx/
%{_datadir}/pixmaps/pcmanx.png
%{_datadir}/locale/

%changelog
* Fri Apr 10 2009 - halton.huo@sun.com
- Initial version
