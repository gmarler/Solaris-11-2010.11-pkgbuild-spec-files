#
# spec file for package elementtree
#
# includes module(s): elementtree (Python module)
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
%{?!pythonver:%define pythonver 2.4}

Name:         elementtree
License:      BSD-like
Group:        Development/Languages/Python
Version:      1.2.6-20050316
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Elementtree Python module
Source:       http://effbot.org/downloads/elementtree-%{version}.tar.gz
URL:          http://effbot.org/zone/element-index.htm
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/doc
Autoreqprov:  off
Prereq:       /sbin/ldconfig
Requires:      python >= %{pythonver}
BuildRequires: python >= %{pythonver}

%description
The Element type is a simple but flexible container object, designed to
store hierarchical data structures, such as simplified XML infosets,
in memory.  The element type can be described as a cross between a
Python list and a Python dictionary.

The ElementTree wrapper adds code to load XML files as trees of Element
objects, and save them back again.

%prep
%setup -q

%build

%install
python%{pythonver} setup.py install --prefix=%{_prefix} --root=$RPM_BUILD_ROOT

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

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
* Thu Jul 27 2006 - laca@sun.com
- create
