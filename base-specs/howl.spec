#
# spec file for package howl
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:                    howl
License:        	 GPL
Group:                   System/Libraries
Version:                 1.0.0
Release:                 1
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
Summary:                 howl - mDNS responder daemon
URL:                     http://www.porchdogsoft.com/products/howl/
Source:                  http://www.porchdogsoft.com/download/%{name}-%{version}.tar.gz
Patch1:                  howl-01-ordering.diff
Patch2:                  howl-02-ifreq.diff
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n howl-%version
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_cxx_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir} --disable-python
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Oct 01 2010 - jchoi42@pha.jhu.edu
- initial spec
