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
Source:		http://downloads.sourceforge.net/%{srcname}/%{srcname}-%{version}.tar.bz2
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

#%include build-depend.inc   # Not in repository yet
BuildRequires: SUNWgmake
BuildRequires: SUNWgnu-coreutils
BuildRequires: SUNWgtar

Requires: SFE-qt4
Requires: SUNWzlib


%prep
%setup -q -n %srcname-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi
export LIBS=-lz

# The smplayer Makefile doesn't look at CXXFLAGS or LDFLAGS.  Qt is built
# against stdcxx, but apparently not using -library=stdcxx4 when building
# smplayer doesn't do any harm.

# Use ginstall and gtar
sed -e 's/install /ginstall /' -e 's/tar /gtar /g' Makefile > Makefile.fixed
mv Makefile.fixed Makefile

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
%attr (-, root, other) %_datadir/icons/hicolor
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
* Sun Oct 17 2010 - Alex Viskovatoff
- Initial spec
