#
# spec file for package libmms
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner:halton
# bugdb: http://bugs.launchpad.net/libmms/+bug/
#

Name:           libmms
Summary:        mms stream protocol library
Group:          Libraries/Multimedia
Version:        0.6
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:            http://sourceforge.net/projects/libmms/
License:      	LGPL
Source:         %{sf_download}/%{name}/%{name}-%{version}.tar.gz
# date:2008-09-02 owner:halton type:bug bugid:263864
Patch1:         %{name}-01-solaris-uint.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

%description
libmms is a library implementing the mms streaming protocol

%package devel
Summary: Libraries and includefiles for developing with libmms
Group:	 Development/Libraries

%description devel
This paackage provides the necessary development headers and libraries
to allow you to devel with libmms

%prep
%setup -q
%patch1 -p0

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

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-, root, root)
%doc AUTHORS COPYING.LIB ChangeLog NEWS README TODO README.LICENSE
%{_libdir}/libmms.so.*

%files devel
%{_includedir}/libmms/mms.h
%{_includedir}/libmms/bswap.h
%{_includedir}/libmms/mmsio.h
%{_includedir}/libmms/mmsh.h
%{_libdir}/libmms.so
%{_libdir}/pkgconfig/libmms.pc

%changelog
* Thu Jun 10 2010 - Albert Lee <trisk@opensolaris.org>
- Bump to 0.6
- Update URLs
* Tue Sep 02 2008 - halton.huo@sun.com
- Initial version
