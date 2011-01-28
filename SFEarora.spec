#
# spec file for package SFEsmplayer
#
# includes module: smplayer
#

%include Solaris.inc
%define srcname arora

Name:		SFEarora
Summary:	Lightweight Web browser using QtWebKit
URL:		http://code.google.com/p/arora
Vendor:		Benjamin C. Meyer
Version:	0.11.0
License:	GPL
Source:		http://%srcname.googlecode.com/files/%srcname-%version.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWgmake
BuildRequires: SUNWgnu-coreutils
BuildRequires: SUNWgtar
BuildRequires: SFEqt47-devel

Requires: SFEqt47
Requires: SUNWzlib


%if %build_l10n
%package l10n
Summary:        %summary - l10n files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires:       %name
%endif


%prep
%setup -q -n %srcname-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export PATH=$PATH:/usr/stdcxx/bin
export QMAKESPEC=solaris-cc-stdcxx
export QTDIR=/usr/stdcxx
qmake PREFIX=$RPM_BUILD_ROOT%_basedir
gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

gmake install

%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%_datadir/%srcname
%endif

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%_bindir
%dir %attr (-, root, sys) %_datadir
%dir %attr (-, root, other) %_datadir/applications
%_datadir/applications/*.desktop
%_mandir
%dir %attr (-, root, other) %_datadir/icons
%dir %attr (-, root, other) %_datadir/icons/hicolor
%dir %attr (-, root, other) %_datadir/icons/hicolor/16x16
%dir %attr (-, root, other) %_datadir/icons/hicolor/16x16/apps
%_datadir/icons/hicolor/16x16/apps/arora.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/32x32
%dir %attr (-, root, other) %_datadir/icons/hicolor/32x32/apps
%_datadir/icons/hicolor/32x32/apps/arora.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/128x128
%dir %attr (-, root, other) %_datadir/icons/hicolor/128x128/apps
%_datadir/icons/hicolor/128x128/apps/arora.png
%dir %attr (-, root, other) %_datadir/icons/hicolor/scalable
%dir %attr (-, root, other) %_datadir/icons/hicolor/scalable/apps
%_datadir/icons/hicolor/scalable/apps/arora.svg
%dir %attr (-, root, other) %_datadir/pixmaps
%_datadir/pixmaps/arora.xpm

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %_datadir
%dir %attr (-, root, other) %_datadir/%srcname/locale
%attr (-, root, other) %_datadir/%srcname/locale/*
%endif


%changelog
* Thu Jan 27 2011 - Alex Viskovatoff
- Accommodate to Qt being in /usr/stdcxx
* Sat Dec 11 2010 - Alex Viskovatoff
- Initial spec
