#
# spec file for package libsyncml
#
# includes module(s): libsyncml
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jerryyu
# bugdb: http://libsyncml.opensync.org/ticket/
#

Name:           libsyncml
Version:        0.5.0
Release:        1
License:        LGPL 2.1 or higher
Group:          Development/Libraries
Distribution:   Java Desktop System
Vendor:	        Sun Microsystems, Inc.
Summary:        C library implementation of the SyncML protocol
URL:            http://libsyncml.opensync.org
Source:         http://libsyncml.opensync.org/download/releases/%{version}/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
Requires:       wbxml2 libsoup >= 2.2.91 
BuildRequires:  wbxml2-devel libsoup-devel >= 2.2.91 

%description
C library implementation of the SyncML protocol

%package devel
Summary:        Header files, libraries and development documentation for %{name}
Group:	        Development/Libraries
Requires:       %{name} = %{version}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

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

mkdir build && cd build
%if %debug_build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_BUILD_TYPE=Debug ..
%else
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr ..
%endif

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
cd build
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/syncml-http-server
%{_bindir}/syncml-obex-client
%{_libdir}/libsyncml.la
%{_libdir}/libsyncml.so
%{_libdir}/libsyncml.so.0
%{_libdir}/libsyncml.so.0.0.0

%files devel
%defattr(-,root,root)
%{_includedir}/libsyncml-1.0/libsyncml/http_client.h
%{_includedir}/libsyncml-1.0/libsyncml/http_server.h
%{_includedir}/libsyncml-1.0/libsyncml/obex_client.h
%{_includedir}/libsyncml-1.0/libsyncml/sml_auth.h
%{_includedir}/libsyncml-1.0/libsyncml/sml_base64.h
%{_includedir}/libsyncml-1.0/libsyncml/sml_command.h
%{_includedir}/libsyncml-1.0/libsyncml/sml_defines.h
%{_includedir}/libsyncml-1.0/libsyncml/sml_devinf.h
%{_includedir}/libsyncml-1.0/libsyncml/sml_ds_server.h
%{_includedir}/libsyncml-1.0/libsyncml/sml_elements.h
%{_includedir}/libsyncml-1.0/libsyncml/sml_error.h
%{_includedir}/libsyncml-1.0/libsyncml/sml_md5.h
%{_includedir}/libsyncml-1.0/libsyncml/sml_notification.h
%{_includedir}/libsyncml-1.0/libsyncml/sml_parse.h
%{_includedir}/libsyncml-1.0/libsyncml/sml_session.h
%{_includedir}/libsyncml-1.0/libsyncml/sml_transport.h
%{_includedir}/libsyncml-1.0/libsyncml/syncml.h
%{_includedir}/libsyncml-1.0/libsyncml/obex_server.h
%{_includedir}/libsyncml-1.0/libsyncml/sml_devinf_obj.h
%{_includedir}/libsyncml-1.0/libsyncml/sml_manager.h
%{_libdir}/pkgconfig/libsyncml-1.0.pc


%changelog
* Thu Jan 08 2009 - halton.huo@sun.com
- Bump to 0.5.0
- Remove upstreamed patch fail-null.diff
* Thu Sep 04 2008 - halton.huo@sun.com
- Bump to 0.4.7.
- Remove upstreamed patch: void-func-return.diff, TCSBRKP.diff
  strcasestr.diff
- Add patch fail-null.diff to fix bug #161
* Fri Mar 07 2008 - nonsea@users.sourceforge.net
- Bump to 0.4.6.
- Use cmake to build
- Remove upstreamed patch printf-null.diff
- Add patch void-func-return.diff, TCSBRKP.diff and strcasestr.diff
* Wed Oct 17 2007 - nonsea@users.sourceforge.net
- Bump to 0.4.5.
- Remove upstreamed patch 01-Makefile.diff, 02-define-func.diff
  03-fail-null.diff and 04-cfmakeraw.diff, reorder.
- Rework patch 01-printf-null.diff
* Fri Sep 21 2007 - jijun.yu@sun.com
- add patch5.
* Tue Apr  3 2007 - laca@sun.com
- add patch cfmakeraw.diff to fix build of the openobex module on Solaris
- enable the openobex module
* Fri Mar 30 2007 - daymobrew@users.sourceforge.net
- Bump to 0.4.4. Add patch 03-fail-null to add 'NULL' to empty 'fail()' calls.
* Thu Jan 11 2007 - jijun.yu@sun.com
- Initial version
