#
# spec file for package SFEsakura
#
# includes module: sakura
#

%include Solaris.inc
%define srcname sakura

Name:		SFEsakura
Summary:	Lightweight terminal emulator based on GTK and VTE
URL:		http://www.pleyades.net/david/sakura.php
Version:	2.3.8
License:	GPLv2
Source:		http://www.pleyades.net/david/projects/%srcname/%srcname-%version.tar.bz2
%include default-depend.inc
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
BuildRequires:	SUNWgmake
BuildRequires:	SUNWcmake
BuildRequires:	SUNWgtk2-devel
Requires:	SUNWgtk2
BuildRequires:	SUNWgnome-terminal
Requires:	SUNWgnome-terminal
BuildRequires:	SUNWncurses
Requires:	SUNWncurses

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

cmake -DCMAKE_INSTALL_PREFIX=%_prefix .

gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

gmake install

mkdir -p $RPM_BUILD_ROOT/%_prefix
mv ./sfw_stage/* $RPM_BUILD_ROOT/%_prefix

%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%_datadir/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%_bindir/sakura
%dir %attr (-, root, sys) %_datadir
%dir %attr (-, root, other) %_datadir/applications
%_datadir/applications/sakura.desktop
%dir %attr (-, root, other) %_datadir/doc
%_datadir/doc/sakura
%dir %attr (-, root, other) %_datadir/pixmaps
%_datadir/pixmaps/*


%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %_datadir
%dir %attr (-, root, other) %_datadir/locale
%attr (-, root, other) %_datadir/locale/*
%endif


%changelog
* Wed Dec  8 2010 - Alex Viskovatoff
- Initial spec
