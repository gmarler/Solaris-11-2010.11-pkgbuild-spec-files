#
# spec file for package SFEgst-plugins-bad
#
# includes module(s): gst-plugins-bad
#
%include Solaris.inc

Name:                    SFEgst-plugins-bad
Summary:                 GStreamer bad plugins
Version:                 0.10.9
URL:                     http://gstreamer.freedesktop.org/
Source:                  http://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-%{version}.tar.bz2
Patch1:                  gst-plugins-bad-01-gettext.diff
Patch5:                  gst-plugins-bad-05-gstapexraop.diff
Patch6:                  gst-plugins-bad-06-ladspa.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%define gst_minmaj %(echo %{version} | cut -f1,2 -d.)

BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-media-devel
Requires: SUNWgnome-libs
Requires: SUNWgnome-media

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%prep
%setup -n gst-plugins-bad-%{version} -q
%patch1 -p1
%patch5 -p1
%patch6 -p1

%build
export CFLAGS="%optflags -I/usr/sfw/include -DANSICPP"
export RPM_OPT_FLAGS="$CFLAGS"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export PERL5LIB=%{_prefix}/perl5/site_perl/5.6.1/sun4-solaris-64int
export LDFLAGS="%_ldflags"

glib-gettextize -f
aclocal -I ./m4 -I ./common/m4 $ACLOCAL_FLAGS
libtoolize --copy --force
intltoolize --copy --force --automake
autoheader
autoconf

# Do not build the selector plugin since it is now included in 
# SUNWgnome-media.
#
automake -a -c -f
./configure \
  --prefix=%{_prefix}   \
  --sysconfdir=%{_sysconfdir} \
  --mandir=%{_mandir}   \
  %{gtk_doc_option}     \
  --disable-selector \
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
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/gstreamer-%{gst_minmaj}/gst
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%if %{!?_without_gtk_doc:1}%{?_without_gtk_doc:0}
%{_datadir}/gtk-doc
%endif

%changelog
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
