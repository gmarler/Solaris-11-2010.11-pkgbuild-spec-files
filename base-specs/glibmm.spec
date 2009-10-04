#
# spec file for package glibmm
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:                    glibmm
License:        	 LGPL
Group:                   System/Libraries
Version:                 2.21.3
Release:                 1
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
Summary:                 glibmm - C++ Wrapper for the Glib2 Library
URL:                     http://www.gtkmm.org/
Source:                  http://ftp.gnome.org/pub/GNOME/sources/glibmm/2.21/%{name}-%{version}.tar.bz2
Patch1:                  glibmm-01-m4-macro.diff
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:           libsigc++-devel >= 2.0.0
BuildRequires:           glib2-devel >= 2.9.0

%package devel
Summary:                 Headers for developing programs that will use %{name}.
Group:                   System/Libraries
Requires:                libsigc++-devel >= 1.2.0
Requires:                glib2-devel >= 2.9.0

%prep
%setup -q -n glibmm-%version
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

aclocal $ACLOCAL_FLAGS -Iscripts
autoconf
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_cxx_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir} --disable-python
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

cp examples/child_watch/.libs/child_watch $RPM_BUILD_ROOT%{_datadir}/doc/glibmm-2.4/examples/child_watch/child_watch
cp examples/iochannel_stream/.libs/example $RPM_BUILD_ROOT%{_datadir}/doc/glibmm-2.4/examples/iochannel_stream/example
cp examples/markup/.libs/parser $RPM_BUILD_ROOT%{_datadir}/doc/glibmm-2.4/examples/markup/parser
cp examples/markup/test.xml $RPM_BUILD_ROOT%{_datadir}/doc/glibmm-2.4/examples/markup/test.xml
cp examples/options/.libs/example $RPM_BUILD_ROOT%{_datadir}/doc/glibmm-2.4/examples/options/example
cp examples/regex/.libs/example $RPM_BUILD_ROOT%{_datadir}/doc/glibmm-2.4/examples/regex/example
cp examples/thread/.libs/dispatcher $RPM_BUILD_ROOT%{_datadir}/doc/glibmm-2.4/examples/thread/dispatcher
cp examples/thread/.libs/dispatcher2 $RPM_BUILD_ROOT%{_datadir}/doc/glibmm-2.4/examples/thread/dispatcher2
cp examples/thread/.libs/thread $RPM_BUILD_ROOT%{_datadir}/doc/glibmm-2.4/examples/thread/thread
cp examples/thread/.libs/threadpool $RPM_BUILD_ROOT%{_datadir}/doc/glibmm-2.4/examples/thread/threadpool

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Sep 25 2009 - jchoi42@pha.jhu.edu
- Bump to 2.21.3
* Mon Mar 31 2008 - damien.carbery@sun.com
- Bump to 2.16.1.
* Tue Mar 11 2008 - damien.carbery@sun.com
- Bump to 2.16.0. Remove upstream patch 03-overloading-ambiguity.
* Wed Mar  5 2008 - simon.zheng@sun.com
- To fix failure of building with SS11 compiler, add patch
  04-overloading-ambiguity. Add an explicit template specification
  to avoid ction to avoid ambiguity. Fix is from glibmm maintainer
  murrayc@murrayc.com, and also go upstream.
  available on next tarball.
* Tue Mar  4 2008 - damien.carbery@sun.com
- Bump to 2.15.8.
* Tue Feb 26 2008 - damien.carbery@sun.com
- Bump to 2.15.7.
* Mon Feb 25 2008 - damien.carbery@sun.com
- Bump to 2.15.6.
* Mon Feb 18 2008 - damien.carbery@sun.com
- Add patch 02-m4-macro to build on sparc. The GNU m4 check was failing because
  '[Mm]' in the aclocal code was losing the brackets when aclocal/autoconf
  created the configure script.
* Wed Feb 15 2008 - simon.zheng@sun.com
- Correct download URL.
* Tue Feb 14 2008 - simon.zheng@sun.com
- Bump to Version 2.15.5.
- Add glibmm-01-build.diff.
- Remove glimm-01-gtestutils.diff.
* Thu Feb 14 2008 - damien.carbery@sun.com
- Add patch 01-gtestutils to include glib/gtestutils.h in some source files to
  define g_assert macro.
* Tue Feb 12 2008 - ghee.teo@sun.com
- Added all the examples to the /usr/share/doc.
  Also cleaned out %files and %files-devel where are not used here.
* Mon Jan 28 2008 - simon.zheng@sun.com
- Create. Split from SFEglibmm and bump to version 2.14.2.
