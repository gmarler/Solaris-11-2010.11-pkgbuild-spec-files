#
# spec file for package gnome-build
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#

Name:		gnome-build
License:	GPL
Group:		Development/Libraries
Version:	2.24.1
Release:	1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:		http://www.gnome.org
Summary:	GNOME Build Framework.
Source:		http://download.gnome.org/sources/%{name}/2.24/%{name}-%{version}.tar.bz2
# date:2009-01-16 owner:halton type:bug bugzilla:567967
Patch1:         %{name}-01-suncc-empty-struct.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

Requires:	libglade >= 2.0.1
Requires:	gdl >= 0.7.0
BuildRequires:  gtk+-devel >= 2.3.0
BuildRequires:	libglade-devel >= 2.0.1
BuildRequires:	gdl-devel >= 0.7.0


%description
This is the GNOME Build Framework (GBF).

%package devel
Summary:	Libraries and include files for Gnome Build Framework.
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel 
Libraries and header files if you want to make use of the GNOME debug framework
in your own programs.


%prep
%setup -q
%patch1 -p1

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
intltoolize --force
aclocal $ACLOCAL_FLAGS -I .
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

make -j $CPU

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
%{_bindir}/*
%{_libdir}/lib*.so.*
%{_libdir}/gnome-build-1.0
%{_datadir}/pixmaps/*.png
%{_datadir}/gnome-build
%{_datadir}/locale

%files devel
%defattr (-, root, root)
%{_includedir}/gnome-build-1.0
%{_libdir}/*a
%{_libdir}/*so
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Jan 16 2009 - halton.huo@sun.com
- Bump to 2.24.1
- Add patch suncc-empty-struct.diff to fix bugzilla #567967
* Wed Aug 20 2008 - nonsea@users.sourceforge.net
- Bump to 2.23.90
* Tue Jan 03 2008 - nonsea@users.sourceforge.net
- Bump to 0.3.0
* Tue Apr 22 2008 - nonsea@users.sourceforge.net
- Bump to 0.2.4.
* Mon Mar 03 2008 - nonsea@users.sourceforge.net
- Bump to 0.2.3.
* Mon Feb 18 2008 - nonsea@users.sourceforge.net
- Bump to 0.2.2.
* Tue Oct 16 2007 - laca@sun.com
- use IT_PROG_INTLTOOL instead of AC_PROG_INTLTOOL in configure.in
* Mon Sep 10 2007 - nonsea@users.sourceforge.net
- Bump to 0.2.0
* Sun May 13 2007 - nonsea@users.sourceforge.net
- Bump to 0.1.7.
- Remove patch gnu-regex.diff since solaris's one works fine now.
* Sun May 13 2007 - nonsea@users.sourceforge.net
- Bump to 0.1.6.
- Remove upstreamed patch debug-define.diff.
* Sat Apr 21 2007 - dougs@truemail.co.th
- Disabled parallel make. Can be a problem on a multicpu system
* Thu Apr 05 2007 - nonsea@users.sourceforge.net
- Remove patch share-glue.diff, since this problem
  is resolved in anjuta.
* Wed Apr 04 2007 - nonsea@users.sourceforge.net
- Add patch share-glue.diff.
* Thu Mar 29 2007 - nonsea@users.sourceforge.net
- Add bug comments.
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Initial spec
