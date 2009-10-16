#
# spec file for package fvwm.spec
#
# includes module(s): fvwm
#
%include Solaris.inc

%define src_url		ftp://ftp.fvwm.org/pub/fvwm/version-2

Name:                   fvwm
Summary:                fvwm window manager
Version:                2.5.28
Source:                 %{src_url}/%{name}-%{version}.tar.gz

%prep
%setup -q -n %{name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

X11LIB="-L/usr/X11/lib -R/usr/X11/lib"
GNULIB="-L/usr/gnu/lib -R/usr/gnu/lib"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CPPFLAGS="-I/usr/gnu/lib -I/usr/X11/include"
export CFLAGS="%{optflags} -I/usr/X11/include -I/usr/gnu/include"
export LDFLAGS="%{_ldflags} $GNULIB $X11LIB"

libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
automake --add-missing
autoconf --force

./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --datadir=%{_datadir}		\
            --libexecdir=%{_libexecdir} 	\
            --sysconfdir=%{_sysconfdir} 	\
            --enable-shared			\
	    --disable-static		

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT
fvwmdir=$RPM_BUILD_ROOT%{_datadir}/fvwm
mv $fvwmdir/system.fvwm2rc-sample-95 $fvwmdir/system.fvwm2rc

%changelog
* Fri Apr 27 2006 - dougs@truemail.co.th
- Initial version
