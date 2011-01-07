#
# spec file for package handbrake
#
# Copyright 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:         HandBrake
License:      GPL
Version:      0.9.5
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      handbrake - multiplatform, multithreaded video transcoder
Source:       http://downloads.sourceforge.net/project/handbrake/%{version}/HandBrake-%{version}.tar.bz2
Patch1:       handbrake-01-ffmpeg.diff
Patch2:       handbrake-02-fontconfig.diff
Patch3:       handbrake-03-downloads.diff
Patch4:       handbrake-04-moduledefs.diff
Patch5:       handbrake-05-m64.diff
Patch6:       handbrake-06-libiconvdisable.diff
Patch7:       handbrake-07-flags.diff

URL:          http://handbrake.fr
BuildRoot:    %{_tmppath}/%{name}-%{version}-build


%prep
%setup -q -n HandBrake-%version
%patch1 -p1
touch contrib/fontconfig/P01-solaris.patch
%patch2 -p1
%patch4 -p1
# disable libiconv
%patch6 -p1

# enable x64 build
#%patch5 -p1

# manually (re)set ldflags for /usr/gnu/lib (change per your setup)
%patch7 -p1

# depreciated
rm contrib/x264/P01-solaris.patch


# The handbrake build system automatically downloads sources it needs.
# This will cause pkgbuild download-only to fail. An alternative is to
# download everything one time, and use it for successive builds.
#  default == no
%define bandwidthsavermode 0
#%define bandwidthsavermode 1

%if %bandwidthsavermode
%patch3 -p1
# Edit this path if you want downloaded srcs persistent across reboots
#handbraketmpdir="/tmp/handbrakehax"
if [ ! -d $handbraketmpdir ]; then
    mkdir -p $handbraketmpdir
    cd $handbraketmpdir
    # populate downloads directory

    wget http://download.m0k.org/handbrake/contrib/a52dec-0.7.4.tar.gz
    wget http://download.m0k.org/handbrake/contrib/libiconv-1.13.tar.bz2
    wget http://download.m0k.org/handbrake/contrib/faac-1.28.tar.gz
    wget http://download.handbrake.fr/handbrake/contrib/bzip2-1.0.6.tar.gz
    wget http://download.m0k.org/handbrake/contrib/ffmpeg-r25689.tar.bz2
    wget http://download.m0k.org/handbrake/contrib/libsamplerate-0.1.4.tar.gz
    wget http://download.m0k.org/handbrake/contrib/a52dec-0.7.4.tar.gz
    wget http://download.m0k.org/handbrake/contrib/zlib-1.2.3.tar.gz
    wget http://download.m0k.org/handbrake/contrib/libmkv-0.6.4.1-0-ga80e593.tar.bz2
    wget http://download.m0k.org/handbrake/contrib/libdca-r81-strapped.tar.gz
    wget http://download.m0k.org/handbrake/contrib/libdvdnav-svn1168.tar.gz
    wget http://download.m0k.org/handbrake/contrib/mp4v2-trunk-r355.tar.bz2
    wget http://download.m0k.org/handbrake/contrib/fontconfig-2.8.0.tar.gz
    wget http://download.m0k.org/handbrake/contrib/faad2-2.7.tar.gz
    wget http://download.m0k.org/handbrake/contrib/libxml2-2.7.7.tar.gz
    wget http://download.m0k.org/handbrake/contrib/pthreads-w32-cvs20100909.tar.bz2
    wget http://download.m0k.org/handbrake/contrib/libvorbis-aotuv_b5.tar.gz
    wget http://download.m0k.org/handbrake/contrib/libogg-1.1.3.tar.gz
    wget http://download.m0k.org/handbrake/contrib/freetype-2.3.9.tar.gz
    wget http://download.m0k.org/handbrake/contrib/lame-3.98.tar.gz
    wget http://download.m0k.org/handbrake/contrib/libass-0.9.9.tar.bz2
    wget http://download.handbrake.fr/handbrake/contrib/x264-r1834-a51816a.tar.gz
    wget http://download.m0k.org/handbrake/contrib/libdvdread-svn1168.tar.gz
    wget http://download.m0k.org/handbrake/contrib/mpeg2dec-0.5.1.tar.gz
    wget http://download.m0k.org/handbrake/contrib/libtheora-1.1.0.tar.bz2
    wget http://download.m0k.org/handbrake/contrib/libbluray-0.0.1-pre-16-g1aab213.tar.gz
fi

mkdir -p download
cp -r $handbraketmpdir/* download
%endif  # bandwidthsavermode



%build

# All this is necessary to free up enough registers on x86
%ifarch i386
export CFLAGS="%optflags -Os -fno-rename-registers -fomit-frame-pointer -fno-PIC -UPIC -mpreferred-stack-boundary=4 -I%{xorg_inc} -I%{_includedir}"
%else
export CFLAGS="%optflags -Os -I%{xorg_inc} -I%{_includedir}"
%endif
export LDFLAGS="%_ldflags %{xorg_lib_path} -L/usr/gnu/lib -R/usr/gnu/lib -L%{_libdir} -R%{_libdir}"

./configure --prefix=%{_prefix} \
            --disable-gtk

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
cd build
gmake -j$CPUS 

%install
cd build
gmake install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Wed Dec 16 2010 - jchoi42@pha.jhu.edu
- initial spec
