#
# spec file for package clutter-gtk-0-10
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: bewitche
#

Name:         clutter-gtk-0-10
Summary:      clutter-gtk - GTK+ integration library for clutter
Version:      0.10.2
Release:      1
License:      GPL
Group:        System/Libraries
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Source:	  http://www.clutter-project.org/sources/clutter-gtk/0.10/clutter-gtk-%{version}.tar.bz2
# Patch taken from here:
# http://bugzilla.o-hand.com/show_bug.cgi?id=1490
URL:          http://www.clutter-project.org/
BuildRoot:               %{_tmppath}/%{name}-%{version}-build


%prep
%setup -q -n clutter-gtk-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
./configure --prefix=%{_prefix}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --disable-static
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Remove gtk docs since they are installed with the 0.8 package.
rm -fR $RPM_BUILD_ROOT%{_datadir}/gtk-doc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*


%changelog
* Mon Aug 03 2009 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.10.2.
* Tue Jul 07 2009 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.9.2.  Remove upstream patch clutter-gtk9-01-introspection.diff.
* Tue May 12 2009 - Brian Cameron  <brian.cameron@sun.com>
- Created.


