#
# spec file for package libsndfile
#
# includes module(s): libsndfile
#

%define src_name libsndfile
%define src_url http://www.mega-nerd.com/%{src_name}
Name:		libsndfile
Summary:	libsndfile  - a library of C routines for reading and writing files containing sampled audio data
Version:	1.0.19
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		libsndfile-01-flac-1.1.3.diff
Patch2:		libsndfile-02-cpp_test.diff
Patch3:		libsndfile-03-endian.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export CXXFLAGS="%cxx_optflags -features=extensions"
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif

./configure --prefix=%{_prefix}		\
	    --mandir=%{_mandir}		\
            --bindir=%{_bindir}		\
            --libdir=%{_libdir}		\
            --libexecdir=%{_libexecdir}	\
            --sysconfdir=%{_sysconfdir}	\
            --disable-alsa              \
            --disable-sqlite            \
            --enable-shared		\
	    --disable-static

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Mar 03 2009 - Thomas Wagner
- bump to 1.0.19
* Tue Oct 16 2007 - laca@sun.com
- disable use of sqlite for now -- no 64-bit version
- disable alsa support for now -- breaks the build
* Sun Aug 12 2007 - dougs@truemail.co.th
- Changed to build 64bit
* Mon Apr 30 2007 - laca@sun.com
- bump to 1.0.17
- add gentoo patch that makes it build with flac 1.1.3
- add patch that fixes the cpp_test test program when built with sun studio
* Mon Jun 12 2006 - laca@sun.com
- rename to SFElibsndfile
- change to root:bin to follow other JDS pkgs.
- get rid of -share pkg
- move stuff around between base and -devel
- add missing deps
* Mon May 8 2006 - drdoug007@yahoo.com.au
- Initial version
