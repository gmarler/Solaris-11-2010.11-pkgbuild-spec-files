#
# spec file for package pygobject
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
Name:			pygobject
License:		LGPL	
Group:			System/Library
Version:		2.16.1
Release:		2
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		Python bindings for GObject
Source:			http://ftp.gnome.org/pub/GNOME/sources/pygobject/2.16/pygobject-%{version}.tar.bz2
# owner:laca date:2008-08-26 type:bug
Patch1:                 pygobject-01-uninstalled-pc.diff
# owner:laca date:2008-09-12 type:bug
Patch2:                 pygobject-02-sun-studio.diff
URL:			http://www.gnome.org
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/doc
Autoreqprov:		on

%define libglade_version 2.4.0
%define glib2_version 2.6.0
%define gtk2_version 2.6.0
%define atk_version 1.8.0
%define pango_version 1.8.0
%{?!python_version:%define python_version 2.4}

Requires:		libglade >= %{libglade_version}
Requires:		gtk2 >= %{gtk2_version}
Requires:		glib2 >= %{glib2_version}
Requires:		atk >= %{atk_version}
Requires:		pango >= %{pango_version}
Requires:		python >= %{python_version}
BuildRequires: 		gtk2-devel >= %{gtk2_version}
BuildRequires:		libglade-devel >= %{libglade_version}
BuildRequires:		glib2-devel >= %{glib2_version}
BuildRequires:		atk-devel >= %{atk_version}
BuildRequires:		pango-devel >= %{pango_version}

%description
PyGObject is an extension module for python that gives you access to GObject

%package devel
Summary: files needed to build wrappers for GObject libraries
Group: Development/Languages
Requires: %{name} = %{version}

%description devel
This package contains files required to build wrappers for GObject
libraries so that they interoperate with pygobject.

%prep
%setup -q -n pygobject-%{version}
%patch1 -p1
%patch2 -p1

%build
%ifos solaris
# Disable optimizations on x86 to workaround compiler bug 6382078.
%ifarch sparc
CFLAGS="$RPM_OPT_FLAGS"				\
%else
CFLAGS="$RPM_OPT_FLAGS -xO0"			\
%endif
%endif
# Append -xc99 to fix #error failure in /usr/include/sys/feature_tests.h
CFLAGS="$CFLAGS -xc99 $EXTRA_CFLAGS"
./configure 	--prefix=%{_prefix}		\
	    	--sysconfdir=%{_sysconfdir}     \
                --without-ffi
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
%{_libdir}/python?.?/vendor-packages/*

%files devel
%defattr(-, root, root)
%doc examples
%doc AUTHORS NEWS README MAPPING ChangeLog
%{_bindir}/*
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/pygobject/*
%{_datadir}/pygobject/*

%changelog -n pygobject
* Wed Mar 18 2009 - jeff.cai@sun.com
- Copied from spec-files
* Thu Feb 26 2009 - dave.lin@sun.com
- Bump to 2.16.1
* Mon Nov 24 2008 - laca@sun.com
- use %{python_version} macro to select which version of Python to build with
* Fri Sep 12 2008 - laca@sun.com
- bump to 2.15.4; disable ffi support for now, Studio 12 will be needed
  to enable it; add patch sun-studio.diff to fix the build.
* Mon Aug 11 2008 - damien.carbery@sun.com
- Bump to 2.15.2. Remove pyexecdir and pythondir vars from make install as it
  was breaking the build.
* Wed Jul 16 2008 - damien.carbery@sun.com
- Bump to 2.15.1.
* Tue Jul 15 2008 - damien.carbery@sun.com
- Bump to 2.15.0. Remove upstream patch, 01-pc-file.
* Mon May 26 2008 - damien.carbery@sun.com
- Bump to 2.14.2.
* Fri Jan 04 2008 - damien.carbery@sun.com
- Bump to 2.14.1. Remove upstream patch, 01-uninst-datadir; rename rest.
* Tue Oct 16 2007 - damien.carbery@sun.com
- Add patch, 02-pc-file, to add entries to the pc files to support building
  against the uninstalled module.
* Sun Oct 07 2007 - damien.carbery@sun.com
- Add patch, 01-uninst-datadir, to add a 'datadir' entry to the uninstalled pc
  file.
* Wed Sep 19 2007 - damien.carbery@sun.com
- Bump to 2.14.0.
* Mon Jul 09 2007 - damien.carbery@sun.com
- Bump to 2.13.2. Remove upstream patches, 01-gcc-wall and 02-return-zero.
  Remove autofoo calls because configure.ac patches removed.
  Append -xc99 to CFLAGS to fix #error in /usr/include/sys/feature_tests.h
* Wed May 09 2007 - damien.carbery@sun.com
- Bump to 2.13.1. Remove upstream patches, 01-uninstalled.pc and 02-void-return.
  Add patches, 01-gcc-wall and 02-return-zero, to fix build issues.
* Mon Nov 27 2006 - damien.carbery@sun.com
- Remove reference to pygtk2-02-pygobject-xsl-dir.diff as it has been removed.
* Mon Nov 27 2006 - damien.carbery@sun.com
- Bump to 2.12.3.
* Sat Oct 07 2006 - brian.cameron@sun.com
- Add aclocal and automake calls.
* Wed Oct 04 2006 - damien.carbery@sun.com
- Bump to 2.12.2.
* Tue Sep 05 2006 - damien.carbery@sun.com
- Bump to 2.12.1.
* Mon Aug 28 2006 - damien.carbery@sun.com
- Bump to 2.11.4.
* Tue Aug 22 2006 - damien.carbery@sun.com
- Bump to 2.11.3.
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 2.11.2.
* Mon Aug 07 2006 - damien.carbery@sun.com
- Bump to 2.11.1.
* Fri Jul 21 2006 - damien.carbery@sun.com
- Bump to 2.11.0.
* Tue Apr 11 2006 - damien.carbery@sun.com
- Bump to 2.10.1.
* Wed Apr  5 2006 - damien.carbery@sun.com
- Initial Sun release.
