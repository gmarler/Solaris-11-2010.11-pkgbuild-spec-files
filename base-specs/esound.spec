#
# spec file for package esound
#
# Copyright (c) 2007, 2010, Oracle and/or its affiliates. All rights reserved.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%define owner yippi
#

%define OSR LFI#105446 (gnome Exec. summary):n/a

Name:         esound
License:      LGPL v2
Group:        System/Library/GNOME
Version:      0.2.41
Release:      1
Distribution: Java Desktop System
Vendor:       Gnome Community
Summary:      esound - The Enlightened Sound Daemon
Source:       http://ftp.gnome.org/pub/GNOME/sources/esound/0.2/esound-%{version}.tar.bz2
Patch1:       esound-01-build.diff
URL:          http://www.tux.org/~ricdude/overview.html
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on
Requires:     audiofile

%description
The Enlightened Sound Daemon (ESD or EsounD) is the sound server for
Enlightenment and GNOME. It mixes several sound streams into one for output.
It can also manage network-transparent audio.

%prep
%setup -q
%patch1 -p1

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

%if %debug_build
%define debug_opt --enable-debugging
%else
%define debug_opt --disable-debugging
%endif

libtoolize --force
aclocal $ACLOCAL_FLAGS -I .
autoconf
automake -a -c -f
./configure --prefix=%{_prefix}				\
	    --sysconfdir=%{_sysconfdir} 		\
            --with-esd-dir=%{_prefix}/lib		\
            --libdir=%{_libdir}                         \
            --bindir=%{_bindir}                         \
            --libexecdir=%{_prefix}/lib                 \
            --disable-audiofiletest                     \
	    --mandir=%{_mandir} %{debug_opt}
make -j$CPUS


%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%{_bindir}/*
%{_libdir}/*
%{_sysconfdir}/*

%changelog
* Tue Dec 07 2010 - brian.cameron@oracle.com
- Created.
