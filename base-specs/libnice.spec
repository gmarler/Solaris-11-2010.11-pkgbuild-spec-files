Version:        0.0.13
Summary:        Implementation of the IETF's Interactive Connectivity Establishment (ICE) standard

Group:          System/Libraries
License:        LGPL/MPL
URL:            http://nice.freedesktop.org/
Source:         http://nice.freedesktop.org/releases/libnice-%{version}.tar.gz
Patch1:         libnice-01-nogcc.diff
Patch2:         libnice-02-solaris.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n libnice-%{version}
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
        export LDFLAGS="$LDFLAGS -m64"
fi

export PKG_CONFIG_PATH="%{_prefix}/lib/pkgconfig"

libtoolize -f -c
aclocal --force
autoheader
automake -a -c
autoconf -f

./configure --prefix=%{_prefix}                 \
            --libdir=%{_libdir}                 \
            --datadir=%{_datadir}               \
            --mandir=%{_mandir}                 \
            --enable-shared                     \
            --disable-static

make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.{a,la}
rm -f $RPM_BUILD_ROOT%{_libdir}/gstreamer-0.10/*.{a,la}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Sep 21 2010 - Albert Lee <trisk@opensolaris.org.
- Add libtoolize
* Mon Sep 20 2010 - Albert Lee <trisk@opensolaris.org>
- Initial spec
