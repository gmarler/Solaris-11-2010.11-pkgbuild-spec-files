#
# spec file for package alsa-plugins
#
# includes module(s): alsa-plugins
#

%define src_name alsa-plugins
%define src_url ftp://ftp.alsa-project.org/pub/plugins

Name:			 alsa-plugins
Summary:                 ALSA Plugins
Version:                 1.0.14
Source:                  %{src_url}/%{src_name}-%{version}.tar.bz2
Source1:		 asound.conf
Patch1:			 alsa-plugins-01-configure.diff
Patch2:			 alsa-plugins-02-oss.diff
Patch3:			 alsa-plugins-03-dsp.diff
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

CC=/usr/sfw/bin/gcc
export CPPFLAGS="-D_POSIX_SOURCE -D__EXTENSIONS__ -D_XPG4_2"
export CFLAGS="-O3"
export LDFLAGS="%_ldflags"

if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q amd64 ) ; then
        export CFLAGS="$CFLAGS -m64"
        export LDFLAGS="-Wl,-64 -L%{_libdir} -R%{_libdir} $LDFLAGS"
	pulseopt=--with-pulseaudio=no
fi

libtoolize -f -c
aclocal
autoheader
automake -f -a
autoconf -f
./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --datadir=%{_datadir}		\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}		\
            --sysconfdir=%{_sysconfdir}		\
            --enable-shared			\
	    --disable-static			\
	    $pulseopt

gmake -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/alsa-lib/*.la

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
cp %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Aug 12 2007 - dougs@truemail.co.th
- Initial version
