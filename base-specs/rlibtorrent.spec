#
# spec file for package rlibtorrent
#
# includes module(s): libtorrent
#

Name:           libtorrent
Summary:        BitTorrent library written in C++
URL:            http://libtorrent.rakshasa.no/
Version:        0.12.2
Source:         http://libtorrent.rakshasa.no/downloads/%{name}-%{version}.tar.gz
Patch1:         rlibtorrent-01-madvise.diff
Patch2:         rlibtorrent-02-event-ports.diff
Patch3:         rlibtorrent-03-dh-generate.diff
Patch4:         rlibtorrent-04-sunpro.diff
Patch5:         rlibtorrent-05-tracker-usable.diff
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
            --disable-shared		\
	    --enable-static		\
	    --with-ports

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_cxx_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Jul 04 2008 - trisk@acm.jhu.edu
- Add patch5 for bug in tracker updating
* Thu Jun 26 2008 - trisk@acm.jhu.edu
- Add patch3 for DH key error, patch4 for Studio compatibility
* Mon Jun 16 2008 - trisk@acm.jhu.edu
- Rename to rlibtorrent
- Make static library for SFErtorrent
* Sat May 24 2008 - trisk@acm.jhu.edu.
- Enable ports, add patch2
* Fri May  9 2008 - laca@sun.com
- Initial base spec file
