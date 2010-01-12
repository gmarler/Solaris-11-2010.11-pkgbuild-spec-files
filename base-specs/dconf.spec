Name:         dconf
Version:      0.2
Release:      1

Group:        System/Libraries/GNOME
License:      LGPL
URL:          http://live.gnome.org/dconf
Source:       http://ftp.acc.umu.se/pub/gnome/sources/%{name}/%{version}/%{name}-%{version}.tar.bz2
# date:2010-01-11 owner:jedy type:branding
Patch1:       dconf-01-build.diff


%prep
%setup -q
%patch1 -p1


%build
%ifos linux
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

#aclocal $ACLOCAL_FLAGS
#libtoolize --copy --force
#autoheader
#automake -a -c -f  -Wno-portability
#autoconf
./configure --prefix=%{_prefix} \
		--bindir=%{_bindir} \
		--sysconfdir=%{_sysconfdir} \
		--libexecdir=%{_libdir} \
		--libdir=%{_libdir}
make -j $CPUS


%install
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'


%clean 
rm -rf $RPM_BUILD_ROOT


%changelog
* Tue Jan 12 2010 - jedy.wang@sun.com
- Initial spec
