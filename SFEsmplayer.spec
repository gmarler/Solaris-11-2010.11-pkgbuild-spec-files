#
# spec file for package SFEsmplayer
#
# includes module: smplayer
#

%include Solaris.inc
%define srcname smplayer

Name:		SFEsmplayer
Summary:	MPlayer front-end
URL:		http://smplayer.sourceforge.net
Vendor:		Ricardo Villalba
Version:	0.6.9
License:	GPL
Source:		%sf_download/%srcname/%srcname-%version.tar.bz2
Patch1:		smplayer-01-std-namespace.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWgmake
BuildRequires: SUNWgnu-coreutils
BuildRequires: SUNWgtar
BuildRequires: SFEqt47-devel
Requires: SFEqt47
Requires: SUNWzlib


%prep
%setup -q -n %srcname-%version
%patch1 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export LIBS=-lz
export PATH=$PATH:/usr/stdcxx/bin
export QMAKESPEC=solaris-cc-stdcxx
export QTDIR=/usr/stdcxx
gmake -j$CPUS PREFIX=%_basedir

%install
rm -rf $RPM_BUILD_ROOT

gmake install PREFIX=%_basedir DOC_PATH=%_docdir/%srcname DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%_bindir/%srcname
%dir %attr (-, root, sys) %_datadir
%dir %attr (-, root, other) %_datadir/applications
%_datadir/applications/*.desktop
%dir %attr (-, root, other) %_docdir
%_docdir/%srcname
%_mandir
%_datadir/%srcname
%dir %attr (-, root, other) %_datadir/icons
%dir %attr (-, root, other) %_datadir/icons/hicolor
%dir %attr (-, root, other) %_datadir/icons/hicolor/16x16
%dir %attr (-, root, other) %_datadir/icons/hicolor/16x16/apps
%_datadir/icons/hicolor/16x16/apps/smplayer.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/22x22
%dir %attr (-, root, other) %_datadir/icons/hicolor/22x22/apps
%_datadir/icons/hicolor/22x22/apps/smplayer.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/32x32
%dir %attr (-, root, other) %_datadir/icons/hicolor/32x32/apps
%_datadir/icons/hicolor/32x32/apps/smplayer.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/64x64
%dir %attr (-, root, other) %_datadir/icons/hicolor/64x64/apps
%_datadir/icons/hicolor/64x64/apps/smplayer.png


%changelog
* Fri Jan 28 2011 - Alex Viskovatoff
- Stop linking to libCstd (which did not cause crashes for some reason)
- Add the Qt bin directory to $PATH, so one patch is no longer needed
* Thu Jan 27 2011 - Alex Viskovatoff
- Use SFEqt47, adding two patches
* Sun Oct 17 2010 - Alex Viskovatoff
- Initial spec
