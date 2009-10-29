#
# spec file for package libmtp
#
# includes module(s): libmtp
#

%define src_ver 1.0.1
%define src_name libmtp
%define src_url http://jaist.dl.sourceforge.net/sourceforge/%{src_name}

Name:		libmtp
Summary:	Implementation of Microsoft's Media Transfer Protocol (MTP)
License:        LGPL
Version:	%{src_ver}
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		libmtp-01-wall.diff
Patch2:		libmtp-02-u_int.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

#if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
#    SFWLIB="-L/usr/sfw/lib/%{_arch64} -R/usr/sfw/lib/%{_arch64}"
#else
#    SFWLIB="-L/usr/sfw/lib -R/usr/sfw/lib"
#fi

#export CPPFLAGS="-I/usr/sfw/include"
export CFLAGS="%optflags"
#export LDFLAGS="%_ldflags $SFWLIB"
export CC=gcc
export CXX=g++
export CXXFLAGS="%gcc_cxx_optflags"
export LDFLAGS="%_ldflags"

export LD_LIBRARY_PATH=/usr/gnu/lib

#libtoolize -f -c
#aclocal-1.10 -I m4
#autoheader
#autoconf -f
#automake-1.10 -a -f

./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_cxx_libdir}		\
            --libexecdir=%{_libexecdir}	\
            --sysconfdir=%{_sysconfdir}	\
            --with-libiconv-prefix=/usr/gnu \
            --with-gnu-ld               \
            --enable-shared		\
	    --disable-static

#perl -pi -e 's,-shared,-Wl,-G' libtool
gmake

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_cxx_libdir}/lib*.*a
rm -f $RPM_BUILD_ROOT%{_cxx_libdir}/libmtp/lib*.*a

# Replace hard links with relative links
cd $RPM_BUILD_ROOT%{_bindir}
rm -f mtp-delfile mtp-getfile mtp-newfolder mtp-sendfile mtp-sendtr
ln -sf mtp-connect mtp-delfile
ln -sf mtp-connect mtp-getfile
ln -sf mtp-connect mtp-newfolder
ln -sf mtp-connect mtp-sendfile
ln -sf mtp-connect mtp-sendtr

# FIXME: this hack works around that fact that libusb comes without
# a pkgconfig .pc file on Solaris
cd $RPM_BUILD_ROOT%{_cxx_libdir}/pkgconfig
grep -v 'Requires: libusb' libmtp.pc > libmtp.pc.new
sed -e 's,\(^Libs: .*\),\1 -L/usr/gnu/lib -R/usr/gnu/lib -lusb,' \
    libmtp.pc.new > libmtp.pc
rm libmtp.pc.new

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Oct 23 2009 - jchoi42@pha.jhu.edu
- Bump to 1.0.1, updated both patches to this version, add libiconv
- changed to build against /usr/lib/g++/ and without libtool (officially available verson is too old)
* Sun Dec 30 2007 - markwright@internode.on.net
- Bump to 0.2.4
* Tue Sep 18 2007 - dougs@truemail.co.th
- Initial base spec file
