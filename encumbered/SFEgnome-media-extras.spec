#
# spec file for packages SUNWgnome-media-extras
#
# includes module(s): gst-ffmpeg, gst-plugins-ugly, gst-plugins-bad
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: trisk
#
%include Solaris.inc

%define with_hal %(pkginfo -q SUNWhal && echo 1 || echo 0)
%define SFElibsndfile   %(/usr/bin/pkginfo -q SFElibsndfile && echo 1 || echo 0)
%define with_amrnb %(pkginfo -q SFEamrnb && echo 1 || echo 0)
%define with_amrwb %(pkginfo -q SFEamrwb && echo 1 || echo 0)
%define SFEsdl      %(/usr/bin/pkginfo -q SFEsdl && echo 1 || echo 0)
%define NVDAgraphics %(/usr/bin/pkginfo -q NVDAgraphics && echo 1 || echo 0)

%use gst_ffmpeg = gst-ffmpeg.spec
%use gst_plugins_ugly = gst-plugins-ugly.spec
%use gst_plugins_bad = gst-plugins-bad.spec

%define gst_minmaj %(echo %{gst_plugins_ugly.version} | cut -f1,2 -d.)

Name:                    SFEgnome-media-extras
Summary:                 GNOME streaming media framework - extra plugins
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

Requires: SUNWlibms
Requires: SUNWlxml
Requires: SUNWzlib
Requires: SUNWfreetype2
BuildRequires: SUNWbison
BuildRequires: SUNWPython
BuildRequires: SUNWPython-extra
BuildRequires: SUNWgtk-doc
BuildRequires: SUNWgnome-xml-share 
Requires: SUNWgnome-libs
BuildRequires: SUNWgnome-libs-devel
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
Requires: SUNWgnome-media
BuildRequires: SUNWgnome-media-devel
Requires: SUNWliboil
BuildRequires: SUNWliboil-devel
Requires: SUNWgnome-audio
BuildRequires: SUNWgnome-audio-devel
Requires: SUNWgnome-config
BuildRequires: SUNWgnome-config-devel
Requires: SUNWgnome-vfs
BuildRequires: SUNWgnome-vfs-devel
##### for gst-ffmpeg #####
BuildRequires: SUNWbzip
Requires: SUNWbzip
Requires: SFEffmpeg
BuildRequires: SFEffmpeg-devel
##### for gst-plugins-ugly #####
Requires: SFEliba52
BuildRequires: SFEliba52-devel
Requires: SFElibcdio
BuildRequires: SFElibcdio-devel
Requires: SFElibdvdread
BuildRequires: SFElibdvdread-devel
Requires: SFElibdvdnav
BuildRequires: SFElibdvdnav-devel
Requires: SFElibid3tag
BuildRequires: SFElibid3tag-devel
Requires: SFElame
BuildRequires: SFElame-devel
Requires: SFElibmad
BuildRequires: SFElibmad-devel
Requires: SFElibmpeg2
BuildRequires: SFElibmpeg2-devel
Requires: SFElibx264
BuildRequires: SFElibx264-devel
##### for gst-plugins-bad #####
%if %SFElibsndfile
BuildRequires: SFElibsndfile-devel
Requires: SFElibsndfile
%else
BuildRequires:	SUNWlibsndfile
Requires:	SUNWlibsndfile
%endif
# Notes: metadata plugin which uses libexif may be unstable
#Requires: SUNWlibexif
#BuildRequires: SUNWlibexif-devel
Requires: SUNWmusicbrainz
BuildRequires: SUNWmusicbrainz-devel
#Requires: SUNWlibrsvg
#BuildRequires: SUNWlibrsvg-devel
Requires: SUNWxorg-clientlibs
BuildRequires: SUNWxorg-clientlibs
%if %SFEsdl
Requires: SFEsdl
BuildRequires: SFEsdl-devel
%else
Requires: SUNWlibsdl
BuildRequires:  SUNWlibsdl-devel
%endif
%if %NVDAgraphics
# VDPAU
BuildRequires: NVDAgraphics
%endif
#Requires: SUNWlibtheora
#BuildRequires: SUNWlibtheora-devel
#BuildRequires: SFEdirac-devel
Requires: SUNWopensslr
BuildRequires: SUNWopenssl-include
Requires: SFEfaad2
BuildRequires: SFEfaad2-devel
# Note: musepack plugin doesn't compile with Studio
#BuildRequires: SFElibmpcdec-devel
Requires: SFElibmms
BuildRequires: SFElibmms-devel
Requires: SFElibofa
Requires: SFEwildmidi
BuildRequires: SFEwildmidi-devel
Requires: SFExvid
BuildRequires: SFExvid-devel
Requires: SFEladspa
BuildRequires: SFEladspa-devel
Requires: SFEsoundtouch
BuildRequires: SFEsoundtouch-devel
Requires: SFElibschroedinger
BuildRequires: SFElibschroedinger-devel

%ifarch sparc
%define arch_opt --enable-mlib
BuildRequires: SUNWmlib
Requires: SUNWmlib
%else
%define arch_opt --disable-mlib --disable-mmx --disable-mmx2
%endif
%if %with_hal
Requires: SUNWhal
%endif
%if %with_amrnb
Requires: SFEamrnb
BuildRequires: SFEamrnb-devel
%endif
%if %with_amrwb
Requires: SFEamrwb
BuildRequires: SFEamrwb-devel
%endif

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SUNWpostrun-root
Requires: SUNWgnome-config

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version
%gst_ffmpeg.prep -d %name-%version
%gst_plugins_ugly.prep -d %name-%version
%gst_plugins_bad.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
# There seems to be an issue with the version of libtool that GStreamer is
# now using.  The libtool script uses the echo and RM variables but does not
# define them, so setting them here addresses this.
export echo="/usr/bin/echo"
export RM="/usr/bin/rm -f"

# Note that including  __STDC_VERSION n CFLAGS for gnome-media breaks the S9
# build for gstreamer,  gst-plugins, and gnome-media, so not including for them.
#

export CFLAGS="%optflags -I%{xorg_inc} -I%{sfw_inc} -DANSICPP"
# gstmodplug needs C99 __func__
export CXXFLAGS="%cxx_optflags -features=extensions -I%{sfw_inc}"
# AC_CHECK_PROG fails if $CXX is not in $PATH
export HAVE_CXX=yes
# double dollar sign for make, extra backslash for libtool
export LDFLAGS="%_ldflags -R'%{_libdir}/\\\$\$ISALIST' %{xorg_lib_path} %{sfw_lib_path}"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export PERL5LIB=%{_prefix}/perl5/site_perl/5.6.1/sun4-solaris-64int
%gst_ffmpeg.build -d %name-%version
%gst_plugins_ugly.build -d %name-%version
%gst_plugins_bad.build -d %name-%version

%install
# There seems to be an issue with the version of libtool that GStreamer is
# now using.  The libtool script uses the echo and RM variables but does not
# define them, so setting them here addresses this.
export echo="/usr/bin/echo"
export RM="/usr/bin/rm -f"

rm -rf $RPM_BUILD_ROOT

%gst_ffmpeg.install -d %name-%version
%gst_plugins_ugly.install -d %name-%version
%gst_plugins_bad.install -d %name-%version

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{gst_minmaj}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{gst_minmaj}/*.a
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc

# remove files that conflict with SUNWgnome-media
rm -rf $RPM_BUILD_ROOT%{_bindir}
rm -rf $RPM_BUILD_ROOT%{_mandir}

%if %{!?_without_gtk_doc:0}%{?_without_gtk_doc:1}
rm -rf $RPM_BUILD_ROOT%{_datadir}/gtk-doc
%endif

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libgst*.so*
%{_libdir}/gstreamer-%{gst_minmaj}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gstreamer-*
%{_datadir}/gstreamer-*/presets/*
%{_datadir}/gstreamer-*/camera-apps/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/gstreamer-%{gst_minmaj}/gst
%if %{!?_without_gtk_doc:1}%{?_without_gtk_doc:0}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc
%endif

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Thu Jun 10 2010 Albert Lee <trisk@opensolaris.org>
- Use %{_libdir}/$ISALIST to select optimised dependencies
- Use libmms
- Fix C++ compilation
* Sat Apr 24 2010 Milan Jurik
- enable SDL plugin, ladspa, soundtouch and libschroedinger
* Sat Oct 17 2009 Milan Jurik
- update for the latest bad plugins
* Fri Sep 18 2009 Milan Jurik
- SUNWgtk-doc and SUNWgnome-xml as build dependencies
* Wed Sep 02 2009 Albert Lee <trisk@forkgnu.org>
- Remove SUNWtheora dependency
- Add SUNWopensslr and SUNWopenssl-include dependencies for apexsink.
- Sync with SFEgst-plugins-bad.
* Sun Jun 28 2009 - Milan Jurik
- amrwb and amrwb as optional
- x264 and cdio and lame enabled
* Tue Feb 17 2009 - Thomas Wagner
- make (Build-)Requires conditional SUNWlibsndfile|SFElibsndfile(-devel)
* Fri Dec 12 2008 - trisk@acm.jhu.edu
- Bump gst-plugins-ugly to 0.10.10
- Bump gst-plugins-bad to 0.10.9
- Update dependencies again
* Thu Sep 02 2008 - halton.huo@sun.com
- Update dependencies
* Wed Jul 23 2008 - trisk@acm.jhu.edu
- Update dependencies
* Thu Apr 24 2008 - trisk@acm.jhu.edu
- Add gst-ffmpeg
* Thu Nov 22 2007 - daymobrew@users.sourceforge.net
- Change SUNWneon dependency to SFEneon.
* Wed Oct 17 2007 - trisk@acm.jhu.edu
- Initial spec, based on SUNWgnome-media
