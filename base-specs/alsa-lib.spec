#
# spec file for package alsa-lib
#
# includes module(s): alsa-lib
#
%define src_name alsa-lib
%define src_url ftp://ftp.alsa-project.org/pub/lib

Name:                    alsa-lib
Summary:                 ALSA Library
Version:                 1.0.23
Source:                  %{src_url}/%{src_name}-%{version}.tar.bz2
Source1:		 byteswap-compat.h
Source2:		 endian-compat.h
Patch1:			 alsa-lib-01-configure.diff
Patch2:			 alsa-lib-02-byteorder.diff
Patch3:			 alsa-lib-03-alloca.diff
Patch4:			 alsa-lib-04-inttypes.diff
Patch5:			 alsa-lib-05-ioctl.diff
Patch6:			 alsa-lib-06-async.diff
Patch7:			 alsa-lib-07-aflocal.diff
Patch8:			 alsa-lib-08-mapfile.diff
Patch9:			 alsa-lib-09-search.diff
Patch10:		 alsa-lib-10-err.diff
Patch11:		 alsa-lib-11-sockio.diff
Patch12:		 alsa-lib-12-compat.diff
Patch13:		 alsa-lib-13-global.diff
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}-%{version}
cp %{SOURCE1} include
cp %{SOURCE2} include
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
#%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

# /usr/bin/sed is busted. Find a better one :)
export PATH=/usr/gnu/bin:/usr/xpg4/bin:$PATH

CC=/usr/gcc/4.3/bin/gcc
#export LD=/usr/gnu/bin/ld
export CPPFLAGS="-D_POSIX_SOURCE -D__EXTENSIONS__ -D_XPG4_2"

%if %debug_build
export CFLAGS="-g"
dbgopt=-enable-debug
%else
export CFLAGS="-O4"
dbgopt=-disable-debug
%endif

#LDFLAGS="$( echo %_ldflags | sed 's/ -Wl,-Bdirect/ -Wl,-Bsymbolic/' )"

if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q amd64 ) ; then
	export CFLAGS="$CFLAGS -m64"
	LDFLAGS="$LDFLAGS -L/usr/gnu/lib/%{_arch64} -R/usr/gnu/lib/%{_arch64}"
else
	LDFLAGS="$LDFLAGS -L/usr/gnu/lib -R/usr/gnu/lib"
fi
export LDFLAGS

libtoolize -f -c
aclocal
autoconf -f
autoheader
automake -f -a

./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --datadir=%{_datadir}		\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}		\
            --sysconfdir=%{_sysconfdir}		\
	    --without-versioned			\
            --enable-shared			\
	    --disable-static

gmake -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a
rm -f $RPM_BUILD_ROOT%{_libdir}/alsa-lib/*/*la

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Oct 20 2010 - Milan Jurik
- bump to 1.0.23
* Sat Sep 22 2007 - dougs@truemail.co.th
- Changed to build with SFEgcc
* Sun Aug 12 2007 - dougs@truemail.co.th
- Changed to build 64bit
* Sun Aug 12 2007 - dougs@truemail.co.th
- Fixed headers for easier building of apps
* Sat Aug 11 2007 - dougs@truemail.co.th
- Initial version
