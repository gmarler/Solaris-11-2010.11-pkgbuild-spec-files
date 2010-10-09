#
# spec file for package farsight2
#
# Owner:elaine_sun
#

Name:           farsight2
License:        GPL
Group:          Applications/Internet
Version:        0.0.21
Release:        1
Distribution:   Java Desktop System
Vendor:         Oracle, Inc.
Summary:        A library that binds Farsigh to the Connection Manager
Source:	        http://farsight.freedesktop.org/releases/%{name}/%{name}-%{version}.tar.gz
URL:            http://farsight.freedesktop.org/wiki
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Docdir:         %{_defaultdocdir}/farsight2


Autoreqprov: on
Prereq:      /sbin/ldconfig

# date:2010-10-08 owner:jefftsai type:bug bugzilla:xxx
Patch1:       farsight2-01-sockaddr.diff

%description
This library binds Farsight to the Empathy Connection Manager via D-Bus
and the Telepathy Media Stream Spec and is used for all their streaming
requirements.

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

CFLAGS="$RPM_OPT_FLAGS"			        \
./configure --prefix=%{_prefix}         \
            --mandir=%{_mandir}         \
            --libdir=%{_libdir} \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name "*.la"|xargs rm -rf 
find $RPM_BUILD_ROOT -name "*.a"|xargs rm -rf 

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
