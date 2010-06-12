#
# spec file for package gst-plugins-ugly
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%define gst_0_10_26 %(pkg-config --atleast-version=0.10.26 gstreamer-0.10 && echo 1 || echo 0)

Name:           gst-plugins-ugly
License:        GPL
%if %gst_0_10_26
Version:        0.10.15
%else
Version:        0.10.13
%endif
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
Group:          Libraries/Multimedia
Summary:        GStreamer Streaming-media framework plug-ins - restricted redistribution.
URL:            http://gstreamer.freedesktop.org/
Source:         http://gstreamer.freedesktop.org/src/gst-plugins-ugly/gst-plugins-ugly-%{version}.tar.bz2
Patch1:         gst-plugins-ugly-01-gettext.diff
Patch4:         gst-plugins-ugly-04-xsi_shell.diff
%if %gst_0_10_26
%else
Patch5:		gst-plugins-ugly-05-x264.diff
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
Docdir:         %{_defaultdocdir}/doc
Autoreqprov:    on
Prereq:         /sbin/ldconfig

%define 	majorminor	0.10

%description
GStreamer is a streaming-media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plug-ins.

%prep
%setup -n gst-plugins-ugly-%{version} -q
%patch1 -p1
%patch4 -p1
%if %gst_0_10_26
%else
%patch5 -p1
%endif

%build
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; \
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; \
FFLAGS="${FFLAGS:-%optflags}" ; export FFLAGS ; \
glib-gettextize -f
intltoolize --copy --force --automake
aclocal -I ./m4 -I ./common/m4 $ACLOCAL_FLAGS
autoheader
autoconf
automake -a -c -f
CONFIG_SHELL=/bin/bash \
bash ./configure \
  --prefix=%{_prefix}	\
  --sysconfdir=%{_sysconfdir} \
  --mandir=%{_mandir}   \
  %{gtk_doc_option}     \
%if %with_amrnb
%else
  --disable-amrnb \
%endif
%if %with_amrwb
%else
  --disable-amrwb \
%endif
  --disable-sidplay     \
  --disable-twolame     \
  --enable-external     \
  --disable-shave

# FIXME: hack: stop the build from looping
touch po/stamp-it

if [ "$SMP" != "" ]; then
  (make "MAKE=make -k -j $SMP"; exit 0)
  make 
else
  make
fi

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ]
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make DESTDIR=$RPM_BUILD_ROOT install
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

# Clean out files that should not be part of the rpm.
# This is the recommended way of dealing with it for RH8
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/*.a

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc AUTHORS COPYING README REQUIREMENTS
%{_libdir}/gstreamer-*/*.so
%{_sysconfdir}/gconf/schemas/gstreamer-*.schemas
%{_datadir}/locale/*/LC_MESSAGES/*.mo

%post 
%{_bindir}/gst-register > /dev/null 2> /dev/null
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="gstreamer-0.10.schemas"
for S in $SCHEMAS; do
 gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%package devel
Summary: 	GStreamer Plugin Library Headers.
Group: 		Development/Libraries
Requires: 	gstreamer-plugins-devel >= 0.10.0
Requires:       %{name} = %{version}

%description devel
GStreamer support libraries header files.

%files devel
%defattr(-, root, root)
%{_datadir}/gtk-doc

%changelog
* Thu Jun 10 2010 - Albert Lee <trisk@opensolaris.org>g
- Bump to 0.10.15, use 0.10.13 for older GStreamer
* Sun Dec 20 2009 - Milan Jurik
- upgrade to 0.10.13
* Wed Sep 02 2009 - Albert Lee <trisk@forkgnu.org>
- Add %gtk_doc_option
- Disable twolame
* Sun Jun 28 2009 - Milan Jurik
- upgrade to 0.10.12
- build cleanup, libtool shave disable (problematic shell script)
- amrnb as optional
- cdio and lame by default
* Fri Dec 12 2008 - trisk@acm.jhu.edu
- Bump to 0.10.10
- Disable more plugins
* Thu Sep 08 2008 - halton.huo@sun.com
- Bump to 0.10.9
* Wed Jul 23 2008 - trisk@acm.jhu.edu
- Add patch2 to use dvdnav
* Tue Jul 22 2008 - trisk@acm.jhu.edu
- Bump to 0.10.8
* Thu Oct 18 2007 - trisk@acm.jhu.edu
- Licence should be GPL
* Wed Oct 17 2007 - trisk@acm.jhu.edu
- Initial spec, based on gst-plugins-good
