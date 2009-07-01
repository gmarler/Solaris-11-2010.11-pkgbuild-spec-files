#
# spec file for package SFEffmpeg
#
# includes module(s): FFmpeg
#

Summary:                 FFmpeg - a very fast video and audio converter

Version:                 0.5
#Source:                  http://pkgbuild.sf.net/spec-files-extra/tarballs/ffmpeg-export-%{year}-%{month}-%{day}.tar.bz2
#Source:                  http://electricsheep.org/ffmpeg-0.4.9-p%{year}%{month}%{day}.tar.bz2
Source:                  http://ffmpeg.mplayerhq.hu/releases/ffmpeg-%{version}.tar.bz2
URL:                     http://ffmpeg.mplayerhq.hu/index.html
#Patch1:                  ffmpeg-01-BE_16.diff
Patch2:                  ffmpeg-02-configure.diff
#Patch3:                  ffmpeg-03-v4l2.diff
Patch4:                  ffmpeg-04-options.diff
Patch5:                  ffmpeg-05-mlib.diff
# Security: CVE-2008-3162
#Patch6:                  ffmpeg-06-cve-2008-3162.diff
Patch7:                  ffmpeg-07-new-v4l2.diff
Patch8:                  ffmpeg-08-versionsh.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Autoreqprov:             on

%prep
#%setup -q -n ffmpeg-export-%{year}-%{month}-%{day}
%setup -q -n ffmpeg-%version
#%patch1 -p1
%patch2 -p1
#%patch3 -p1
%patch4 -p1
%patch5 -p1
#%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
# for pod2man
export PATH=/usr/perl5/bin:$PATH
export CC=/usr/sfw/bin/gcc
# All this is necessary to free up enough registers on x86
%ifarch i386
export CFLAGS="%gcc_optflags -fno-rename-registers -fomit-frame-pointer -fno-PIC -UPIC -mpreferred-stack-boundary=4 -I%{xorg_inc}"
%else
export CFLAGS="%gcc_optflags -I%{xorg_inc}"
%endif
export LDFLAGS="%_ldflags %{xorg_lib_path}"
bash ./configure	\
    --prefix=%{_prefix} \
    --libdir=%{_libdir}	\
    --shlibdir=%{_libdir}	\
    --mandir=%{_mandir}	\
    --cc=$CC		\
    %{arch_opt}		\
    --disable-optimizations	\
    --disable-debug	\
    --enable-gpl	\
    --enable-postproc	\
    --enable-avfilter   \
    --enable-swscale	\
    --disable-vhook	\
    --enable-libgsm	\
    --enable-libxvid	\
    --enable-libx264	\
    --enable-libfaad	\
    --enable-libfaadbin	\
    --enable-libtheora	\
    --enable-libmp3lame	\
    --enable-libvorbis	\
    --disable-libamr-nb	\
    --disable-libamr-wb	\
    --enable-x11grab	\
    --enable-libspeex   \
    --enable-pthreads	\
    --disable-static	\
    --extra-ldflags=-mimpure-text \
    --enable-shared

gmake 

%install
gmake install DESTDIR=$RPM_BUILD_ROOT BINDIR=$RPM_BUILD_ROOT%{_bindir}

mkdir $RPM_BUILD_ROOT%{_libdir}/ffmpeg
cp config.mak $RPM_BUILD_ROOT%{_libdir}/ffmpeg

# Create a ffmpeg.pc - Some apps need it
cat > $RPM_BUILD_ROOT%{_libdir}/pkgconfig/ffmpeg.pc << EOM
Name: ffmpeg
prefix=%{_prefix}
exec_prefix=${prefix}
libdir=${exec_prefix}/lib
includedir=${prefix}/include
Description: FFmpeg codec library
Version: 51.40.4
Requires:  libavcodec libpostproc libavutil libavformat libswscale x264 ogg theora vorbisenc vorbis dts
Conflicts:
EOM

#mv $RPM_BUILD_ROOT%{_libdir}/lib*.*a $RPM_BUILD_ROOT%{_libdir}/ffmpeg

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* San Jun 28 2009 - Milan Jurik
- switch to GNU make
* Mon Mar 16 2009 - Milan Jurik
- version 0.5
* Thu Aug 07 2008 - trisk@acm.jhu.edu
- Add patch6, update CFLAGS
* Thu Mar 27 2008 - trisk@acm.jhu.edu
- Convert to base-spec
- Update to 0.4.9-p20080326 from electricsheep.org
- Update patches
- Disable static libs
* Mon Jun 30 2008 - andras.barna@gmail.com
- Force SFWgcc
- Add -I/usr/X11/include
* Tue Mar 18 2008 - trisk@acm.jhu.edu
- Add patch5 to fix green tint with mediaLib, contributed by James Cheng
* Sat Aug 11 2007 - trisk@acm.jhu.edu
- Disable mediaLib support on non-sparc (conflicts with MMX)
- Enable x11grab for X11 recording
- Enable v4l2 demuxer for video capture
- Add workaround for options crash
* Wed Aug  3 2007 - dougs@truemail.co.th
- Bumped export version
- Added codecs
- Created ffmpeg.pc
* Tue Jul 31 2007 - dougs@truemail.co.th
- Added SUNWlibsdl test. Otherwise require SFEsdl
* Sat Jul 14 2007 - dougs@truemail.co.th
- Build shared library
* Sun Jan 21 2007 - laca@sun.com
- fix devel pkg default attributes
* Wed Jan 10 2007 - laca@sun.com
- create
