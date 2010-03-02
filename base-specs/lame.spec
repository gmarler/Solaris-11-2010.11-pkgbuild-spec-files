#
# spec file for package lame
#
# bugdb: http://sourceforge.net/tracker/index.php?func=detail&group_id=290&atid=100290&aid=
#

Name:                    SFElame
Summary:                 lame  - Ain't an MP3 Encoder
Version:                 3.98.3
Source:                  %{sf_download}/lame/lame-%{version}.tar.gz
# date:2008-08-17 owner:halton type:bug bugid:2054873
Patch1:                  lame-01-configure-gtk.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibms

%prep
%setup -q -n lame-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

%if %use_gcc4
export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++
%else
export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++
%endif

export CFLAGS="%optflags -I%gnu_inc"
export MSGFMT="/usr/bin/msgfmt"
export LD_OPTIONS="%gnu_lib_path"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}              \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --with-fileio=sndfile            \
            --enable-shared		     \
	    --disable-static
make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Oct 06 2009 - Milan Jurik
- LDFLAGS for gcc are not valid, removed
- xmmintrin.h hack removed, configure script detects it correctly now
* Tue Sep 15 2009 - Thomas Wagner
- add switch %use_gcc4 and CC/CXX compiler setting to be default gcc3 or explicitly gcc4
- comment out LDFLAGS since I see compile/link error arch=sse2 unkown switch
* Sat Mar 14 2009 - Milan Jurik
- upgrade to 3.98.2
* Thu Oct 23 2008 - dick@nagual.nl
- Add --with-fileio=sndfile for better file reckognize (i.e. au files)
* Sat Aug 16 2008 - nonsea@users.sourceforge.net
- Add aclocal to fix build error
- Remove commentted patch1 and patch2
* Fri Aug 15 2008 - andras.barna@gmail.com
- new version
- add a hack to disable MMX things which causes compilation failure, FIXME
- disable patch1, patch2 not needed
* Sun Apr 22 2007 - dougs@truemail.co.th
- Forced automake to automake-1.9
* Tue Mar 20 2007 - dougs@truemail.co.th
- Changed to be a base spec
* Mon Jun 12 2006 - laca@sun.com
- rename to SFElame
- change to root:bin to follow other JDS pkgs.
- go back to 02l version of toolame because the beta tarball download site
  is gone.
* Mon May  8 2006 - drdoug007@yahoo.com.au
- Initial version
