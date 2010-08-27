#
# spec file for package libxklavier
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: sureshc
#
Name:         libxklavier
License:      LGPLv2+
Group:        System/Libraries
Version:      4.0
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      High-level API for X Keyboard Extension(XKB)
Source:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/4.0/libxklavier-%{version}.tar.bz2
#Source1:      l10n-configure.sh
#Source2:      %{name}-po-sun-%{po_sun_version}.tar.bz2
#Patch1:       libxklavier-01-null-dpy-pointer.diff
# date:2009-07-15 owner:sureshc type:bug
Patch1:       libxklavier-01-compile-makefile.diff
Patch2:       libxklavier-02-fixcrash.diff
#Patch2:       libxklavier-02-xsun-fail.diff
URL:          http://www.freedesktop.org/Software/LibXklavier
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/doc
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define libxml2_version 2.6.7
%define glib2_version   2.6.0

BuildRequires: libxml2-devel >= %{libxml2_version}
BuildRequires: libxkbfile-devel
BuildRequires: libX11-devel
BuildRequires: libXi-devel
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: iso-codes-devel

Requires: libxml2 >= %{libxml2_version}

%description
libxklavier provides high level APIs to access X Keyboard Extention(XKB) functionality. Used for creating keyboard layouts etc.

%package devel
Summary:      X Keyboard Extension high level APIs 
Group:        Development/Libraries
Requires:     %{name} = %{version}
Requires:     libxml2-devel >= %{libxml2_version}

%description devel
This package contains libraries, header files and developer documentation for libxklavier library.

%prep
%setup -q
#bzip2 -c -d %SOURCE2 | tar xf -
%patch1 -p1
%patch2 -p1

#bash -x %SOURCE1

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

CFLAGS="$RPM_OPT_FLAGS"			\

aclocal $ACLOCAL_FLAGS
automake

%ifos solaris
%define xkbbase /usr/X11/lib/X11/xkb
./configure --prefix=%{_prefix}		\
	    --x-includes=/usr/openwin/include \
            --with-xkb-base=%xkbbase \
	    --libdir=%{_libdir} \
	    --sysconfdir=%{_sysconfdir}
%else
./configure --prefix=%{_prefix}		\
	    --sysconfdir=%{_sysconfdir}
%endif

make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install 
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr (-, root, root)
%{_libdir}/*.so.*

%files devel
%defattr (-, root, root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/libxklavier
%{_datadir}/libxklavier

%changelog
* Mon Oct 05 2009 - <suresh.chandrasekharan@sun.com>
- initial Sun release.
