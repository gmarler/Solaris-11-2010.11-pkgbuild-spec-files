#
# spec file for packages SUNWgnome-media-extras
#
# includes module(s): gst-ffmpeg, gst-plugins-ugly, gst-plugins-bad
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: trisk
#
%include Solaris.inc

%define with_hal %(pkginfo -q SUNWhal && echo 1 || echo 0)
%define SFElibsndfile   %(/usr/bin/pkginfo -q SFElibsndfile && echo 1 || echo 0)

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

%if %SFElibsndfile
BuildRequires: SFElibsndfile-devel
Requires: SFElibsndfile
%else
BuildRequires:	SUNWlibsndfile
Requires:	SUNWlibsndfile
%endif

Requires: SUNWgnome-vfs
Requires: SUNWlibms
Requires: SUNWlxml
Requires: SUNWxorg-clientlibs
Requires: SUNWzlib
Requires: SUNWfreetype2
BuildRequires: SUNWbison
BuildRequires: SUNWPython
BuildRequires: SUNWPython-extra
BuildRequires: SUNWbzip
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
Requires: SFEffmpeg
BuildRequires: SFEffmpeg-devel
##### for gst-plugins-ugly #####
Requires: SFEliba52
BuildRequires: SFEliba52-devel
#Requires: SFElibcdio
#BuildRequires: SFElibcdio-devel
Requires: SFElibdvdnav
BuildRequires: SFElibdvdnav-devel
Requires: SFElibid3tag
BuildRequires: SFElibid3tag-devel
Requires: SFElibmad
BuildRequires: SFElibmad-devel
Requires: SFElibmpeg2
BuildRequires: SFElibmpeg2-devel
##### for gst-plugins-bad #####
# Notes: metadata plugin which uses libexif may be unstable
#Requires: SUNWlibexif
#BuildRequires: SUNWlibexif-devel
Requires: SUNWmusicbrainz
BuildRequires: SUNWmusicbrainz-devel
Requires: SUNWlibsdl
BuildRequires:  SUNWlibsdl-devel
Requires: SUNWlibtheora
BuildRequires: SUNWlibtheora-devel
# Note: amrnb code is non-distributable, so don't depend on it
#Requires: SFEamrnb
#BuildRequires: SFEamrnb-devel
#BuildRequires: SFEdirac-devel
Requires: SFEfaad2
BuildRequires: SFEfaad2-devel
# Note: musepack plugin doesn't compile with Studio
#BuildRequires: SFElibmpcdec-devel
#Requires: SFElibmms
#BuildRequires: SFElibmms-devel
Requires: SFElibofa
Requires: SFEwildmidi
BuildRequires: SFEwildmidi-devel
Requires: SFExvid
BuildRequires: SFExvid-devel

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
# Note that including  __STDC_VERSION n CFLAGS for gnome-media breaks the S9
# build for gstreamer,  gst-plugins, and gnome-media, so not including for them.
#

export CFLAGS="%optflags -I%{xorg_inc} -I%{sfw_inc} -DANSICPP"
# gstmodplug needs C99 __func__
export CXXFLAGS="%cxx_optflags -features=extensions -I%{sfw_inc}"
export LDFLAGS="%_ldflags %{xorg_lib_path} %{sfw_lib_path}"
%gst_ffmpeg.build -d %name-%version
%gst_plugins_ugly.build -d %name-%version
%gst_plugins_bad.build -d %name-%version

%install
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
