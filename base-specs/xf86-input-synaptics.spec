#
# spec file for package xf86-input-synaptics
#
# includes module(s): xf86-input-synaptics
#

%define src_name         xf86-input-synaptics

Summary:                 Synaptics/ALPS input device driver for X.org
Version:                 1.0.0
Source:                  http://xorg.freedesktop.org/archive/individual/driver/%{src_name}-%{version}.tar.bz2
Patch1:                  xf86-input-synaptics-01-alps-tap.diff
Patch2:                  xf86-input-synaptics-02-synclient.diff
Patch3:                  xf86-input-synaptics-03-alignment.diff
Patch4:                  xf86-input-synaptics-04-syndaemon.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Autoreqprov:             on

%prep
%setup -q -n%{src_name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CPPFLAGS="-I%{xorg_inc}"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags %{xorg_lib_path}"

if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
    XMODULEDIR="%{_prefix}/X11/lib/modules/%{_arch64}"
    CFLAGS="$CFLAGS -D_XSERVER64"
else
    XMODULEDIR="%{_prefix}/X11/lib/modules"
fi

bash ./configure	\
    --prefix=%{_prefix}/X11	\
    --libdir=%{_prefix}/lib	\
    --mandir=%{_prefix}/X11/share/man	\
    --with-xorg-module-dir=$XMODULEDIR

make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

# rename modules/%{_arch64}/input to modules/input/%{_arch64}
if [ -d $RPM_BUILD_ROOT%{_prefix}/X11/lib/modules/%{_arch64} ]; then
  rm -f $RPM_BUILD_ROOT%{_prefix}/X11/lib/modules/%{_arch64}/input/*.la
  mkdir -p $RPM_BUILD_ROOT%{_prefix}/X11/lib/modules/input
  mv $RPM_BUILD_ROOT%{_prefix}/X11/lib/modules/%{_arch64}/input \
    $RPM_BUILD_ROOT%{_prefix}/X11/lib/modules/input/%{_arch64}
  rm -rf $RPM_BUILD_ROOT%{_prefix}/X11/lib/modules/%{_arch64}
else
  rm -f $RPM_BUILD_ROOT%{_prefix}/X11/lib/modules/input/*.la
fi

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Mar 09 2009 - Albert Lee
- Add patch1, patch2, patch3, patch4
* Mon Mar 02 2009 - Albert Lee
- Initial spec
