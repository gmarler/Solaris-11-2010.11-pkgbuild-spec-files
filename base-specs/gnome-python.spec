#
# spec file for package gnome-python
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
Name:			gnome-python
License:		LGPL	
Group:			System/Library
Version:		2.25.90
Release:		1
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		Python bindings for various GNOME libraries
Source:			http://ftp.gnome.org/pub/GNOME/sources/gnome-python/2.25/gnome-python-%{version}.tar.bz2
URL:			http://www.gnome.org
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/doc
Autoreqprov:		off

%define libglade_version           2.4.0
%{?!python_version:%define python_version 2.4}
%define pygtk2_version             2.4.0
%define pyorbit_version            2.0.1
%define libgnomeui_version         2.0.0
%define gconf_version              1.2.0
%define nautilus_version           2.0.0
%define gnome_panel_version        2.0.0
%define gtkhtml_version            2.3.1
%define libgnomeprintui_version    2.2.0

Requires: python >= %{python_version}
Requires: pygtk2 >= %{pygtk2_version}
Requires: pyorbit >= %{pyorbit_version}
Requires: libgnomeui >= %{libgnomeui_version}
Requires: libglade >= %{libglade_version}
Requires: GConf >= %{gconf_version}
Requires: nautilus >= %{nautilus_version}
Requires: gnome-panel >= %{gnome_panel_version}
Requires: gtkhtml >= %{gtkhtml_version}
Requires: libgnomeprintui >= %{libgnomeprintui_version}

BuildRequires: python >= %{python_version}
BuildRequires: pygtk2-devel >= %{pygtk2_version}
BuildRequires: pyorbit-devel >= %{pyorbit_version}
BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: GConf-devel >= %{gconf_version}
BuildRequires: nautilus-devel >= %{nautilus_version}
BuildRequires: gnome-panel-devel >= %{gnome_panel_version}
BuildRequires: gtkhtml-devel >= %{gtkhtml_version}
BuildRequires: libgnomeprintui-devel >= %{libgnomeprintui_version}

%description
GNOME-Python provides the Python language bindings for the GNOME libraries.

%package devel
Summary: Files needed to build applications using the Python bindings for GNOME libraries
Group: Development/Languages
Requires: %{name} = %{version}

%description devel
This package contains files required to build Python applications that need 
to interope rate with the various GNOME libraries

%prep
%setup -q -n gnome-python-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS"				\
./configure 	--prefix=%{_prefix}		\
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
%defattr(-, root, root)
%{_libdir}/python?.?/vendor-packages/gtk-2.0
%{_libdir}/gnome-vfs-*/modules/lib*.so

%doc AUTHORS NEWS README ChangeLog
%doc examples

%files devel
%defattr(644, root, root)
%{_libdir}/pkgconfig/*
%{_datadir}/pygtk
%{_includedir}/*

%changelog -n gnome-python
* Mon Feb 16 2009 - dave.lin@sun.com
- Bump to 2.25.90
* Mon Nov 24 2008 - laca@sun.com
- use %{python_version} macro to select with version of Python to build which
* Mon Sep 29 2008 - christian.kelly@sun.com
- Bump to 2.22.3.
* Mon Jun 16 2008 - damien.carbery@sun.com
- Bump to 2.22.1.
* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Mon Feb 25 2008 - damien.carbery@sun.com
- Bump to 2.21.1.
* Tue Dec 04 2007 - damien.carbery@sun.com
- Bump to 2.21.0.
* Tue Nov 27 2007 - damien.carbery@sun.com
- Bump to 2.20.1.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Tue Jul 31 2007 - damien.carbery@sun.com
- Bump to 2.19.2.
* Mon Jul 09 2007 - damien.carbery@sun.com
- Bump to 2.19.1.
* Thu Apr 12 2007 - damien.carbery@sun.com
- Bump to 2.18.2.
* Thu Apr 12 2007 - damien.carbery@sun.com
- Bump to 2.18.1.
* Mon Mar 12 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Mon Mar 05 2007 - damien.carbery@sun.com
- Bump to 2.17.92.
* Wed Jan 10 2007 - damien.carbery@sun.com
- Bump back to 2.17.2. Laca fixed an issue in pycc in SUNWPython.
* Tue Jan 09 2007 - damien.carbery@sun.com
- Unbump back to 2.16.2 as 2.17.[12] kill the build machine during configure.
* Mon Jan 08 2007 - damien.carbery@sun.com
- Bump to 2.17.2.
* Mon Nov 06 2006 - damien.carbery@sun.com
- Bump to 2.16.2.
* Mon Nov 06 2006 - damien.carbery@sun.com
- Bump to 2.16.1.
* Tue Sep 05 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Tue Aug 22 2006 - damien.carbery@sun.com
- Bump to 2.15.91.
* Wed Jul 26 2006 - damien.carbery@sun.com
- Bump to 2.15.90.
* Fri Jul 21 2006 - damien.carbery@sun.com
- Bump to 2.15.4.
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.12.4.
* Tue Jan 03 2006 - dermot.mccluskey@sun.com
- Bump to 2.12.3.
* Tue Dec 20 2005 - dermot.mccluskey@sun.com
- Bump to 2.12.2
* Thu Oct 27 2005 - laca@sun.com
- move from site-packages to vendor-packages
- include the .pyc files
* Fri Aug 26 2005 - laca@sun.com
- fix dependencies, fix %files
* Fri Aug 12 2005 - rich.burridge@sun.com
- Initial Sun release
