#
# spec file for package SFEmplayer
#
# includes module(s): mplayer
#

# want this? compile with: pkgtool --with-gcc4 build <specfile>
%define use_gcc4 %{?_with_gcc4:1}%{?!_with_gcc4:0}

%include Solaris.inc

%define cc_is_gcc 1
%if %use_gcc4
%define _gpp /usr/gnu/bin/g++
%else
%define _gpp /usr/sfw/bin/g++
%endif
%include base.inc


%define with_fribidi %(pkginfo -q SFElibfribidi && echo 1 || echo 0)
%define with_ladspa %(pkginfo -q SFEladspa && echo 1 || echo 0)
%define with_openal %(pkginfo -q SFEopenal && echo 1 || echo 0)
%define with_mad %(pkginfo -q SFElibmad && echo 1 || echo 0)
%define with_lame %(pkginfo -q SFElame && echo 1 || echo 0)
%define with_twolame %(pkginfo -q SFEtwolame && echo 1 || echo 0)
%define with_mpcdec %(pkginfo -q SFElibmpcdec && echo 1 || echo 0)
%define with_xvid %(pkginfo -q SFExvid && echo 1 || echo 0)
%define with_x264 %(pkginfo -q SFElibx264 && echo 1 || echo 0)
%define with_giflib %(pkginfo -q SFEgiflib && echo 1 || echo 0)
%define with_schroedinger %(pkginfo -q SFElibschroedinger && echo 1 || echo 0)

%define SFElibsndfile   %(/usr/bin/pkginfo -q SFElibsndfile && echo 1 || echo 0)

Name:		SFEmplayer
Summary:	mplayer - The Movie Player
Version:	1.0.0.0.3
%define tarball_version 1.0rc3
URL:		http://www.mplayerhq.hu/
Source:		http://www.mplayerhq.hu/MPlayer/releases/MPlayer-%{tarball_version}.tar.bz2
Source3:	http://www.mplayerhq.hu/MPlayer/skins/Blue-1.7.tar.bz2
Source4:	http://www.mplayerhq.hu/MPlayer/skins/Abyss-1.7.tar.bz2
Source5:	http://www.mplayerhq.hu/MPlayer/skins/neutron-1.5.tar.bz2
Source6:	http://www.mplayerhq.hu/MPlayer/skins/proton-1.2.tar.bz2
Patch1:		mplayer-01-cddb.diff
Patch4:		mplayer-04-cabac-asm.diff
Patch11:	mplayer-11-cpudetect.diff
Patch12:	mplayer-12-realplayer.diff
Patch30:	mplayer-30-configure.diff
Patch31:	mplayer-31-rdynamic.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{tarball_version}-build

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
%if %use_gcc4
BuildRequires: SFEgcc
Requires: SFEgccruntime
#also required for libs still compiled with gcc3?
Requires: SUNWgccruntime
%else
BuildRequires: SUNWgcc
Requires: SUNWgccruntime
%endif
Requires: SUNWgnome-base-libs
BuildRequires: SUNWxwrtl
Requires: SUNWxwrtl
BuildRequires: SUNWxorg-mesa
Requires: SUNWxorg-mesa
BuildRequires: SUNWaalib
Requires: SUNWaalib
BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl
BuildRequires: SUNWlibm
Requires: SUNWlibm
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
Requires: SFElibmpcdec
BuildRequires: SFElibmpcdec-devel
Requires: SFElibfribidi
BuildRequires: SFElibfribidi-devel
Requires: SFEladspa
BuildRequires: SFEladspa-devel
Requires: SFElibmad
BuildRequires: SFElibmad-devel
%if %with_openal
Requires: SFEopenal
BuildRequires: SFEopenal-devel
%endif
%if %with_xvid
Requires: SFExvid
BuildRequires: SFExvid-devel
%endif
BuildRequires: SUNWgawk
%if %with_x264
Requires: SFElibx264
BuildRequires: SFElibx264-devel
%endif
%if %with_giflib
Requires: SFEgiflib
BuildRequires: SFEgiflib-devel
%endif
%if %with_schroedinger
Requires: SFElibschroedinger
BuildRequires: SFElibschroedinger-devel
%endif

%define x11	/usr/openwin
%ifarch i386 amd64
%define x11	/usr/X11
%endif

%prep
%setup -q -n MPlayer-%tarball_version
%patch1 -p1
%patch4 -p1
%patch11 -p1
%patch12 -p1
%patch30 -p1
%patch31 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%if %debug_build
dbgflag=--enable-debug
#export CFLAGS="-g -D__hidden=\"\" -I%{_includedir}"
export CFLAGS="-g -D__hidden=\"\""
%else
dbgflag=--disable-debug
#export CFLAGS="-O2 -D__hidden=\"\" -I%{_includedir}"
export CFLAGS="-O3 -D__hidden=\"\" -std=gnu99"
%endif

export LDFLAGS="-L%{x11}/lib -L/usr/gnu/lib -R/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib -L%{_libdir} -R%{_libdir} -liconv" 
%if %use_gcc4
export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++
%else
export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++
%endif

bash ./configure			\
	    --prefix=%{_prefix}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --confdir=%{_sysconfdir}	\
            --enable-gui		\
            --enable-menu		\
            --extra-cflags="-I%{_libdir}/live/liveMedia/include -I%{_libdir}/live/groupsock/include -I%{_libdir}/live/UsageEnvironment/include -I%{_libdir}/live/BasicUsageEnvironment/include -I%{x11}/include -I/usr/sfw/include -I%{_prefix}/X11/include" \
            --extra-ldflags="-L%{_libdir}/live/liveMedia -R%{_libdir}/live/liveMedia -L%{_libdir}/live/groupsock -R%{_libdir}/live/groupsock -L%{_libdir}/live/UsageEnvironment -R%{_libdir}/live/UsageEnvironment -L%{_libdir}/live/BasicUsageEnvironment -R%{_libdir}/live/BasicUsageEnvironment -L%{x11}/lib -R%{x11}/lib -L/usr/gnu/lib -R/usr/gnu/lib -L/usr/sfw/lib -R/usr/sfw/lib" \
            --extra-libs='-lBasicUsageEnvironment -lUsageEnvironment -lgroupsock -lliveMedia -lstdc++ -liconv' \
            --codecsdir=%{_libdir}/mplayer/codecs \
            --enable-live		\
            --enable-network		\
	    --enable-rpath		\
            --enable-largefiles		\
	    --enable-crash-debug	\
            --enable-dynamic-plugins	\
%ifarch i386 amd64
            --enable-runtime-cpudetection	\
%endif
            --disable-xvr100		\
	    $dbgflag

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
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
ln -s /usr/share/fonts/TrueType/freefont/FreeSerif.ttf $RPM_BUILD_ROOT%{_datadir}/mplayer/subfont.ttf
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
* Thu Jun 03 2010 - Milan Jurik
- SFElibschroedinger as optional
* Mon May 31 2010 - Milan Jurik
- update to rc3, cleanup in patches
* Sun May 23 2010 - Milan Jurik
- rtsp integer overflow fix
* Mars 12 2010 - Gilles Dauphin
- includedir search path in /usr/SFE
* Tue Sep 14 2009 - Thomas Wagner
- make (Build)Requires a build-time --with_gcc4 switch defaulting to off (which is then: use SUNWgcc, gcc3)
* Sun Aug 09 2009 - Thomas Wagner
- switch to gcc4
- add (Build)Requires: SFEgcc/SFEgccruntime SUNWxwrtl SUNWxorg-mesa SUNWaalib SUNWlibsdl-devel/SUNWlibsdl SUNWlibm
* Sun Jul 05 2009 - Milan Jurik
- disable x264 support for now, incompatible with the latest x264
* Sat Mar 14 2009 - Milan Jurik
- Xvid support
- Dynamic plugin support
- SSE(2) autodetection support
- CVE-2008-5616, CVE-2008-5276, CVE-2008-0486, CVE-2008-0485, CVE 2007-2948, CVE-2008-0630
* Tue Feb 17 2009 - Thomas Wagner
- make (Build-)Requires conditional SUNWlibsndfile|SFElibsndfile(-devel)
* Wed Nov 29 2008 - dauphin@enst.fr
- change to SUNWgawk is in b101
* Wed Oct 22 2008 - dick@nagual.nl
- added SFEgawk as dep. Needed to compile without errors.
* Sun Aug 17 2008 - nonsea@users.sourceofrge.net
- Use SUNWfreetype2 instead of SFEfreetype
- Remove missed patches: Patch6, Patch7, Patch8, Patch9
- Remove BuildRequires: SFEgawk for it is in CBE now
* Thu Jul 31 2008 - trisk@acm.jhu.edu
- Use SFElibdvdnav instead of SFElibdvdplay
- Add security patches
* Sat Jun 14 2008 - trisk@acm.jhu.edu
- Update Abyss skin to 1.7
- Disable 3GPP AMR codecs as they are non-redistributable
* Tue Jan 08 2008 - moinak.ghosh@sun.com
- Link with SFEfreetype to fix missing symbol problem.
* Tue Jan 08 2008 - moinak.ghosh@sun.com
- Updated LDFLAGS to add extra libs to fix link failure
- Chenged to dependency to SFEfreetype to get newer version of freetype2
* Thu Nov 22 2007 - daymobrew@users.sourceforge.net
- Remove SUNWlibiconv dependency to try to get the module to build.
* Mon Nov 5 2007 - markwright@internode.on.net
- Bump to 1.0rc2.  Change SUNWlibcdio to SFElibcdio.  Remove SFElibfame.
- Comment mplayer-02-makefile-libfame-dep.diff (libfame removed).  Bump patch1.
- Comment patch3 (already applied). Add BuildRequires: SFEgawk.  Add patch5
- as SFEgcc 4.2.2 does not understand -rdynamic.
* Fri Oct 19 2007 - dougs@truemail.co.th
- Fixed 3gpp urls
* Tue Aug 28 2007 - dougs@truemail.co.th
- Added debug option
* Tue Jul 31 2007 - dougs@truemail.co.th
- Removed dirac codec from Requirement
* Sun Jul 15 2007 - dougs@truemail.co.th
- Removed dirac codec patch - causes crashes
* Sat Jul 14 2007 - dougs@truemail.co.th
- Added dirac codec patch
- Added SFEladspa,SFElibfribidi requirement
* Tue May  1 2007 - dougs@truemail.co.th
- Removed SFEsdl from the Required. Conflicts with SUNWlibsdl
* Sun Apr 22 2007 - dougs@truemail.co.th
- Added /usr/gnu/libs to LDFLAGS
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Add Requires SUNWsmbau after check-deps.pl run.
* Sun Jan  7 2007 - laca@sun.com
- split the codecs out into SFEmplayer-codecs
* Wed Jan  3 2007 - laca@sun.com
- re-add patches cddb and makefile-libfame-dep after merging with 1.0rc1
- add patches asmrules_20061231 (fixes a buffer overflow) and
  cabac-asm (disables some asm stuff that doesn't seem to compile on Solaris.
* Wed Nov 29 2006 - laca@sun.com
- bump to 1.0rc1
* Tue Sep 26 2006 - halton.huo@sun.com
- Add Requires after check-deps.pl run
* Tue Sep 26 2006 - halton.huo@sun.com
- Bump Source4 to version 1.6
* Thu Jul 27 2006 - halton.huo@sun.com
- Bump Source3 to version 1.6
* Fri Jun 23 2006 - laca@sun.com
- rename to SFEmplayer
- delete -share subpkg
- update file attributes
* Mon Jun 13 2006 - dougs@truemail.co.th
- Bumped version to 1.0pre8
* Mon May 8 2006 - drdoug007@yahoo.com.au
- Initial version
