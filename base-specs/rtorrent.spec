#
# spec file for package rtorrent
#
# includes module(s): rtorrent
#

Name:           rtorrent
Summary:        ncurses BitTorrent client
URL:            http://libtorrent.rakshasa.no/
Version:        0.8.2
Source:         http://libtorrent.rakshasa.no/downloads/%{name}-%{version}.tar.gz
Patch1:         rtorrent-01-solaris.diff
Patch2:         rtorrent-02-event-ports.diff
Patch3:         rtorrent-03-curl-event.diff
Patch4:         rtorrent-04-sunpro.diff
Patch5:         rtorrent-05-sunpro-crash.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{name}-%{version}
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

aclocal -I ./scripts
autoheader
libtoolize --automake --copy --force
automake
autoconf
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_cxx_libdir}     \
            --libexecdir=%{_libexecdir}	\
            --sysconfdir=%{_sysconfdir}	\
            --enable-shared		\
	    --disable-static		\
	    --with-xmlrpc-c

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Jun 27 2008 - trisk@acm.jhu.edu
- Add patch3 for scalable curl events, patch4, patch5 for Studio compatibility
* Sat May 24 2008 - trisk@acm.jhu.edu
- Enable XML-RPC, add patch2
* Fri May  9 2008 - laca@sun.com
- Initial base spec file
