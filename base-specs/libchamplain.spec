#
# spec file for package libchamplain
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%define owner jouby
#

Name:		libchamplain
License:	GPL
Group:		Development/Libraries
Version:	0.4.3
Release:	1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:		http://projects.gnome.org/libchamplain/
Summary:	a Clutter based widget to display rich, eye-candy and interactive maps
Source:		http://download.gnome.org/sources/%{name}/0.4/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

Requires: 	clutter >= 1.0
Requires: 	glib >= 2.10
Requires: 	cairo >= 1.4
Requires: 	gio >= 2.16
Requires: 	gdk >= 2.14
Requires: 	sqlite >= 3.0
Requires: 	gtk >= 2.12
Requires: 	clutter-gtk >= 0.10
BuildRequires:	cairo-devel >= 1.4
BuildRequires:	clutter-cairo-devel >= 0.8
BuildRequires:	clutter-devel >= 0.8.4
BuildRequires:	clutter-gtk-devel >= 0.8
BuildRequires:	clutter-devel >= 1.0.0
BuildRequires:	clutter-gtk-devel >= 0.10
BuildRequires:	gir-repository-devel
BuildRequires:	glib2-devel >= 2.16
BuildRequires:	gobject-introspection-devel

%description
libchamplain is a Clutter based widget to display rich, eye-candy and
interactive maps.

%package devel
Summary:	Libraries and include files for libchamplain.
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Libraries and header files if you want to make use of the libchamplain library in your
own programs.


%prep
%setup -q

#FIXME: When #590829 fixed in next release, remove following lines 
rm -f m4/lt~obsolete.m4
rm -f m4/ltoptions.m4
rm -f m4/libtool.m4
rm -f m4/ltsugar.m4
rm -f m4/ltversion.m4

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
aclocal $ACLOCAL_FLAGS -I m4
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
%{_prefix}/share/gir-*

%files devel
%defattr (-, root, root)
%{_prefix}/include/liblibchamplain-*
%{_prefix}/lib/lib*.a
%{_prefix}/lib/lib*.la
%{_prefix}/lib/lib*.so
%{_prefix}/lib/pkgconfig/*

%changelog
* Wed Oct 28 2009 - brian.cameron@sun.com
- Bump to 0.4.2.
* Fri Sep 18 2009 - halton.huo@sun.com
- Bump to 0.4.0.
- Remove upstreamed patch clutter-1-0.diff for bugzilla #590825
- Add patch libtool.diff to fix bugzilla #595534.
* Wed Aug 05 2009 - halton.huo@sun.com
- Initial spec.
