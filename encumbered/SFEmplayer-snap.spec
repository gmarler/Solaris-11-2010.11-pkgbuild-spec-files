#
# spec file for package SFEmplayer
#
# includes module(s): mplayer
#

# NOTE:	Make sure that the first gcc found in your path is version 4.3.3
#	or later.  gcc-3 can build this, but MPlayer complains that the
#	compiler is too old when it is run.  gcc-4.5.1 is recommended.

# NOTE: To make man display the man page correctly, use
#	export PAGER="/usr/bin/less -insR"

# If you want to build the gui, use
#   pkgtool --with-gui build <specfile>
# Please note that the MPlayer download page says the included gui is
# no longer developed and there is limited bug fixing for it.
# SMPlayer is recommended instead as a front end.

# To build using the daily MPlayer Subversion snapshot, use
# --with-daily-snap.  But that will almost certainly require you
# to rework some patches.

# Default is to use fixed tarball revision from Arch Linux
%define with_constant_tarball %{?_with_daily_snap:0}%{?!_with_daily_snap:1}

# Default is to build without the gui "gmplayer"; if you want a modern gui,
# then consider building SFEsmplayer as well
%define build_gui %{?_with_gui:1}%{?!_with_gui:0}

%include Solaris.inc
%define cc_is_gcc 1 

%define with_faad %(pkginfo -q SFEfaad2 && echo 1 || echo 0)
%define with_fribidi %(pkginfo -q SFElibfribidi && echo 1 || echo 0)
%define with_ladspa %(pkginfo -q SFEladspa && echo 1 || echo 0)
%define with_openal %(pkginfo -q SFEopenal && echo 1 || echo 0)
%define with_mad %(pkginfo -q SFElibmad && echo 1 || echo 0)
%define with_liba52 %(pkginfo -q SFEliba52 && echo 1 || echo 0)
%define with_lame %(pkginfo -q SFElame && echo 1 || echo 0)
%define with_twolame %(pkginfo -q SFEtwolame && echo 1 || echo 0)
%define with_mpcdec %(pkginfo -q SFElibmpcdec && echo 1 || echo 0)
%define with_xvid %(pkginfo -q SFExvid && echo 1 || echo 0)
%define with_x264 %(pkginfo -q SFElibx264 && echo 1 || echo 0)
%define with_openjpeg %(pkginfo -q SFEopenjpeg && echo 1 || echo 0)
%define with_giflib %(pkginfo -q SFEgiflib && echo 1 || echo 0)

%if %with_constant_tarball
%define revision 32792
#else
%define ver %(date '+%Y%m%d')
%endif

%define SFElibsndfile   %(/usr/bin/pkginfo -q SFElibsndfile && echo 1 || echo 0)

Name:                    SFEmplayer
Summary:                 mplayer - The Movie Player
Version:                 1.0.3.%ver
URL:                     http://www.mplayerhq.hu/
%if %with_constant_tarball
Source7:		 ftp://ftp.archlinux.org/other/mplayer/mplayer-%revision.tar.xz
%else
Source:                  http://www.mplayerhq.hu/MPlayer/releases/mplayer-export-snapshot.tar.bz2
%endif
Patch1:                  mplayer-snap-01-shell.diff
Patch2:                  mplayer-snap-02-aserror.diff
Patch3:                  mplayer-snap-03-ldflags.diff
Patch4:                  mplayer-snap-04-realplayer.diff
Patch5:                  mplayer-snap-05-cpudetect.diff
#Patch6:                  mplayer-snap-06-mkstemp.diff
%if %build_gui
Source3:                 http://www.mplayerhq.hu/MPlayer/skins/Blue-1.7.tar.bz2
Source4:                 http://www.mplayerhq.hu/MPlayer/skins/Abyss-1.7.tar.bz2
Source5:                 http://www.mplayerhq.hu/MPlayer/skins/neutron-1.5.tar.bz2
Source6:                 http://www.mplayerhq.hu/MPlayer/skins/proton-1.2.tar.bz2
%endif
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-build

%include default-depend.inc
Requires: SUNWsmbau
Requires: SUNWgnome-audio
BuildRequires: SUNWgnome-audio-devel
Requires: SUNWxorg-clientlibs
Requires: SUNWfontconfig
Requires: SUNWfreetype2
Requires: SUNWspeex
Requires: SUNWjpg
Requires: SUNWpng
Requires: SUNWogg-vorbis
Requires: SUNWlibtheora
Requires: SUNWgccruntime
Requires: SUNWgnome-base-libs
Requires: SUNWsmbau
Requires: SFEliveMedia
Requires: SFElibcdio
%ifarch i386 amd64
BuildRequires: SFEyasm
%endif
BuildRequires: SFElibcdio-devel
BuildRequires: SUNWgroff
BuildRequires: SUNWesu
%if %with_constant_tarball
BuildRequires: SFExz
%endif

%if %SFElibsndfile
BuildRequires: SFElibsndfile-devel
Requires: SFElibsndfile
%else
BuildRequires:	SUNWlibsndfile
Requires:	SUNWlibsndfile
%endif

Requires: SFElame
BuildRequires: SFElame-devel
%if %with_twolame
Requires: SFEtwolame
BuildRequires: SFEtwolame-devel
%endif
Requires: SUNWgawk
Requires: SFEfaad2
BuildRequires: SFEfaad2-devel
Requires: SFElibmpcdec
BuildRequires: SFElibmpcdec-devel
%if %with_fribidi
Requires: SFElibfribidi
BuildRequires: SFElibfribidi-devel
%endif
Requires: SFEladspa
BuildRequires: SFEladspa-devel
Requires: SFElibmad
BuildRequires: SFElibmad-devel
Requires: SFEliba52
BuildRequires: SFEliba52-devel
%if %with_openal
Requires: SFEopenal
BuildRequires: SFEopenal-devel
%endif
%if %with_xvid
Requires: SFExvid
BuildRequires: SFExvid-devel
%endif
%if %with_x264
Requires: SFElibx264
BuildRequires: SFElibx264-devel
%endif
%if %with_openjpeg
Requires: SFEopenjpeg
BuildRequires: SFEopenjpeg-devel
%endif
%if %with_giflib
Requires: SFEgiflib
BuildRequires: SFEgiflib-devel
%endif

%define x11	/usr/openwin
%ifarch i386 amd64
%define x11	/usr/X11
%endif

%prep
rm -rf %name-build
mkdir -p %name-build
cd %name-build
%if %with_constant_tarball
xzcat %SOURCE7 | tar xf -
%define builddir mplayer
%else
bzcat %SOURCE | tar xf -
%define builddir mplayer-export
mv mplayer-export-* mplayer-export
%endif
cd %builddir
%patch1 -p0
%patch2 -p0
%patch3 -p1
%patch4 -p1
%patch5 -p1
#%patch6 -p1

%build
cd %name-build/%builddir
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%if %debug_build
dbgflag=--enable-debug
export CFLAGS="-g -D__hidden=\"\""
%else
dbgflag=--disable-debug
export CFLAGS="-O2 -fomit-frame-pointer -D__hidden=\"\""
%endif

export LDFLAGS="-L%{x11}/lib -L/usr/gnu/lib -R/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib -liconv" 
export CC=gcc

bash ./configure				\
	    --prefix=%{_prefix}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --confdir=%{_sysconfdir}		\
%if %build_gui
            --enable-gui			\
%endif
            --enable-menu			\
            --extra-cflags=" -I/usr/lib/live/liveMedia/include -I/usr/lib/live/groupsock/include -I/usr/lib/live/UsageEnvironment/include -I/usr/lib/live/BasicUsageEnvironment/include -I%{x11}/include -I/usr/sfw/include" \
            --extra-ldflags="-L/usr/lib/live/liveMedia -R/usr/lib/live/liveMedia -L/usr/lib/live/groupsock -R/usr/lib/live/groupsock -L/usr/lib/live/UsageEnvironment -R/usr/lib/live/UsageEnvironment -L/usr/lib/live/BasicUsageEnvironment -R/usr/lib/live/BasicUsageEnvironment -L%{x11}/lib -R%{x11}/lib -L/usr/gnu/lib -R/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib" \
            --extra-libs='-lBasicUsageEnvironment -lUsageEnvironment -lgroupsock -lliveMedia -lstdc++ -liconv' \
            --codecsdir=%{_libdir}/mplayer/codecs \
%if %with_faad
            --enable-faad		\
%endif
            --enable-live			\
	    --enable-rpath			\
            --enable-largefiles			\
	    --enable-crash-debug		\
            --enable-dynamic-plugins            \
	    $dbgflag

gmake -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
cd %name-build/%builddir
gmake install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%_libdir/mplayer/codecs
%if %build_gui
mkdir -p $RPM_BUILD_ROOT%{_datadir}/mplayer/skins
(
	cd $RPM_BUILD_ROOT%{_datadir}/mplayer/skins
	gtar fxj %SOURCE3
	gtar fxj %SOURCE4
	gtar fxj %SOURCE5
	gtar fxj %SOURCE6
	ln -s Blue default
)
%else
mkdir $RPM_BUILD_ROOT%_datadir/mplayer
%endif
ln -s /usr/openwin/lib/X11/fonts/TrueType/FreeSerif.ttf \
      $RPM_BUILD_ROOT%_datadir/mplayer/subfont.ttf

# nroff does not understand macros used by mplayer man page
# See http://www.mplayerhq.hu/DOCS/tech/manpage.txt
mkdir $RPM_BUILD_ROOT%_datadir/man/cat1
cd $RPM_BUILD_ROOT%_datadir/man/cat1
groff -mman -Tutf8 -rLL=78n ../man1/mplayer.1 | col -bxp > mplayer.1
ln -s mplayer.1 mencoder.1
cd -

rm -f $RPM_BUILD_ROOT%_libdir/lib*a

rm -rf $RPM_BUILD_ROOT%_sysconfdir

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%_bindir/*
%_libdir/*
%dir %attr (0755, root, sys) %_datadir
%_mandir/man1
%_mandir/cat1
%_datadir/mplayer/subfont.ttf
%if %build_gui
%{_datadir}/mplayer/skins
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%endif

%changelog
* Tue Jan 18 2011 - Alex Viskovatoff
- Update to new tarball, with Patch6 no longer required
- Replace --without-gui option with --with-gui, disabling gui by default
* Fri Nov  5 2010 - Alex Viskovatoff
- Use fixed (constant) tarball from Arch Linux repository by default
- Remove obsolete configure switch --enable-network
- Restore cpu detection patch by Milan Jurik
- Add Patch6 by Thomas Wagner to make mkstemp get used
- Add --without-gui option: the configure default is to disable the gui,
  and the MPlayer download page effectively deprecates the included gui
- Create a formatted man page, since nroff cannot handle the man page
* Wed Aug 18 2010 - Thomas Wagner
- rename configure switch --enable-faad-external to --enable-faad   
- use gmake in %build instead make (might have solved makefile syntax error)
* Fri May 21 2010 - Milan Jurik
- openjpeg and giflib support
* Thu Aug 20 2009 - Milan Jurik
- -fomit-frame-pointer to workaround Solaris GCC bug on Nehalem
* Sun Aug 16 2009 - Milan Jurik
- GNU grep not needed
* Sat Jul 18 2009 - Milan Jurik
- improved handling of tarball
* Sat Jul 11 2009 - Milan Jurik
- Initial version
