#
# spec file for package SUNWgnome-screensaver
#
# includes module(s): gnome-screensaver
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: me, me, me, I want it!
#
%include Solaris.inc

%use gss = gnome-screensaver.spec

Name:                    SFEgnome-screensaver
Summary:                 GNOME screensaver
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires:	SUNWcsl
Requires:       SUNWdbus
Requires:       SUNWgtk2
Requires:       SUNWlibglade
Requires:       SUNWlibpopt
Requires:	SUNWlxml
Requires:	SUNWgnome-config
Requires:	SUNWgnome-panel
Requires:       SUNWlibms
Requires:       SUNWzlib
Requires:       SUNWpostrun
Requires:       %{name}-root
BuildRequires:	SUNWcsl
BuildRequires:  SUNWdbus-devel
BuildRequires:  SUNWgtk2-devel
BuildRequires:  SUNWlibglade-devel
BuildRequires:  SUNWlibpopt-devel
BuildRequires:	SUNWlxml
BuildRequires:	SUNWgnome-config-devel
BuildRequires:	SUNWgnome-panel-devel

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires:                %{name}

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version
%gss.prep -d %name-%version

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
%gss.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gss.install -d %name-%version

rm -r $RPM_BUILD_ROOT%{_sysconfdir}/pam.d

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif                                


%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait

%postun
test -x $BASEDIR/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/gnome-screensaver
%{_libdir}/gnome-screensaver-gl-helper
%{_libexecdir}/gnome-screensaver-dialog
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_datadir}/desktop-directories
%{_datadir}/gnome-screensaver
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, other) %{_datadir}/backgrounds
%{_datadir}/backgrounds/*
%dir %attr (0755, root, bin) %{_datadir}/gnome-background-properties
%{_datadir}/gnome-background-properties/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/gnome-screensaver.1
%{_mandir}/man1/gnome-screensaver-command.1
%{_mandir}/man1/gnome-screensaver-preferences.1

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/gnome-screensaver.schemas
%{_sysconfdir}/xdg

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Thu Jan 31 2007 - damien.carbery@sun.com
- Add manpages to %files after tarball bump.
* Fri Oct  5 2007 - laca@sun.com
- set CFLAGS and LDFLAGS
* Wed May 09 2007 - damien.carbery@sun.com
- Add %{_libdir}/gnome-screensaver-gl-helper to %files after getting new tarball
  to build.
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Thu Jun 29 2006 - laca@sun.com
- update postrun scripts
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Mon Feb 20 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Sat Dec  3 2005 - laca@sun.com
- add %post script that runs update-desktop-database
* Wed Nov 30 2005 - damien.carbery@sun.com
- Add ACLOCAL_FLAGS setting back as it is needed in bumped tarball.
* Fri Nov 04 2005 - damien.carbery@sun.com
- Remove ACLOCAL_FLAGS setting as bugs fixed in bumped tarball.
* Tue Nov 01 2005 - damien.carbery@sun.com
- Set ACLOCAL_FLAGS for use in base spec file.
* Tue Oct 25 2005 - damien.carbery@sun.com
- Remove unused environment variables in %build section.
* Mon Oct 24 2005 - damien.carbery@sun.com
- Remove share package; add build and runtime dependencies.
* Fri Oct 21 2005 - damien.carbery@sun.com
- Initial spec file created.

