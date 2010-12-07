#
# spec file for package SFEpigment-python
#
# includes module(s): pigment-python
#
# Copyright (c) 2009, 2010, Oracle and/or its affiliates. All rights reserved.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#
# bugdb: https://code.fluendo.com/pigment/trac/
#
%include Solaris.inc
%define pythonver 2.6

%use pypigment= libpigment-python.spec

Name:            SFElibpigment-python26
IPS_package_name: library/python-2/python-pigment-26
Meta(info.classification): %{classification_prefix}:System/Multimedia Libraries
Vendor:          Sun Microsystems, Inc.
Summary:      Pigment user interface library with embedded multimedia
Version:         %{pypigment.version}
License:         LGPL v2.1
SUNW_BaseDir:    %{_basedir}

BuildRoot:       %{_tmppath}/%{name}-%{version}-build
BuildRequires:   SUNWPython26-devel
BuildRequires:   SUNWgnome-common-devel
BuildRequires:   SUNWgnome-media-devel
BuildRequires:   SUNWgnome-python26-libs-devel
BuildRequires:   SUNWgst-python26
BuildRequires:   SFElibpigment-devel
BuildRequires:   SUNWpython26-setuptools
Requires:        SUNWgnome-media
Requires:        SUNWgnome-python26-libs
Requires:        SFElibpigment
Requires:        SUNWgst-python26

%description
pigment python binding for python %{pythonver}

%include default-depend.inc

%prep

rm -rf %name-%version
mkdir -p %name-%version
%pypigment.prep -d %name-%version

%build
%pypigment.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%pypigment.install -d %name-%version
rm -rf $RPM_BUILD_ROOT/usr/share/pigment-python

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc -d %{pypigment.name}-%{pypigment.version} README AUTHORS
%doc(bzip2) -d %{pypigment.name}-%{pypigment.version} NEWS COPYING ChangeLog
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/_pgmgtkmodule.so
%{_libdir}/python%{pythonver}/vendor-packages/_pgmmodule.so
%{_libdir}/python%{pythonver}/vendor-packages/_pgmimagingmodule.so
%{_libdir}/python%{pythonver}/vendor-packages/pgm
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
#%{_datadir}/pigment-python

%changelog
* Tue Dec 07 2010 - brian.cameron@oracle.com
- Migrate to SFE.
* Thu Feb 12 2009 Brian Cameron  <brian.cameron@sun.com>
- created 2.6 version based on SUNWlibpigment-python.spec.
* Tus Nov 11 2008 Jerry Tan <jerry.tan@sun.com>
- Bump to 0.3.9
* Tue Sep 30 2008 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.3.8.
* Wed Sep 17 2008 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.3.7.
* Thu Sep 11 2008 Jerry Yu <jijun.yu@sun.com>
- Bump to 0.3.6.
* Thu Jul 31 2008 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.3.5.
* Wed Jul 23 2008 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.3.4.
* Wed Mar 19 2008 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.3.3
* Wed Feb 06 2008 Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.3.2.
* Wed Jan 16 2008 Brian Cameron  <brian.cameron@sun.com>
- Created.
