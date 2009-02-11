#
# spec file for package telepathy-haze
#
# Owner:alfred
#

Name:           telepathy-haze
License:        GPL
Group:          Applications/Internet
Version:        0.2.1
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
Summary:        IM backend
Source:			http://telepathy.freedesktop.org/releases/%{name}/%{name}-%{version}.tar.gz
# date:2009-02-11 owner:alfred type:bug
Patch1:	        telepathy-haze-01-configure.diff
URL:            http://developer.pidgin.im/wiki/Telepathy
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Docdir:         %{_defaultdocdir}/telepathy-haze

Autoreqprov: on
Prereq:      /sbin/ldconfig

%description
A connection manager based on libpurple, bringing support for Pidgin's IM
protocols to the Telepathy framework.

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

rm -rf m4/lt*.m4
rm -rf m4/libtool.m4

CFLAGS="$RPM_OPT_FLAGS"			        \
./configure --prefix=%{_prefix}         \
            --mandir=%{_mandir}         \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir}

make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%{_libexecdir}/*
%{_datadir}/doc/*

%changelog
* Wed Feb 11 2009 - alfred.peng@sun.com
- created
