
# spec file for package pyorbit
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
Name:           pyorbit
License:        LGPL
Group:          System/Library
Version:        2.24.0
Release:        1
Distribution:   Java Desktop System
Vendor:	        Sun Microsystems, Inc.
Summary:        Python bindings for ORBit2
Source:         http://ftp.gnome.org/pub/GNOME/sources/pyorbit/2.24/pyorbit-%{version}.tar.bz2
URL:            http://www.gnome.org
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Docdir:         %{_defaultdocdir}/doc
Autoreqprov:    on

%define ORBit2_version 2.10.1
%{?!python_version:%define python_version 2.4}

Requires:       ORBit2 >= %{ORBit2_version}
Requires:       python >= %{python_version}
BuildRequires:  ORBit2-devel >= %{ORBit2_version}

%description
PyORBit is a Python language binding for the ORBit2 CORBA implementation.
It aims to take advantage of new features found in ORBit2 to make language 
bindings more efficient.

%package devel
Summary:      Files needed to build applications using the Python bindings for ORBit2
Group:        Development/Languages
Requires:     %{name} = %{version}

%description devel
This package contains files required to build Python applications that need
to interoperate with pyorbit.

%prep
%setup -q -n pyorbit-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS"
./configure     --prefix=%{_prefix}             \
                --sysconfdir=%{_sysconfdir}
make \
    pyexecdir=%{_libdir}/python%{python_version}/vendor-packages \
    pythondir=%{_libdir}/python%{python_version}/vendor-packages

%install
make install DESTDIR=$RPM_BUILD_ROOT \
    pyexecdir=%{_libdir}/python%{python_version}/vendor-packages \
    pythondir=%{_libdir}/python%{python_version}/vendor-packages
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.pyo" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post

%postun

%files
%defattr(-,root,root)
%{_libdir}/python?.?/vendor-packages/CORBA.py*
%{_libdir}/python?.?/vendor-packages/PortableServer.py*
%{_libdir}/python?.?/vendor-packages/ORBit.so

%doc AUTHORS NEWS README ChangeLog

%files devel
%defattr(-, root, root)
%dir %{_includedir}/pyorbit-2
%{_includedir}/pyorbit-2/pyorbit.h
%{_libdir}/pkgconfig/*

%changelog
* Mon Nov 24 2008 - laca@sun.com
- use %{pythonver} macro to select which version of Python to build with
* Mon Sep 29 2008 - christian.kelly@sun.com
- Bump to 2.24.0.
* Mon May 28 2007 - damien.carbery@sun.com
- Bump to 2.14.3.
* Mon Mar 05 2007 - damien.carbery@sun.com
- Bump to 2.14.2.
* Fri Jul 21 2006 - damien.carbery@sun.com
- Bump to 2.14.1.
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Tue Dec 20 2005 - dermot.mccluskey@sun.com
- Bump to 2.13.1
* Thu Oct 27 2005 - laca@sun.com
- move from site-packages to vendor-packages
* Fri Aug 12 2005 - rich.burridge@sun.com
- Initial Sun release
