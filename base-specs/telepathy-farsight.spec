#
# spec file for package telepathy-farsight
#
# Owner:elaine_sun
#

Name:           telepathy-farsight
License:        GPL
Group:          Applications/Internet
Version:        0.0.15
Release:        1
Distribution:   Java Desktop System
Vendor:         Oracle, Inc.
Summary:        A library that binds Farsigh to the Connection Manager
Source:	        http://telepathy.freedesktop.org/releases/%{name}/%{name}-%{version}.tar.gz
URL:            http://telepathy.freedesktop.org/wiki
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Docdir:         %{_defaultdocdir}/telepathy-farsight

Autoreqprov: on
Prereq:      /sbin/ldconfig

%description
This library binds Farsight to the Empathy Connection Manager via D-Bus
and the Telepathy Media Stream Spec and is used for all their streaming
requirements.

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
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%{_libexecdir}/*
%{_datadir}/doc/*

%changelog
* Fri Oct 08 2010 - jeff.cai@oracle.com
- created
