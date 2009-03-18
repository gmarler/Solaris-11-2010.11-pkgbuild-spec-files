#
# spec file for package pygtk2
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
Name:			pygtk2
License:		LGPL	
Group:			System/Library
Version:		2.14.1
Release:		2
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		Python bindings for GTK+
Source:			http://ftp.gnome.org/pub/GNOME/sources/pygtk/2.14/pygtk-%{version}.tar.bz2
# date:2005-10-27 owner:dcarbery type:feature bugzilla:385131
Patch1:                 pygtk2-01-uninstalled.pc.diff
# The numpy integration patch is based on the pygtk_r2808_patch_for_numpy found
# at this URL - http://www.scipy.org/Porting_to_NumPy.
# date:2007-10-22 owner:yippi type:bug bugzilla:397544 bugster:6602536
Patch2:                 pygtk2-02-numpy-r2808.diff
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
PyGTK is an extension module for python that gives you access to the GTK+
widget set.  Just about anything you can write in C with GTK+ you can write
in python with PyGTK (within reason), but with all the benefits of python.

%package devel
Summary: files needed to build wrappers for GTK+ addon libraries
Group: Development/Languages
Requires: %{name} = %{version}

%description devel
This package contains files required to build wrappers for GTK+ addon
libraries so that they interoperate with pygtk.

%prep
%setup -q -n pygtk-%{version}
%patch1 -p1
%patch2 -p1

%build
numpy_INCLUDES=`$PYTHON -c "import numpy; print numpy.get_include()"`
export CFLAGS="$CFLAGS -I$numpy_INCLUDES"
aclocal $ACLOCAL_FLAGS -I ./m4
libtoolize --force
autoheader
autoconf
./configure 	--prefix=%{_prefix}		\
	    	--sysconfdir=%{_sysconfdir}
make

%install
make install DESTDIR=$RPM_BUILD_ROOT \
    pyexecdir=%{_libdir}/python%{python_version}/vendor-packages \
    pythondir=%{_libdir}/python%{python_version}/vendor-packages
perl -pi -e s,/site-packages,/vendor-packages, \
    $RPM_BUILD_ROOT%{_libdir}/pkgconfig/pygtk-2.0.pc
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
%{_libdir}/pygtk/*
%{_datadir}/pygtk/*

%changelog -n pygtk2
* Wed Mar 18 2009 - jeff.cai@sun.com
- Copied from spec-files
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.14.1
* Thu Feb 12 2009 - brian.cameron@sun.com
- Bump to 2.14.0.  Add autotools commands before calling configure, now needed
  to build.
* Mon Nov 24 2008 - laca@sun.com
- use %{python_version} macro to select with version of Python to build which
* Tue Aug 26 2008 - dave.lin@sun.com
- Bump to 2.13.0, update the following patches to fix the hunk failures,
    pygtk2-01-uninstalled.pc.diff
    pygtk2-02-numpy-r2808.diff
* Fri Jan 04 2008 - damien.carbery@sun.com
- Bump to 2.12.1.
* Mon Oct 22 2007 - brian.cameron@sun.com
- Add patch so pygtk builds against numpy to add numeric processing extension
  support.
* Wed Sep 19 2007 - damien.carbery@sun.com
- Bump to 2.12.0.
* Mon Aug 27 2007 - damien.carbery@sun.com
- Bump to 2.11.0.
* Wed Jul 11 2007 - damien.carbery@sun.com
- Bump to 2.10.5. Remove obsolete patch, 02-gtk-tooltips.
* Fri Jun 22 2007 - damien.carbery@sun.com
- Add patch 02-gtk-tooltips to fix bugzilla 449318 (pygtk not in sync with gtk+)
* Tue Feb  6 2007 - damien.carbery@sun.com
- Bump to 2.10.4.
* Thu Dec 14 2006 - damien.carbery@sun.com
- Remove patch 02-pygobject-xsl-dir as nothing is built in the docs dir.
* Wed Oct 04 2006 - damien.carbery@sun.com
- Bump to 2.10.3.
* Tue Oct 03 2006 - damien.carbery@sun.com
- Bump to 2.10.2.
* Sat Sep  9 2006 - laca@sun.com
- re-enable optimisation as the compiler bug that prevented it has been fixed
* Tue Sep 05 2006 - damien.carbery@sun.com
- Bump to 2.10.1.
* Mon Aug 28 2006 - harry.lu@sun.com
- Bump to 2.9.6 really
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 2.9.6.
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 2.9.5.
* Mon Aug 07 2006 - damien.carbery@sun.com
- Bump to 2.9.4.
* Fri Jul 21 2006 - damien.carbery@sun.com
- Bump to 2.9.3.
* Tue Apr  4 2006 - damien.carbery@sun.com
- Bump to 2.9.0.
* Fri Mar 31 2006 - damien.carbery@sun.com
- Bump to 2.8.5.
* Wed Feb 15 2006 - damien.carbery@sun.com
- Disable optimizations on x86 to workaround compiler bug 6382078.
* Sun Jan 15 2006 - damien.carbery@sun.com
- Bump to 2.8.4
* Tue Dec 20 2005 - dermot.mccluskey@sun.com
- Bump to 2.8.2
* Thu Oct 27 2005 - laca@sun.com
- add patch uninstalled.pc.diff so the pygtk can be included in the same
  Solaris pkg as gnome-python
- move from site-packages to vendor-packages
* Tue Sep 27 2005 - damien.carbery@sun.com
- Bump to 2.7.4.
* Thu Aug 25 2005 rich.burridge@sun.com
- Adjusted the defattr lines to have three parameters, not four.
* Tue Aug 16 2005 - damien.carbery@sun.com
- Bump to 2.7.3.
* Mon Aug 04 2003 - glynn.foster@sun.com
- Initial Sun release
