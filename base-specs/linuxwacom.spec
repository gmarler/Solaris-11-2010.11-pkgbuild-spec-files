#
# spec file for package linuxwacom
#
# includes module(s): linuxwacom
#

%define src_name         linuxwacom	

Summary:                 Wacom input device driver for X.org
Version:                 0.8.4-2
Source:                  %{sf_download}/linuxwacom/%{src_name}-%{version}.tar.bz2
URL:                     http://linuxwacom.sourceforge.net/
Patch1:                  linuxwacom-01-no-usb.diff
Patch2:                  linuxwacom-02-sunpro.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Autoreqprov:             on

%prep
%setup -q -n%{src_name}-%{version}
%patch1 -p1
%patch2 -p1

# automake returns error if not present
if [ ! -f "NEWS" ]; then
    touch "NEWS"
fi

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CPPFLAGS="-I%{xorg_inc}"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags %{xorg_lib_path}"

XPREFIX="%{_prefix}/X11"
XMODULEDIR="%{_prefix}/X11/lib/modules/input"
# prepare for /usr/X11 going away
#if [ ! -d "%{_prefix/X11}" ]; then
#    XPREFIX="/usr"
#    XMODULEDIR="%{_prefix}/lib/modules/input"
#fi

if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
    XMODULEDIR="$XMODULEDIR/%{_arch64}"
    CFLAGS="$CFLAGS -D_XSERVER64"
fi

aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf
bash ./configure	\
    --prefix=$XPREFIX \
    --mandir=$XPREFIX/share/man	\
    --with-x	\
    --with-xmoduledir=$XMODULEDIR

make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

XPREFIX="%{_prefix}/X11"
XMODULEDIR="%{_prefix}/X11/lib/modules/input"
# prepare for /usr/X11 going away
#if [ ! -d "%{_prefix/X11}" ]; then
#    XPREFIX="/usr"
#    XMODULEDIR="%{_prefix}/lib/modules/input"
#fi

if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
    XMODULEDIR="$XMODULEDIR/%{_arch64}"
fi

rm -f $RPM_BUILD_ROOT${XPREFIX}/lib/*.a
rm -f $RPM_BUILD_ROOT${XPREFIX}/lib/*.la
rm -f $RPM_BUILD_ROOT${XMODULEDIR}/*.la

mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/hal
mv $RPM_BUILD_ROOT${XPREFIX}/libexec/* $RPM_BUILD_ROOT%{_prefix}/lib/hal
rmdir $RPM_BUILD_ROOT${XPREFIX}/libexec

if [ "%{_datadir}" != "$XPREFIX/share" ]; then
    mkdir -p $RPM_BUILD_ROOT%{_datadir}
    cp -rp $RPM_BUILD_ROOT${XPREFIX}/share/hal $RPM_BUILD_ROOT%{_datadir}
    rm -rf $RPM_BUILD_ROOT${XPREFIX}/share/hal
fi

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Sep 20 2009 - Albert Lee <trisk@opensolaris.org>
- Bump to 0.8.4-2
- Update X prefix path check
- Add fdi file
* Tue Dec 16 2008 - trisk@acm.jhu.edu
- Fix 64-bit driver crash
* Tue Dec 16 2008 - trisk@acm.jhu.edu
- Initial spec
