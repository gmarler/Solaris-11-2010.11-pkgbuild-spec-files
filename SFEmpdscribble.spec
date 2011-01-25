#
# spec file for package SFEmpdscribble
#
# includes module: mpdscribble
#

%include Solaris.inc
%define srcname mpdscribble

Name:		SFEmpdscribble
Summary:	MPD client which submits information about tracks being played to Last.fm
URL:		http://mpd.wikia.com/wiki/Client:Mpdscribble
Vendor:		Max Kellermann
Version:	0.21
License:	BSD revised
Source:		http://downloads.sourceforge.net/project/musicpd/%srcname/%version/%srcname-%version.tar.bz2
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc

BuildRequires:	SFElibmpdclient-devel
Requires:	SFElibmpdclient

Requires: %name-root
%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
Requires: %name


%prep
%setup -q -n %srcname-%version


%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%_prefix --sysconfdir=%_sysconfdir

# Be modern and use libxnet instead of libsocket
sed 's/-lsocket -lnsl/-lxnet/' Makefile > Makefile.xnet
mv Makefile.xnet Makefile

gmake -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_bindir
%_bindir/%srcname
%dir %attr (0755, root, sys) %_datadir
%dir %attr (0755, root, other) %_datadir/doc
%_datadir/doc/%srcname
%dir %attr (0755, root, bin) %_mandir
%dir %attr (0755, root, bin) %_mandir/man1
%{_mandir}/man1/%srcname.1


%files root
%defattr (-, root, sys)
%dir %attr (-, root, sys) %_sysconfdir
%attr (-, root, root) %_sysconfdir/%srcname.conf


%changelog
* Tue Jan 18 2011 - Alex Viskovatoff
- Initial spec
