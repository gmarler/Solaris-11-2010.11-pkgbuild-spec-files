#
# spec file for package mt-daapd
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:                    mt-daapd
License:        	 GPL
Group:                   System/Libraries
Version:                 0.2.4.2
Release:                 1
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
Summary:                 %{name} - multithreaded DAAP daemon
URL:                     http://fireflymediaserver.org
Source:                  http://sourceforge.net/projects/mt-daapd/files/mt-daapd/%{version}/%{name}-%{version}.tar.gz
BuildRoot:               %{_tmppath}/%{name}-%{version}-build


%prep
%setup -q -n %name-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_cxx_libdir}             \
            --libexecdir=%{_libexecdir}     \
            --sysconfdir=%{_sysconfdir} \
            --enable-sqlite3 --disable-mdns \
            --enable-howl --with-howl-includes=/usr/include/howl
gmake -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Oct 01 2010 - jchoi42@pha.jhu.edu
- initial spec
