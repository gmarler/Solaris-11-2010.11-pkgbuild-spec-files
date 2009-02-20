#
# spec file for package SFEmplayer
#
# includes module(s): mplayer
#
%include Solaris.inc

%define with_dvdnav %(pkginfo -q SFElibdvdnav && echo 1 || echo 0)
%define with_faad %(pkginfo -q SFEfaad && echo 1 || echo 0)
%define with_fribidi %(pkginfo -q SFElibfribidi && echo 1 || echo 0)
%define with_ladspa %(pkginfo -q SFEladspa && echo 1 || echo 0)
%define with_openal %(pkginfo -q SFEopenal && echo 1 || echo 0)
%define with_mad %(pkginfo -q SFElibmad && echo 1 || echo 0)
%define with_liba52 %(pkginfo -q SFEliba52 && echo 1 || echo 0)
%define with_lame %(pkginfo -q SFElame && echo 1 || echo 0)
%define with_twolame %(pkginfo -q SFEtwolame && echo 1 || echo 0)
%define with_mpcdec %(pkginfo -q SFElibmpcdec && echo 1 || echo 0)

%define SFElibsndfile   %(/usr/bin/pkginfo -q SFElibsndfile && echo 1 || echo 0)

Name:                    SFEmplayer
Summary:                 mplayer - The Movie Player
Version:                 1.0
%define tarball_version 1.0rc2
URL:                     http://www.mplayerhq.hu/
Source:                  http://www.mplayerhq.hu/MPlayer/releases/MPlayer-%{tarball_version}.tar.bz2
Patch1:                  mplayer-01-cddb.diff
#Patch2:                 mplayer-02-makefile-libfame-dep.diff
#Patch3:                 mplayer-03-asmrules_20061231.diff
Patch4:                  mplayer-04-cabac-asm.diff
Patch5:                  mplayer-05-configure.diff
Source3:                 http://www.mplayerhq.hu/MPlayer/skins/Blue-1.7.tar.bz2
Source4:                 http://www.mplayerhq.hu/MPlayer/skins/Abyss-1.7.tar.bz2
Source5:                 http://www.mplayerhq.hu/MPlayer/skins/neutron-1.5.tar.bz2
Source6:                 http://www.mplayerhq.hu/MPlayer/skins/proton-1.2.tar.bz2
#Source7:                 http://www.3gpp.org/ftp/Specs/latest/Rel-6/26_series/26104-610.zip
#Source8:                 http://www.3gpp.org/ftp/Specs/latest/Rel-6/26_series/26204-610.zip
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{tarball_version}-build

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
#BuildRequires: SFEgawk
# FIXME: If have dvdnav, need use --disable-dvdread-internal when ./configure,
# but this will cause build fail, do not use it for now.
Requires: SFElibdvdnav
BuildRequires: SFElibdvdnav-devel
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
#latest CDE include gawk, so remove SFEgawk depedency 
#BuildRequires: SFEgawk

%define x11	/usr/openwin
%ifarch i386 amd64
%define x11	/usr/X11
%endif

%prep
%setup -q -n MPlayer-%tarball_version
%patch1 -p1
#%patch2 -p1
#%patch3 -p1
%patch4 -p1
%patch5 -p1

#unzip %SOURCE7
#unzip 26104-610_ANSI_C_source_code.zip
#mv c-code libavcodec/amr_float
#unzip %SOURCE8
#unzip 26204-610_ANSI-C_source_code.zip
#mv c-code libavcodec/amrwb_float

perl -pi -e 's/-O2/-O1/' configure

%build
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
rm -rf ./grep
ln -s /usr/sfw/bin/ggrep ./grep
PATH="`pwd`:$PATH"
echo "`type grep`"

bash ./configure				\
	    --prefix=%{_prefix}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --confdir=%{_sysconfdir}		\
            --enable-gui			\
            --enable-menu			\
            --with-extraincdir=/usr/lib/live/liveMedia/include:/usr/lib/live/groupsock/include:/usr/lib/live/UsageEnvironment/include:/usr/lib/live/BasicUsageEnvironment/include:%{x11}/include:/usr/sfw/include \
            --with-extralibdir=/usr/lib/live/liveMedia:/usr/lib/live/groupsock:/usr/lib/live/UsageEnvironment:/usr/lib/live/BasicUsageEnvironment:%{x11}/lib:/usr/gnu/lib:/usr/sfw/lib \
            --extra-libs='-lBasicUsageEnvironment -lUsageEnvironment -lgroupsock -lliveMedia -lsocket -lnsl -lstdc++ -liconv' \
            --codecsdir=%{_libdir}/mplayer/codecs \
%if %with_faad
            --enable-faad-external		\
%endif
            --enable-live			\
            --enable-network			\
	    --enable-rpath			\
            --enable-largefiles			\
	    --enable-crash-debug		\
            --disable-directfb			\
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
