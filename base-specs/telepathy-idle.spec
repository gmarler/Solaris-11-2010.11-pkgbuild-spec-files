#
# spec file for package telepathy-idle
#
# Owner:elaine_sun
#

Name:           telepathy-idle
License:        GPL
Group:          Applications/Internet
Version:        0.1.6
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
Summary:        An IRC connection manager for Telepathy framework.
Source:	        http://telepathy.freedesktop.org/releases/%{name}/%{name}-%{version}.tar.gz
URL:            http://telepathy.freedesktop.org/wiki
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Docdir:         %{_defaultdocdir}/telepathy-idle

Autoreqprov: on
Prereq:      /sbin/ldconfig

%description
An IRC connection manager for Telepathy framework.

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

CFLAGS="$RPM_OPT_FLAGS"			        \
./configure --prefix=%{_prefix}         \
            --mandir=%{_mandir}         \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS

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
* Wed Sep 29 2010 - jeff.cai@oracle.com
- Bump to 0.1.6
- Upstream -01-misc
* Wed may 27 2009 - elaine.xiong@sun.com
- created
