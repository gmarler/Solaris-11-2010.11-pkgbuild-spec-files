#
# spec file for package SFElibpigment
#
# includes module(s): pigment
#
# Copyright (c) 2008, 2010, Oracle and/or its affiliates. All rights reserved.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%define OSR 9492:0.3.6

#
# bugdb: https://code.fluendo.com/pigment/trac/
#
%define version 0.3.17

%include Solaris.inc

Summary:         Pigment user interface library with embedded multimedia
Name:            SFElibpigment
IPS_package_name: library/desktop/pigment
Meta(info.classification): %{classification_prefix}:System/Multimedia Libraries
License:	 LGPL v2.1
Vendor:          fluendo.com
Version:         %{version}
URL:             https://core.fluendo.com/pigment/trac
Source0:         http://elisa.fluendo.com/static/download/pigment/pigment-%{version}.tar.bz2
SUNW_BaseDir:    %{_basedir}

BuildRoot:       %{_tmppath}/%{name}-%{version}-build
BuildRequires:   SUNWgtk2-devel
BuildRequires:   SUNWgnome-common-devel
BuildRequires:   SUNWgnome-media-devel
Requires:        SUNWgtk2
Requires:        SUNWgnome-media

BuildRequires:   SUNWxorg-mesa
Requires:        SUNWxorg-mesa

%include default-depend.inc

%description
Pigment is a library designed to easily build user interfaces 
with embedded multimedia. Its design allows to use it on several 
platforms, thanks to a plugin system allowing to choose the underlying 
graphical API. Pigment is the rendering engine of Elisa, the Fluendo 
Media Center project.

%package devel
Group: Development/Tools
Summary: Development headers for Pigment
Requires: %name

%prep
%setup -q -n pigment-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

aclocal $ACLOCAL_FLAGS -I ./common/m4
gtkdocize
autoheader
automake -a -c -f
autoconf
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}
make 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -r $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -r $RPM_BUILD_ROOT/%{_libdir}/*.a
rm -r $RPM_BUILD_ROOT/%{_libdir}/pigment-0.3/%{version}/*.la
rm -r $RPM_BUILD_ROOT/%{_libdir}/pigment-0.3/%{version}/*.a

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc README AUTHORS
%doc(bzip2) NEWS COPYING ChangeLog
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/pigment-0.3/%{version}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/gtk-doc
%dir %attr (0755, root, bin) %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/*


%changelog
* Tue Dec 07 2010 - brian.cameron@oracle.com
- Migrated to SFE.
* Sat Apr 24 2010 - dave.lin@sun.com
- Obsoleted useless macro 'name'.
* Fri Jan 09 2009 - brian.cameron@sun.com
- Add SUNWglrt and SUNWxorg-mesa as dependencies.  Fixes bug
  #6791253.
* Wed Nov 12 2008 Jerry Tan <jerry.tan@sun.com>
- Bump to 0.3.12
* Mon Oct 13 2008  Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.3.11.
* Tue Sep 30 2008  Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.3.10.
* Wed Sep 17 2008  Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.3.9.  Remove upstream patch pigment-01-m4.diff.
* Thu Sep 10 2008 Jerry Yu <jijun.yu@sun.com>
- Bump to 0.3.8.
- Add patch pigment-01-m4.diff.
* Thu Jul 31 2008 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.3.7.
* Wed Jul 23 2008 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.3.6.
* Wed Mar 19 2008 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.3.5.
* Wed Feb 06 2008 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.3.4.
* Wed Jan 16 2008 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.3.3.  Remove upstream patch.
* Fri Oct 05 2007 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.3.2
* Sun Aug 05 2007 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.3.1
* Tue Jul 10 2007 Brian Cameron  <brian.cameron@sun.com>
- Create spec file.
