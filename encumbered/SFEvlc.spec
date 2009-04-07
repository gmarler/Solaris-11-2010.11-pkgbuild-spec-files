#
# spec file for package SFEvlc
#
# includes module(s): vlc
#
%include Solaris.inc

%define SUNWlibsdl      %(/usr/bin/pkginfo -q SUNWlibsdl && echo 1 || echo 0)

%define	src_name	vlc
%define	src_url		http://download.videolan.org/pub/videolan/vlc

Name:                   SFEvlc
Summary:                vlc - the cross-platform media player and streaming server
Version:                0.8.6c
Source:                 %{src_url}/%{version}/%{src_name}-%{version}.tar.bz2
Patch1:                 vlc-01-configure-no-pipe.diff
Patch2:                 vlc-02-solaris.diff
Patch3:                 vlc-03-oss.diff
Patch4:                 vlc-04-solaris_specific.diff
Patch5:                 vlc-05-solaris-cmds.diff
Patch6:                 vlc-06-intl.diff
Patch7:			vlc-07-live.diff
Patch8:			vlc-08-osdmenu_path.diff
Patch9:			vlc-09-pic-mmx.diff
Patch10:		vlc-10-real_codecs_path.diff
Patch11:		vlc-11-libpostproc.diff
SUNW_BaseDir:           %{_basedir}
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%if %SUNWlibsdl
BuildRequires:  SUNWlibsdl-devel
Requires:       SUNWlibsdl
%else
BuildRequires:  SFEsdl-devel
Requires:       SFEsdl
%endif
BuildRequires:  SFEsdl-image-devel
Requires:       SFEsdl-image
Requires:       SUNWhal
BuildRequires:  SUNWdbus-devel
Requires:       SUNWdbus
Requires:       SUNWxorg-clientlibs
BuildRequires:  SUNWsmbau
BuildRequires:  SFElibfribidi-devel
Requires:       SFElibfribidi
#BuildRequires:  SFEfreetype-devel
Requires:       SUNWfreetype2
BuildRequires:  SFEliba52-devel
Requires:       SFEliba52
BuildRequires:  SFEffmpeg-devel
Requires:       SFEffmpeg
BuildRequires:  SFElibmad-devel
Requires:       SFElibmad
BuildRequires:  SFElibmpcdec-devel
Requires:       SFElibmpcdec
BuildRequires:  SFElibmatroska-devel
Requires:       SFElibmatroska
BuildRequires:  SUNWogg-vorbis-devel
Requires:       SUNWogg-vorbis
BuildRequires:  SFElibdvbpsi-devel
Requires:       SFElibdvbpsi
BuildRequires:  SFElibdvdnav-devel
Requires:       SFElibdvdnav
BuildRequires:  SFElibdts-devel
BuildRequires:  SFElibcddb-devel
Requires:       SFElibcddb
BuildRequires:  SFElibmpeg2-devel
Requires:       SFElibmpeg2
BuildRequires:  SFElibupnp-devel
Requires:       SFElibupnp
BuildRequires:  SFEvcdimager-devel
Requires:       SFEvcdimager
BuildRequires:  SFElibx264-devel
Requires:       SFElibx264
BuildRequires:  SFElibtar-devel
Requires:       SFElibtar

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%prep
%setup -q -n vlc-%version
#%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
# ffmpeg is build with g++, therefore we need to build with g++

%if %build_l10n
nlsopt=-enable-nls
%else
nlsopt=-disable-nls
%endif

X11LIB="-L/usr/X11/lib -R/usr/X11/lib"
GNULIB="-L/usr/gnu/lib -R/usr/gnu/lib"

export PATH=/usr/gnu/bin:$PATH
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CC=gcc
export CXX=g++
export CPPFLAGS="-D_XOPEN_SOURCE=500 -D__EXTENSIONS__ -I/usr/X11/include -I/usr/gnu/include -I/usr/include/libavcodec -I./include"
%if %debug_build
export CFLAGS="-g"
%else
export CFLAGS="-O4"
%endif
export LDFLAGS="$X11LIB $GNULIB"

ln -s /usr/include/libavcodec include/ffmpeg
rm ./configure
./bootstrap
./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}		\
            --sysconfdir=%{_sysconfdir}		\
	    --enable-shared			\
	    --disable-rpath			\
	    --enable-mkv			\
	    --enable-live555			\
	    --enable-ffmpeg			\
	    --enable-xvid			\
	    --enable-real			\
	    --enable-realrtsp			\
%if %debug_build
	    --enable-debug=yes			\
%endif
	    --disable-static			\
	    $nlsopt

# Disable libmpeg2 to get past configure.

%if %build_l10n
printf '%%%s/\/intl\/libintl.a/-lintl/\nwq\n' | ex - vlc-config
%endif

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
#rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -f $RPM_BUILD_ROOT%{_libdir}/charset.alias
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps
cp $RPM_BUILD_ROOT%{_datadir}/vlc/vlc48x48.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/vlc.png
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps
cp $RPM_BUILD_ROOT%{_datadir}/vlc/vlc32x32.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/vlc.png
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps
cp $RPM_BUILD_ROOT%{_datadir}/vlc/vlc16x16.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps/vlc.png

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( touch %{_datadir}/icons/hicolor || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then 
        %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%postun
test -x $BASEDIR/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS
( touch %{_datadir}/icons/hicolor  || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
        %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/vlc
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/vlc
%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16/apps
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32/apps
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/16x16/apps/*.png
%{_datadir}/icons/hicolor/32x32/apps/*.png
%{_datadir}/icons/hicolor/48x48/apps/*.png

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.a

%changelog
* April 2009 - Gilles Dauphin
- postprocess.h is in libpostproc
- TODO upgrade vlc, that's a nightmare
* Thu Dec 02 2008 - dauphin@enst.fr
- try to use the actual SFE ffmpeg , probleme in new ffmpeg API
- I just resign now, but... later i will retry
- TODO link to libpostproc: s/postproc/libpostproc/ .
* Thu Aug 07 2008 - trisk@acm.jhu.edu
- Rename SFElibdvdread dependency to SFElibdvdnav
* Fri Aug  3 2007 - dougs@truemail.co.th
- Added devel and l10n
- Added options to better find codecs
- Added icons for app
* Tue Jul 31 2007 - dougs@truemail.co.th
- added --disable-rpath option
- added SFElibx264 to the requirements
* Sun Jul 15 2007 - dougs@truemail.co.th
- --with-debug enables --enable-debug, added some dependencies
* Sat Jul 14 2007 - dougs@truemail.co.th
- Build with gcc
* Fri Mar 23 2007 - daymobrew@users.sourceforge.net
- Add two patches, 01-configure-no-pipe and 02-solaris. Add multiple
  dependencies. Getting closer but not quite building yet.
  Patch 01-configure-no-pipe removes the '-pipe' test. It causes problems later
  with -DSYS_SOLARIS being added after -pipe and being rejected by the linker.
  Patch 02-solaris.diff fixes two compiler issues. First involves expansion of
  ?: code; second changes AF_LOCAL to AF_UNIX as the former is not defined in
  <sys/socket.h>.

* Thu Mar 22 2007 - daymobrew@users.sourceforge.net
- Initial version
