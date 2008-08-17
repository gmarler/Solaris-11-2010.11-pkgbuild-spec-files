#
# spec file for package lame
#
# bugdb: http://sourceforge.net/tracker/index.php?func=detail&group_id=290&atid=100290&aid=
#
Name:                    SFElame
Summary:                 lame  - Ain't an MP3 Encoder
Version:                 398
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
export CFLAGS="%optflags -I%gnu_inc"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"
export LDFLAGS="%_ldflags %gnu_lib_path"
export LD_OPTIONS="%gnu_lib_path"

libtoolize --force
aclocal $ACLOCAL_FLAGS
autoconf
autoheader
automake -a -c -f
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}              \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared		     \
	    --disable-static
##FIXME ugly hack
perl -pi -e 's/\#define HAVE_XMMINTRIN_H 1/\/\*\ #define HAVE_XMMINTRIN_H 1\*\/ /' config.h
make -j$CPUS LDFLAGS="%{_ldflags}"

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
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
