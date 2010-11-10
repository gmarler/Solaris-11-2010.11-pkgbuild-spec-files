#
# spec file for package libx264
#
# includes module(s): libx264
#

%define         snap    20101029
%define         snaph   2245
%define src_name x264-snapshot
%define src_url	 http://download.videolan.org/pub/videolan/x264/snapshots

Name:                    libx264
Summary:                 H264 encoder library
Version:                 %{snap}
Source:                  %{src_url}/%{src_name}-%{snap}-%{snaph}.tar.bz2
Source1:                 libx264-replacement-version.sh
URL:                     http://www.videolan.org/developers/x264.html
#Patch1:	         libx264-01-gccisms.diff
#Patch2:                 libx264-02-version.diff
Patch3:                  libx264-03-ld.diff
#Patch4:                 libx264-04-ginstall.diff
#Patch5:                 libx264-05-ssse3.diff
Patch6:                  libx264-06-gpac.diff
Patch7:                  libx264-07-soname.diff
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}-%{snap}-%{snaph}

#replaces patch2 libx264-02-version.diff
cp %{SOURCE1} version.sh

#unused
#%patch1 -p1
#obsoleted by Source1
#%patch2 -p1
%patch3 -p1
#obsolete 
#%patch4 -p1
#reviewd needed? 
#%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lm -L/lib -R/lib"

if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
        export LDFLAGS="$LDFLAGS -m64"
	if [ `uname -p` == "i386" ]; then
		export host="amd64-pc-solaris2.11"
	fi
	if [ `uname -p` == "sparc" ]; then
		sed s/v8plusa/v9a/ configure > configure.new
		mv configure.new configure
		chmod +x configure 
	fi
else
	unset host
fi

./configure	\
    --prefix=%{_prefix}		\
    --bindir=%{_bindir}		\
    --libdir=%{_libdir}		\
    --enable-pic		\
    --extra-cflags="$CFLAGS"	\
    --extra-ldflags="$LDFLAGS"	\
    --enable-shared

make

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Nov 10 2010 - Alex Viskovatoff
- update to new tarball
- reworked patches libx264-02-version.diff (though replaced by Source1),
  libx264-03-ld.diff
  re-worked and re-added libx264-06-gpac.diff (gpac_static not found -> use gpac)
- added Source1 ext-sources/libx264-replacement-version.sh to just copy the file
  over instead of patching (no more patch reworking)
- removed obsolete configure options
* Fri May 21 2010 - Milan Jurik
- update to new tarball
* Sat Nov 28 2009 - Albert Lee <trisk@opensolaris.org>
- Remove GPAC dependency
* Fri Oct 30 2009 - Milan Jurik
- support for multiarch on sparc
* Tue Sep 08 2009 - Milan Jurik
- initial base spec file
