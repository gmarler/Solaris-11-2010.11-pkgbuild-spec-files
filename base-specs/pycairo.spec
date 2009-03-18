#
# spec file for package pycairo
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
Name:			pycairo
License:		LGPL	
Group:			System/Library
Version:		1.4.0
Release:		1
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		Python bindings for Cairo
Source:			http://cairographics.org/releases/pycairo-%{version}.tar.gz
URL:			http://www.cairographics.org
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/doc
Autoreqprov:		on

%{?!python_version:%define python_version 2.4}

%description
PyCairo is an extension module for python that gives you access to Cairo

%package devel
Summary: files needed to build wrappers for Cairo libraries
Group: Development/Languages
Requires: %{name} = %{version}

%description devel
This package contains files required to build wrappers for Cairo
libraries so that they interoperate with python.

%prep
%setup -q -n pycairo-%{version}

%build
autoconf
%ifos solaris
# Disable optimizations on x86 to workaround compiler bug 6382078.
%ifarch sparc
CFLAGS="$RPM_OPT_FLAGS"				\
%else
CFLAGS="$RPM_OPT_FLAGS -xO0"			\
%endif
%endif
./configure 	--prefix=%{_prefix}		\
	    	--sysconfdir=%{_sysconfdir}
make

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
%defattr(-, root, root)
%{_libdir}/python?.?/vendor-packages/*

%files devel
%defattr(-, root, root)
%doc examples
%doc AUTHORS NEWS README MAPPING ChangeLog
%{_bindir}/*
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/pycairo/*
%{_datadir}/pycairo/*

%changelog -n pycairo
* Wed Mar 18 2009 - jeff.cai@sun.com
- Copied from spec-files
* Mon Nov 24 2008 - laca@sun.com
- use %{python_version} macro to select which version of Python to build with
* Thu Mar 15 2007 - damien.carbery@sun.com
- Bump to 1.4.0.
* Mon Aug 28 2006 - harry.lu@sun.com
- Bumped to 1.2.2.
* Fri Jul 28 2006 - damien.carbery@sun.com
- Initial Sun release.
