#
# spec file for package gvfs
#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: gheet
#
Name:         gvfs
License:      LGPL
Group:        System/Libraries/GNOME
Version:      1.5.1
Release:      4
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Virtual File System Library for GNOME
Source:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/1.5/%{name}-%{version}.tar.bz2
URL:          http://www.gnome.org/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on

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
CFLAGS="$RPM_OPT_FLAGS -DDBUS_API_SUBJECT_TO_CHANGE=1"	\
./configure --prefix=%{_prefix}		\
            --sysconfdir=%{_sysconfdir} \
            --libexecdir=%{_libexecdir} \
            %{gtk_doc_option}
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install

%clean 
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Feb 12 2010 - jchoi42@pha.jhu.edu
- bump to 1.5.1
* Sat Nov 17 2007 - daymobrew@users.sourceforge.net
- Bump to 0.0.2. Remove upstream patches, 01-solaris and 02-solaris2.
* Fri Nov 09 2007 - daymobrew@users.sourceforge.net
- Add patch 02-solaris2 to include header files to fix 'implicit function
  declaration' warnings.

* Wed Nov 07 2007 - daymobrew@users.sourceforge.net
- Initial version.
