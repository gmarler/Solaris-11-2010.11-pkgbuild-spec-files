#
# Copyright (c) 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
#%include usr-gnu.inc
%define cc_is_gcc 1
%include base.inc

# TODO: write SMF manifest for rtmpsrv

Name:                SFErtmpdump
Summary:             RTMPdump -- a toolkit for RTMP streams
Version:             2.3
Source:              http://rtmpdump.mplayerhq.hu/download/rtmpdump-%{version}.tgz
Patch1:              rtmpdump-01-lsocket.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
#Requires: SFEboost
Requires: SUNWopenssl-libraries

%package devel
Summary:         %{summary} - development files
SUNW_BaseDir:    %{_basedir}
%include default-depend.inc
Requires: %name


%prep
%setup -q -n rtmpdump-%version
%patch1 -p1

%build
export CC=gcc
export CXX=g++
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi


# Rtmpdump has no configure. We'll make do.
sed -e 's:/usr/local:%{_prefix}:g' Makefile > Makefile.new
mv Makefile.new Makefile
sed -e 's:/usr/local:%{_prefix}:g' librtmp/Makefile > librtmp/Makefile.new
mv librtmp/Makefile.new librtmp/Makefile

gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm ${RPM_BUILD_ROOT}%{_libdir}/librtmp.a
mv ${RPM_BUILD_ROOT}%{_prefix}/sbin/* ${RPM_BUILD_ROOT}%{_bindir}
rm -r ${RPM_BUILD_ROOT}%{_prefix}/sbin

# move mandirs to a more sensible home
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}
mv ${RPM_BUILD_ROOT}%{_prefix}/man/* ${RPM_BUILD_ROOT}%{_mandir}
rm -r ${RPM_BUILD_ROOT}%{_prefix}/man
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
#%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/rtmpdump.1
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/librtmp.3
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/rtmpgw.8

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/librtmp/*


%changelog
* Dec 28 2010 - jchoi42@pha.jhu.edu
- Initial spec
