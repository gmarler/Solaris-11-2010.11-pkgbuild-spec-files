#
# spec file for package gst-plugins-bad
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
Name:           gst-plugins-bad
License:        GPL
Version:        0.10.18
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
Group:          Libraries/Multimedia
Summary:        GStreamer Streaming-media framework plug-ins - unstable.
URL:            http://gstreamer.freedesktop.org/
Source:         http://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-%{version}.tar.bz2
Patch1:         gst-plugins-bad-01-gettext.diff
Patch2:         gst-plugins-bad-02-gstapexraop.diff
Patch3:         gst-plugins-bad-03-xvidmain.diff
Patch4:         gst-plugins-bad-04-equal.diff
Patch5:         gst-plugins-bad-05-xsi_shell.diff
Patch6:         gst-plugins-bad-06-gstqt.diff
Patch7:         gst-plugins-bad-07-videomeasure.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
Docdir:         %{_defaultdocdir}/doc
Autoreqprov:    on

%define 	majorminor	0.10

%description
GStreamer is a streaming-media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plug-ins.

%prep
%setup -n gst-plugins-bad-%{version} -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

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
%if %with_amrwb
%else
  --disable-amrwb \
%endif
  --disable-bayer \
  --disable-dccp \
  --disable-festival \
  --disable-freeze \
  --disable-librfb \
  --disable-mve \
  --disable-nsf \
  --disable-nuvdemux \
  --disable-oss4 \
  --disable-pcapparse \
  --disable-rawparse \
  --disable-selector \
  --disable-subenc \
  --disable-scaletempo \
  --disable-speed \
  --disable-stereo \
  --disable-tta \
  --disable-videomeasure \
  --disable-vmnc \
  --disable-quicktime \
  --disable-vcd \
  --disable-alsa \
  --disable-assrender \
  --disable-cdaudio \
  --disable-celt \
  --disable-dc1394 \
  --disable-directfb \
  --disable-dirac \
  --disable-divx \
  --disable-metadata \
  --disable-faac \
  --disable-fbdev \
  --disable-gsm \
  --disable-ivorbis \
  --disable-jack \
  --disable-jp2k \
  --disable-ladspa \
  --disable-lv2 \
  --disable-libmms \
  --disable-mimic \
  --disable-mpeg2enc \
  --disable-mplex \
  --disable-musepack \
  --disable-mythtv \
  --disable-nas \
  --disable-neon \
  --disable-timidity \
  --disable-sdl \
  --disable-soundtouch \
  --disable-spc \
  --disable-gme \
  --disable-swfdec \
  --disable-dvb \
  --disable-oss4 \
  --disable-selector \
  %{gtk_doc_option}	\
  --enable-external \
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
* Fri Mar 12 2010 - Brian Cameron <brian.cameron@sun.com>
- Bump to 0.10.18.  Remove gst-plugins-bad-06-apexsink.diff and add
  gst-plugins-bad-gstqt.diff needed to build.
* Sun Dec 20 2009 - Milan Jurik
- upgrade to 0.10.17
- videosignal added
* Sat Oct 17 2009 - Milan Jurik
- upgrade to 0.10.14
* Wed Sep 02 2009 - Albert Lee <trisk@forkgnu.org>
- Disable assrender, kate, lv2, mimic, mjpegtools, rsvg, sdl, gme, theora
- Enable apexsink
- Remove soundcard.h
- Add patch6
* Sun Jun 28 2009 - Milan Jurik
- upgrade to 0.10.13
- build cleanup, libtool shave disable (problematic shell script)
- amrwb optional
- x264 by default
- oss4 and selector already in SUNW
* Thu May 21 2009 - brian.cameron@sun.com
- Bump to 0.10.12 and remove upstream patches.
* Tue Jan 20 2009 - brian.cameron@sun.com
- Bump to 0.10.10 and add patches needed to build.
* Thu Jan 08 2008 - brian.cameron@sun.com
- Add patch gst-plugins-bad-05-gstapexraop.diff to fix compile issue.
  Add patch gst-plugins-bad-06-ladspa.diff to fix crashing issue in plugin.
* Fri Dec 12 2008 - trisk@acm.jhu.edu
- Bump to 0.10.9.  
- Disable plugins for dependency consistency and to avoid unstable plugins
* Thu Sep 08 2008 - halton.huo@sun.com
- Bump to 0.10.8
- Add patch byte-order.diff to fix build issue
- Remove disable options to let configure check runtime 
  (please tell me if this is not right)
* Thu Aug 07 2008 - trisk@acm.jhu.edu
- Re-enable faad, theora
* Tue Jul 22 2008 - trisk@acm.jhu.edu
- Bump to 0.10.7
* Thu Oct 18 2007 - trisk@acm.jhu.edu
- Licence should be GPL
* Wed Oct 17 2007 - trisk@acm.jhu.edu
- Initial spec, based on gst-plugins-good
