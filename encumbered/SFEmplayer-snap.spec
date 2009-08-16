#
# spec file for package SFEmplayer
#
# includes module(s): mplayer
#
%include Solaris.inc

%define with_faad %(pkginfo -q SFEfaad && echo 1 || echo 0)
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

%define ver %(date '+%Y%m%d')

%define SFElibsndfile   %(/usr/bin/pkginfo -q SFElibsndfile && echo 1 || echo 0)

Name:                    SFEmplayer
Summary:                 mplayer - The Movie Player
Version:                 1.0.3.%ver
URL:                     http://www.mplayerhq.hu/
Source:                  http://www.mplayerhq.hu/MPlayer/releases/mplayer-export-snapshot.tar.bz2
Patch1:                  mplayer-snap-01-shell.diff
Patch2:                  mplayer-snap-02-aserror.diff
Patch3:                  mplayer-snap-03-ldflags.diff
Patch4:                  mplayer-snap-04-realplayer.diff
Source3:                 http://www.mplayerhq.hu/MPlayer/skins/Blue-1.7.tar.bz2
Source4:                 http://www.mplayerhq.hu/MPlayer/skins/Abyss-1.7.tar.bz2
Source5:                 http://www.mplayerhq.hu/MPlayer/skins/neutron-1.5.tar.bz2
Source6:                 http://www.mplayerhq.hu/MPlayer/skins/proton-1.2.tar.bz2
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
BuildRequires: SFElibcdio-devel

%if %SFElibsndfile
BuildRequires: SFElibsndfile-devel
Requires: SFElibsndfile
%else
BuildRequires:	SUNWlibsndfile
Requires:	SUNWlibsndfile
%endif

Requires: SFElame
BuildRequires: SFElame-devel
Requires: SFEtwolame
BuildRequires: SFEtwolame-devel
Requires: SUNWgawk
Requires: SFEfaad2
BuildRequires: SFEfaad2-devel
Requires: SFElibmpcdec
BuildRequires: SFElibmpcdec-devel
Requires: SFElibfribidi
BuildRequires: SFElibfribidi-devel
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

%define x11	/usr/openwin
%ifarch i386 amd64
%define x11	/usr/X11
%endif

%prep
rm -rf %name-build
mkdir -p %name-build
cd %name-build
bzcat %SOURCE | tar xf -
mv mplayer-export-* mplayer-export
cd mplayer-export
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0

%build
cd %name-build/mplayer-export
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%if %debug_build
dbgflag=--enable-debug
export CFLAGS="-g -D__hidden=\"\""
%else
dbgflag=--disable-debug
export CFLAGS="-O2 -D__hidden=\"\""
%endif

export LDFLAGS="-L%{x11}/lib -L/usr/gnu/lib -R/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib -liconv" 
export CC=gcc

bash ./configure				\
	    --prefix=%{_prefix}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --confdir=%{_sysconfdir}		\
            --enable-gui			\
            --enable-menu			\
            --extra-cflags=" -I/usr/lib/live/liveMedia/include -I/usr/lib/live/groupsock/include -I/usr/lib/live/UsageEnvironment/include -I/usr/lib/live/BasicUsageEnvironment/include -I%{x11}/include -I/usr/sfw/include" \
            --extra-ldflags="-L/usr/lib/live/liveMedia -R/usr/lib/live/liveMedia -L/usr/lib/live/groupsock -R/usr/lib/live/groupsock -L/usr/lib/live/UsageEnvironment -R/usr/lib/live/UsageEnvironment -L/usr/lib/live/BasicUsageEnvironment -R/usr/lib/live/BasicUsageEnvironment -L%{x11}/lib -R%{x11}/lib -L/usr/gnu/lib -R/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib" \
            --extra-libs='-lBasicUsageEnvironment -lUsageEnvironment -lgroupsock -lliveMedia -lstdc++ -liconv' \
            --codecsdir=%{_libdir}/mplayer/codecs \
%if %with_faad
            --enable-faad-external		\
%endif
            --enable-live			\
            --enable-network			\
	    --enable-rpath			\
            --enable-largefiles			\
	    --enable-crash-debug		\
            --enable-dynamic-plugins            \
	    $dbgflag

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
cd %name-build/mplayer-export
gmake install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_libdir}/mplayer/codecs
mkdir -p $RPM_BUILD_ROOT%{_datadir}/mplayer/skins
(
	cd $RPM_BUILD_ROOT%{_datadir}/mplayer/skins
	gtar fxj %SOURCE3
	gtar fxj %SOURCE4
	gtar fxj %SOURCE5
	gtar fxj %SOURCE6
	ln -s Blue default
)
ln -s /usr/openwin/lib/X11/fonts/TrueType/FreeSerif.ttf $RPM_BUILD_ROOT%{_datadir}/mplayer/subfont.ttf
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

rm -rf $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%{_datadir}/mplayer
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%changelog
* Sun Aug 16 2009 - Milan Jurik
- GNU grep not needed
* Sat Jul 18 2009 - Milan Jurik
- improved handling of tarball
* Sat Jul 11 2009 - Milan Jurik
- Initial version
