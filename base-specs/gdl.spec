#
# spec file for package gdl
#
# Copyright (c) 2010, Oracle and/or its affiliates. All rights reserved.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner:halton
#

Name:		gdl
License:	GPL
Group:		Development/Libraries
Version:	2.30.0
Release:	1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:		http://www.gnome.org
Summary:	Components and library for GNOME development tools.
Source:		http://download.gnome.org/sources/%{name}/2.30/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

Requires: 	gtk2 >= 2.4.0
Requires: 	libgnomeui >= 2.6.0
Requires: 	libxml2 >= 2.2.8
Requires: 	libglade2 >= 2.0.0

%description
This package contains components and libraries that are intended to be
shared between GNOME development tools, including gnome-build and anjuta2.

The current pieces of GDL include:

# - A code-editing bonbono component based on the Scintilla
#   widget (scintilla-control).
#
Now the editor widget is the glimmer component that use gtksourceview

 - A utility library that also contains the stubs and skels for
   the above components (gdl).


%package devel
Summary:	Libraries and include files for gdl.
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Libraries and header files if you want to make use of the gdl library in your
own programs.


%prep
%setup -q

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

libtoolize --force
aclocal $ACLOCAL_FLAGS -I .
gtkdocize
autoheader
automake -a -c -f
autoconf

./configure --prefix=%{_prefix} \
	    --bindir=%{_bindir} \
	    --mandir=%{_mandir} \
	    --libdir=%{_libdir} \
	    --datadir=%{_datadir} \
	    --includedir=%{_includedir} \
	    --sysconfdir=%{_sysconfdir} \
	    %gtk_doc_option

make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT


%files
%doc AUTHORS COPYING ChangeLog NEWS README
%defattr (-, root, root)
%{_prefix}/lib/lib*.so.*
%{_prefix}/share/gdl
%{_prefix}/share/locale/*/LC_MESSAGES/*

%files devel
%defattr (-, root, root)
%{_prefix}/include/libgdl-1.0
%{_prefix}/lib/lib*.a
%{_prefix}/lib/lib*.la
%{_prefix}/lib/lib*.so
%{_prefix}/lib/pkgconfig/*

%changelog
* Tue Apr 06 2010 - halton.huo@sun.com
- Bump to 2.30.0
* Mon Jun 15 2009 - halton.huo@sun.com
- Bump to 2.27.3
* Tue May 05 2009 - halton.huo@sun.com
- Bump to 2.27.1
* Tue Mar 03 2009 - halton.huo@sun.com
- Bump to 2.25.92
* Fri Jan 16 2009 - halton.huo@sun.com
- Bump to 2.24.0
* Wed Aug 20 2008 - nonsea@users.sourceforge.net
- Bump to 2.23.90
* Mon Mar 10 2008 - nonsea@users.sourceforge.net
- Bump to 0.7.11.
* Mon Mar 03 2008 - nonsea@users.sourceforge.net
- Bump to 0.7.10.
* Mon Feb 18 2008 - nonsea@users.sourceforge.net
- Bump to 0.7.9.
* Sun Jun 30 2007 - nonsea@users.sourceforge.net
- Bump to 0.7.7.
- Remove upstreamed patch void0-suncc-error
* Sun Jun 30 2007 - nonsea@users.sourceforge.net
- Bump to 0.7.6.
* Sun May 13 2007 - nonsea@users.sourceforge.net
- Bump to 0.7.5.
- Remove upstreamed patch define-FUNCTION.diff.
* Thu Mar 29 2007 nonsea@users.sourceforge.net
- Add patch define-FUNCTION.diff.
* Wed Mar 28 2007 - daymobrew@users.sourceforge.net
- Bump to 0.7.3.
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Initial spec
