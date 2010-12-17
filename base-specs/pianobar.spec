#
# spec file for package pianobar
#
# Copyright 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%define rev_num 13167
%define ver_num 2010.11.06

Name:         pianobar
License:      MIT
Version:      %ver_num
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      pianobar - console client for Pandora web radio
Source:       http://download.github.com/PromyLOPh-pianobar-%{ver_num}-0-gec%{rev_num}.tar.gz

Patch1:       pianobar-01-defs.diff
# ugly hack to get gcc to link with -lsocket
Patch2:       pianobar-02-lsocket.diff

URL:          https://github.com/PromyLOPh/pianobar
BuildRoot:               %{_tmppath}/%{name}-%{version}-build


%prep
rm -rf PromyLOPh-pianobar-ec%{rev_num}
mkdir PromyLOPh-pianobar-ec%{rev_num}
gtar xzf %SOURCE
cd PromyLOPh-pianobar-ec%{rev_num}
%patch1 -p1
%patch2 -p1


%build
cd PromyLOPh-pianobar-ec%{rev_num}
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
gmake -j$CPUS 

%install
cd PromyLOPh-pianobar-ec%{rev_num}
gmake install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Wed Dec 16 2010 - jchoi42@pha.jhu.edu
- initial spec
