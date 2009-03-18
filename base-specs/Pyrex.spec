#
# spec file for package Pyrex
#
# includes module(s): Pyrex
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#

%{!?pythonver:%define pythonver 2.4}

Name:         Pyrex
License:      Free
Group:        Development/Languages/Python
# Unbumped to 0.9.4.1 because 0.9.5.1a breaks at-spi part of
# SUNWgnome-python-libs.
#%define tarball_version 0.9.5.1a
%define tarball_version 0.9.4.1
Version:      0.9.4.1
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Pyrex, a language for writing Python extension modules
Source:       http://www.cosc.canterbury.ac.nz/greg.ewing/python/%{name}/oldtar/%{name}-%{tarball_version}.tar.gz
URL:          http://www.cosc.canterbury.ac.nz/~greg/python/Pyrex/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/doc
Autoreqprov:  off
Prereq:       /sbin/ldconfig
Requires:      python >= %{pythonver}
BuildRequires: python >= %{pythonver}

%description
Pyrex lets you write code that mixes Python and C data types any way
you want, and compiles it into a C extension for Python.

%prep
%setup -q -n Pyrex-%{tarball_version}

%build

%install
python%{pythonver} setup.py install --prefix=%{_prefix} --root=$RPM_BUILD_ROOT

# move to vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%{_bindir}
%{_libdir}/python%{pythonver}/vendor-packages

%changelog
* Wed Mar 18 2009 - jeff.cai@sun.com
- Copied from spec-files
* Mon Nov 24 2008 - laca@sun.com
- use %{pythonver} macro to select which version of Python to build with
* Mon Nov 17 2007 - jedy.wang@sun.com
- Fix installation directory bug.
* Fri Mar  2 2007 - laca@sun.com
- bump to 0.9.5.1a
* Sat Jul 22 2006 - damien.carbery@sun.com
- Bump to 0.9.4.1.
* Thu Oct 27 2005 - laca@sun.com
- move from site-packages to vendor-packages
* Mon Oct 24 2005 - damien.carbery@sun.com
- Include .pyc files. A Google search indicates that most people include them.
* Thu Oct 20 2005 - damien.carbery@sun.com
- Delete .pyc files so they are not included in the package.
* Wed Oct 19 2005 - damien.carbery@sun.com
- Correct install location.
- Initial version.
