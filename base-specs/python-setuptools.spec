#
# base spec file for python-setuptools
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dkenny
#

%define name python-%oname
%define tarball_version 0.6c9

Name:            setuptools
Summary:         Download, build, install, upgrade, and uninstall Python packages easily
URL:             http://peak.telecommunity.com/DevCenter/setuptools
Version:         0.6.9
Source0:         http://cheeseshop.python.org/packages/source/s/%{name}/%{name}-%{tarball_version}.tar.gz
BuildRoot:       %{_tmppath}/%{name}-%{version}-build
Requires:        Python

%{?!pythonver:%define pythonver 2.4}

%prep
%setup -q -n %name-%tarball_version

%build
python%{pythonver} setup.py build
perl -pi -e 's|^#!python|#!/usr/bin/python%{pythonver}|' easy_install.py setuptools/command/easy_install.py

%install
rm -rf $RPM_BUILD_ROOT
python%{pythonver} setup.py install --prefix=%_prefix --root=$RPM_BUILD_ROOT --old-and-unmanageable

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Mar 18 2009 - jeff.cai@sun.com
- Copied from spec-files
* Tue Nov 25 2008 - laca@sun.com
- split from SUNWpython-setuptools.spec
* Tue Nov 18 2008 - jedy.wang@sun.com
- Fix installation directory problem.
* Wed Oct 01 2008 - brian.cameron@sun.com
- Bump to 0.6.9.
* Tue Sep 16 2008 - matt.keenn@sun.com
- Update copyright
* Wed May 14 2008 - darren.kenny@sun.com
- Add SUWNPython dependency.
* Mon May 05 2008 - brian.cameron@sun.com
- Bump to 0.6.8
* Tue Mar 11 2008 - damien.carbery@sun.com
- Use %tarball_version as appropriate in %files and %pre and %install.
* Fri Mar 07 2008 - damien.carbery@sun.com
- Change package version to be numeric.
* Tue Feb 12 2008 - dermot.mccluskey@sun.com
- initial version
