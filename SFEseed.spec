#
# spec file for package seed
#
# Copyright (c) 2010 Sun Microsystems, Inc.
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc
%include default-depend.inc

Summary:	JavaScript interpreter
Name:		seed
Version:	2.30.0
Release:	1
License:	LGPL v3
Group:		Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/seed/2.30/%{name}-%{version}.tar.bz2
Patch0:		seed-01-wall.diff
Patch1:		seed-02-gettext.diff
Patch2:		seed-03-util.diff
Patch3:         seed-04-seed.diff

URL:		http://live.gnome.org/Seed
Distribution:	Java Desktop System
Vendor:		Gnome Community


BuildRequires: SUNWdbus
BuildRequires: SFEgnome-js-common
BuildRequires: SFEgjs
BuildRequires: SUNWgtk2
BuildRequires: SFEwebkitgtk
BuildRequires: SFEmpfr
BuildRequires:	SUNWsqlite3-devel


BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%description
Seed is a library and interpreter, dynamically bridging (through
GObjectIntrospection) the WebKit JavaScriptCore engine, with the GNOME
platform. Seed serves as something which enables you to write
standalone applications in JavaScript, or easily enable your
application to be extensible in JavaScript.


%package devel
Summary:	Header files for seed library
Group:		Development/Libraries

Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel
Requires:	gobject-introspection-devel
Requires:	gtk-webkit-devel


%description devel
Header files for seed library.

%package apidocs
Summary:	seed library API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
API documentation for seed library.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

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


intltoolize --copy --force --automake
libtoolize --force
aclocal 
autoheader
automake -a -c -f
autoconf

./configure --prefix=%{_prefix}			\
	    --sysconfdir=%{_sysconfdir}		\
	    --libexecdir=%{_libexecdir}		\
	    --localstatedir=%{_localstatedir}   \
	    --mandir=%{_mandir}			\
	    --disable-silent-rules              \	
	    --enable-mpfr-module=no

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_docdir}/seed{,-%{version}}
find $RPM_BUILD_ROOT -name "*.a" -o -name "*.la" -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/seed
%attr(755,root,root) %{_libdir}/libseed.so.*
%attr(755,root,root) %{_libdir}/libseed.so
%dir %{_libdir}/seed
%attr(755,root,root) %{_libdir}/seed/libseed_cairo.so
%attr(755,root,root) %{_libdir}/seed/libseed_canvas.so
%attr(755,root,root) %{_libdir}/seed/libseed_dbusnative.so
%attr(755,root,root) %{_libdir}/seed/libseed_example.so
%attr(755,root,root) %{_libdir}/seed/libseed_ffi.so
%attr(755,root,root) %{_libdir}/seed/libseed_gettext.so
%attr(755,root,root) %{_libdir}/seed/libseed_gtkbuilder.so
%attr(755,root,root) %{_libdir}/seed/libseed_libxml.so
%attr(755,root,root) %{_libdir}/seed/libseed_multiprocessing.so
%attr(755,root,root) %{_libdir}/seed/libseed_os.so
%attr(755,root,root) %{_libdir}/seed/libseed_readline.so
%attr(755,root,root) %{_libdir}/seed/libseed_sandbox.so
%attr(755,root,root) %{_libdir}/seed/libseed_sqlite.so
%{_datadir}/doc/seed
%{_datadir}/seed
%{_datadir}/gtk-doc
%{_mandir}/man1/seed.1*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*


%changelog
* Tue Sep 08 2010 - yuntong.jin@sun.com
- Init spec
