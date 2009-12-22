#
# spec file for package SFEgst-plugins-bad
#
# includes module(s): gst-plugins-bad
#
%include Solaris.inc

Name:                    SFEgst-plugins-bad
Summary:                 GStreamer bad plugins
Version:                 0.10.17
URL:                     http://gstreamer.freedesktop.org/
Source:                  http://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-%{version}.tar.bz2
Patch1:                  gst-plugins-bad-01-gettext.diff
Patch2:                  gst-plugins-bad-02-gstapexraop.diff
Patch3:                  gst-plugins-bad-03-xvidmain.diff
Patch4:                  gst-plugins-bad-04-equal.diff
Patch5:                  gst-plugins-bad-05-xsi_shell.diff
Patch6:                  gst-plugins-bad-06-apexsink.diff
Patch7:                  gst-plugins-bad-07-videomeasure.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%define gst_minmaj %(echo %{version} | cut -f1,2 -d.)

BuildRequires: SUNWcairo-devel
BuildRequires: SUNWgtk2-devel
BuildRequires: SUNWgnome-media-devel
BuildRequires: SUNWlibexif-devel
BuildRequires: SUNWlibglade-devel
BuildRequires: SUNWliboil-devel
BuildRequires: SUNWlibtheora-devel
Requires: SUNWcairo
Requires: SUNWgtk2
Requires: SUNWgnome-media
Requires: SUNWlibexif
Requires: SUNWlibglade
Requires: SUNWliboil
Requires: SUNWlibtheora

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%prep
%setup -n gst-plugins-bad-%{version} -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
# There seems to be an issue with the version of libtool that GStreamer is
# now using.  The libtool script uses the echo and RM variables but does not
# define them, so setting them here addresses this.
export echo="/usr/bin/echo"
export RM="/usr/bin/rm"

export CFLAGS="%optflags -I%{sfw_inc} -DANSICPP"
# gstmodplug needs C99 __func__
export CXXFLAGS="%cxx_optflags -features=extensions -I%{sfw_inc}"
export HAVE_CXX=yes
export RPM_OPT_FLAGS="$CFLAGS"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export PERL5LIB=%{_prefix}/perl5/site_perl/5.6.1/sun4-solaris-64int
export LDFLAGS="%_ldflags %{sfw_lib_path}"

glib-gettextize -f
aclocal -I ./m4 -I ./common/m4 $ACLOCAL_FLAGS
libtoolize --copy --force
intltoolize --copy --force --automake
autoheader
automake -a -c -f
autoconf

# Do not build the selector and OSSv4 plugins since they are now included in 
# SUNWgnome-media.
#
automake -a -c -f
./configure \
  --prefix=%{_prefix}   \
  --sysconfdir=%{_sysconfdir} \
  --mandir=%{_mandir}   \
  %{gtk_doc_option}     \
  --disable-selector \
  --disable-oss4 \
  --enable-external --with-check=no

# FIXME: hack: stop the build from looping
touch po/stamp-it

if [ "$SMP" != "" ]; then
  (make "MAKE=make -k -j $SMP"; exit 0)
  make
else
  make
fi

%install
# There seems to be an issue with the version of libtool that GStreamer is
# now using.  The libtool script uses the echo and RM variables but does not
# define them, so setting them here addresses this.
export echo="/usr/bin/echo"
export RM="/usr/bin/rm"

[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ]
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make DESTDIR=$RPM_BUILD_ROOT install
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

# Clean out files that should not be part of the rpm.
# This is the recommended way of dealing with it for RH8
rm $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{gst_minmaj}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{gst_minmaj}/*.a

%if %{!?_without_gtk_doc:0}%{?_without_gtk_doc:1}
rm -rf $RPM_BUILD_ROOT%{_datadir}/gtk-doc
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/gstreamer-%{gst_minmaj}/gst
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%dir %attr (0755, root, other) %{_datadir}/gstreamer-0.10
%{_datadir}/gstreamer-0.10/*
%if %{!?_without_gtk_doc:1}%{?_without_gtk_doc:0}
%{_datadir}/gtk-doc
%endif

%changelog
* Tue Dec 22 2009 - Brian.Cameron@sun.com
- Bump to 0.10.17.
* Thu May 21 2009 - Brian.Cameron@sun.com
- Bump to 0.10.12.  Remove upstream patches.
* Mon Jan 19 2009 - Brian.Cameron@sun.com
- Bump to 0.10.10.  Add patches gst-plugins-bad-03-dccp.diff,
  gst-plugins-bad-04-makefile.diff, and gst-plugins-bad-05-deinterlace.diff to
  address compile issues.  Rework older patches.  Now build plugins which use
  C++, such as modplug.
* Thu Jan 15 2009 - Brian.Cameron@sun.com
- Disable building the selector plugin since we build this with
  SUNWgnome-media.
* Thu Jan 08 2009 - Brian.Cameron@sun.com
- Bump to 0.10.9.  Add patch
  gst-plugins-bad-05-gstapexraop.diff to fix compile issue.
  Add patch gst-plugins-bad-06-ladspa.diff to fix crashing
  issue in plugin.
* Thu Jul 31 2008 - Brian.Cameron@sun.com
- Bump to 0.10.8.
* Thu Apr 24 2008 - Brian.Cameron@sun.com
- Created with version 0.10.7
