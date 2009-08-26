#
# spec file for package SFEvlc
#
# includes module(s): vlc
#

# NOTE EXPERIMENTAL - does contain a few null pointer uses, so you might want to  " LD_PRELOAD=/usr/lib/0@0.so.1 vlc  "
# NOTE EXPERIMENTAL - does not link correctly - volunteers please let's get into contact and collaborate
# NOTE EXPERIMENTAL - uses SFEqt45 which is build by: pkgtool build experimental/SFEqt45-gcc.spec (no autodeps for experimental!)
#                     make SFEqt45 *before* vlc, manually
# NOTE EXPERIMENTAL - patches for experimental are (non-svn-)copied to the new name %-1.0.1 if they are modified from the older revisions
# NOTE EXPERIMENTAL - patches from old revision sometimes success with line offsets, need reworking

# tickets
#
# Ticket #3034 (closed defect: fixed) https://trac.videolan.org/vlc/ticket/3034
#    confusing delayed Interface initialization failed message
#    Fixed by 1861697 


#  Ticket #3036 (reopened patch) https://trac.videolan.org/vlc/ticket/3036
#    vlc-config calls /bin/sh but uses bash-isms

#  Ticket #3033 (new defect) https://trac.videolan.org/vlc/ticket/3033
#    lazy use of NULL pointers causes segfaults on Solaris

#  Ticket #3039 (new defect) https://trac.videolan.org/vlc/ticket/3039
#    no MMX symbols on Solaris 10?


# ticket worked around here in he spec-file (see tickets related to patches below in the patch section)
#  Ticket #3035 (closed defect: fixed) https://trac.videolan.org/vlc/ticket/3035
#    Solaris needs explicit -lsocket
#    Fixed by d17b37c 


%include Solaris.inc

%define cc_is_gcc 1
%define _gpp /usr/gnu/bin/g++
%if %arch_sse2
#######%define arch_opt --cpu=i686 --enable-mmx --enable-mmx2
%include x86_sse2.inc
%endif
 
%include base.inc

%define SUNWlibsdl      %(/usr/bin/pkginfo -q SUNWlibsdl && echo 1 || echo 0)

%define	src_name	vlc
%define	src_url		http://download.videolan.org/pub/videolan/vlc

Name:                   SFEvlc
Summary:                vlc - the cross-platform media player and streaming server
Version:                1.0.1
Source:                 %{src_url}/%{version}/%{src_name}-%{version}.tar.bz2
#Patch1:                 vlc-01-configure-no-pipe.diff
#obsoleted by ticket #3027 Solaris does not have AF_LOCAL - define AF_LOCAL as AF_UNIX
#Patch2:                 vlc-02-solaris.diff-1.0.1
Patch3:                 vlc-03-oss.diff-1.0.1
Patch4:                 vlc-04-solaris_specific.diff
Patch5:                 vlc-05-solaris-cmds.diff-1.0.1
Patch6:                 vlc-06-intl.diff-1.0.1
Patch7:                        vlc-07-live.diff-1.0.1
Patch8:                        vlc-08-osdmenu_path.diff-1.0.1
#pausiert ##TODO## ##FIXME## Patch9:                   vlc-09-pic-mmx.diff
Patch10:               vlc-10-real_codecs_path.diff-1.0.1
Patch12:               vlc-12-for-int-loop.diff-1.0.1
#Patch13:               vlc-13-x264-git-20090404.diff
#https://trac.videolan.org/vlc/ticket/3028
#Fixed by [23414d6]
Patch14:               vlc-14-modules-access-file.c-disable_have_fstatfs.diff
Patch16:               vlc-16-modules.c-file_offset_bits_ticket_3031.diff
#seems only relevant to older SunOS releases (5.10, eventuall older builds of 5.11)
##TODO## need rework to test for already existing dirfd else define 
#Patch17:               vlc-17-dirfd-missing-ticket-3029-Fixed-by-c438250.diff
Patch18:               vlc-18-empty-struct.diff-1.0.1





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
Requires:  SFElibdts
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

##TODO## using gcc compiled qt 4.5.x from experimental/SFEqt45-gcc.s- must "pkgtool build" manually before, no autodeps available for specs in experimental/*
BuildRequires:	SFEqt45-devel
Requires:	SFEqt45

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
#obsolete ticket 3027 - %patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
#%patch9 -p1
%patch10 -p1
%patch12 -p1
%patch14 -p1
%patch16 -p1
%patch18 -p1
#seems only relevant to older SunOS releases (5.10, eventuall older builds of 5.11)
##TODO## need rework to test for already existing dirfd else define 
#%patch17 -p1

perl -w -pi.bak -e "s,#\!\s*/bin/sh,#\!/usr/bin/bash," `find . -type f -exec grep -q "#\!.*/bin/sh" {} \; -print | egrep -v "/libtool"`

##TODO## experimental
# text references
#perl -w -pi.bakztext -e "s, -z def,," libtool

#especially for configure.in ....
perl -w -pi.bak2 -e "s,hostname -s,hostname," configure*

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

##evil!!! export PATH=/usr/gnu/bin:$PATH
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal -I ./m4"
export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++
#export CXXFLAGS="%cxx_optflags"
#export CFLAGS="%optflags -D_XOPEN_SOURCE=500 -D__C99FEATURES__ -D__EXTENSIONS__"
#export CPPFLAGS="-D_XOPEN_SOURCE=500 -D__C99FEATURES__ -D__EXTENSIONS__ -I/usr/X11/include -I/usr/gnu/include -I/usr/include/libavcodec -I./include"
#
#notes to flags:
# Ticket #3040 (closed defect: fixed) https://trac.videolan.org/vlc/ticket/3040
# need to define _XPG4_2 on Solaris
#
export CXXFLAGS="%cxx_optflags -D_XPG4_2 -D__C99FEATURES__ -D__EXTENSIONS__ -L/lib -R/lib"
export CFLAGS="%optflags -D_XPG4_2 -D__C99FEATURES__ -D__EXTENSIONS__ -L/lib -R/lib"
export CPPFLAGS="-I/usr/X11/include -I/usr/gnu/include -I/usr/include/libavcodec -I./include -D_XPG4_2 -D__C99FEATURES__ -D__EXTENSIONS__"

%if %debug_build
export CFLAGS="$CFLAGS -g"
%else
export CFLAGS="$CFLAGS -O4"
%endif
##TODO## experime
#export LD=/usr/gnu/bin/ld
#export LDFLAGS="%_ldflags $X11LIB $GNULIB"
##TODO## experime
export LDFLAGS="%_ldflags $X11LIB $GNULIB -lsocket -lxnet"
#export LDFLAGS="         $X11LIB $GNULIB -lsocket -lxnet"


export CONFIG_SHELL=/usr/bin/bash

ln -s /usr/include/libavcodec include/ffmpeg
#rm ./configure
#./bootstrap
perl -w -pi.bak3 -e "s,#\!\s*/bin/sh,#\!/usr/bin/bash," configure
./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}		\
            --sysconfdir=%{_sysconfdir}		\
	    --enable-shared			\
	    --disable-static			\
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
--disable-mmx \
	    $nlsopt

#           --with-gnu-ld                       \

# Disable mmx temporarily (video_*) does not compile 
# Disable libmpeg2 to get past configure.

%if %build_l10n
printf '%%%s/\/intl\/libintl.a/-lintl/\nwq\n' | ex - vlc-config
%endif

# spatializer fails to compile, disable for now
#  Ticket #3037 (reopened defect) https://trac.videolan.org/vlc/ticket/3037
#  spatializer does not compile on Solaris
perl -w -pi.bakspatializer -e "s, spatializer , ," vlc-config
##TODO## experime
#perl -w -pi.bak420 -e "s, (i420_rgb_mmx|i420_ymga|i420_ymga_mmx|i420_yuy2|i420_yuy2_mmx|i422_i420|i422_yuy2|i422_yuy2_mmx|yuy2_i420|yuy2_i422) ,," vlc-config

#/bin/false

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
#rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
find $RPM_BUILD_ROOT%{_libdir}/ -name '*.la' -exec rm {} \;
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
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/vlc*
%{_libdir}/libvlc*
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
#%dir %attr (0755, root, bin) %{_libdir}
#%{_libdir}/lib*.a
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Aug 26 2009 - Gilles dauphin
- add patch , avoid empty struct for SS12
* Fri Aug 14 2009 - Thomas Wagner
- copy to encumbered/SFEvlc-1.0.1-experimental.spec
- remove patch11 libprostproc detection is upstream
- rework some patches for vlc-1.0.1
- still does not link correctly with sun and gnu linker - volunteers welcome, please get in contact
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
