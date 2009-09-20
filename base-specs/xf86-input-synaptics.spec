#
# spec file for package xf86-input-synaptics
#
# includes module(s): xf86-input-synaptics
#

%define src_name         xf86-input-synaptics

Summary:                 Synaptics/ALPS input device driver for X.org
Version:                 1.1.3
Source:                  http://xorg.freedesktop.org/archive/individual/driver/%{src_name}-%{version}.tar.bz2
Patch1:                  xf86-input-synaptics-01-alps-tap.diff
Patch2:                  xf86-input-synaptics-02-synclient.diff
Patch3:                  xf86-input-synaptics-03-alignment.diff
Patch4:                  xf86-input-synaptics-04-syndaemon.diff
Patch5:                  xf86-input-synaptics-05-solaris.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Autoreqprov:             on

%prep
%setup -q -n%{src_name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CPPFLAGS="-I%{xorg_inc}"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags %{xorg_lib_path}"

XPREFIX="%{_prefix}/X11"
XMODULEDIR="%{_prefix}/X11/lib/modules"
# prepare for /usr/X11 going away
#if [ ! -d "%{_prefix}/X11" ]; then
#    XPREFIX="/usr"
#    XMODULEDIR="%{_prefix}/lib/modules" ];
#fi

if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
    CFLAGS="$CFLAGS -D_XSERVER64"
fi

bash ./configure	\
    --prefix=$XPREFIX	\
    --libdir=%{_prefix}/lib	\
    --mandir=$XPREFIX/share/man	\
    --with-xorg-module-dir=$XMODULEDIR

make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

XPREFIX="%{_prefix}/X11"
XMODULEDIR="%{_prefix}/X11/lib/modules"
# prepare for /usr/X11 going away
#if [ ! -d "%{_prefix/X11}" ]; then
#    XPREFIX="/usr"
#    XMODULEDIR="%{_prefix}/lib/modules"
#fi

# rename modules/input to modules/input/%{_arch64}
if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
    mkdir -p $RPM_BUILD_ROOT${XMODULEDIR}/input/%{_arch64}
    mv $RPM_BUILD_ROOT${XMODULEDIR}/input/*.so \
    $RPM_BUILD_ROOT${XMODULEDIR}/input/%{_arch64}
fi

rm -f $RPM_BUILD_ROOT${XMODULEDIR}/input/*.la

mkdir -p $RPM_BUILD_ROOT%{_datadir}/hal/fdi/policy/20thirdparty
cp fdi/*.fdi $RPM_BUILD_ROOT%{_datadir}/hal/fdi/policy/20thirdparty

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Sep 20 2009 - Albert Lee <trisk@opensolaris.org>
- Bump to 1.1.3
- Update X prefix path check
- Add patch5
- Add fdi file
* Mon Mar 09 2009 - Albert Lee
- Add patch1, patch2, patch3, patch4
* Mon Mar 02 2009 - Albert Lee
- Initial spec
