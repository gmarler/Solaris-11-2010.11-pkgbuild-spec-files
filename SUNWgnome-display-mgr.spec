#
# spec file for package SUNWgnome-display-mgr
#
# includes module(s): gdm
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#
%include Solaris.inc

Summary:                 GNOME display manager
Name:                    SUNWgnome-display-mgr
Version:                 2.25.92
Release:                 1
Source:                  http://download.gnome.org/sources/gdm/2.25/gdm-%{version}.tar.bz2
Source1:                 gdm.xml
Source2:                 svc-gdm
# date:2009-02-13 owner:yippi type:branding
Patch1:                  gdm-01-branding.diff
# Patch1 adds SDTLOGIN interface, which drops the Xserver to user
# perms rather than running as root, for added security on Solaris.
# It also adds logindevperm support.  Refer to bug #531651.  My
# hope is to get logindevperm support upstream.
# date:2008-05-06 owner:yippi type:bug bugid:531651
Patch2:                  gdm-02-sdtlogin-devperm.diff
# Add ctrun support when running the user session.  Otherwise, any
# core dump in the user session will cause GDM to restart.
Patch3:                  gdm-03-ctrun.diff
# Manage displays on the fly
# date:2008-06-03 owner:yippi type:bug bugid:536355
Patch4:                  gdm-04-dynamic-display.diff
# Possible fix for unwritable gdm user $HOME. gnome-session
# tries to update ~/.ICEAuthority and gdm-simple-greeter crashes
# when looking up option widgets.
# date:2008-09-29 owner:yippi type:bug bugid:554242
Patch5:                  gdm-05-ICE-optionwidget.diff
# Fix gconf-santiy-check-2 warning dialog.
# date:2008-09-04 owner:yippi type:bug bugid:550832
Patch6:			 gdm-06-gconfsanity.diff
# date:2008-12-16 owner:yippi type:bug bugid:568323
Patch7:                  gdm-07-hide-face-browser.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SUNWlibrsvg-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWlxml
BuildRequires: SUNWlibcroco
BuildRequires: SUNWlibpopt-devel
BuildRequires: SUNWlibrsvg-devel
%if %option_without_fox
#
# GDM's configure depends on Xephyr to be installed so it properly
# sets Xnest configure option.
BuildRequires: SUNWxorg-server
Requires: SUNWxorg-server
Requires: SUNWxwplt
%else
# if SUNWxwplt is installed, then configure finds /usr/X11/bin/Xserver
# instead of /usr/X11/bin/Xorg
BuildConflicts: SUNWxwplt
%endif
Requires: SUNWlibms
Requires: SUNWlibpopt
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-libs
Requires: SUNWgnome-display-mgr-root
Requires: SUNWgnome-dialog
Requires: SUNWlibrsvg
Requires: SUNWlxml
Requires: SUNWlibcroco
Requires: SUNWpostrun
Requires: SFEconsolekit
%if %option_with_dt
Requires: SUNWgnome-dtlogin-integration
%else
Requires: SUNWgnome-dtstart
%endif

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n gdm-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
# disable dynamic patch for now, since we're working new ways for it, refer to
# http://wiki.genunix.org/wiki/index.php/design_for_newgdm_consolekit_multiseat_multidisplay
#%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
export LDFLAGS="%_ldflags"
export PKG_CONFIG_PATH=%{_pkg_config_path}
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
%if %option_without_dt
export GDMGNOMESESSIONCMD="/usr/bin/dtstart jds"
%endif

%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

glib-gettextize -f
# FIXME: create m4 dir as workaround for bugzilla #575218
mkdir m4
intltoolize --force --copy --automake
aclocal $ACLOCAL_FLAGS -I . -I ./m4
libtoolize --copy --force
autoheader
automake -a -c -f
autoconf
./configure \
        --prefix=%{_prefix} \
        --sysconfdir=%{_sysconfdir} \
        --localstatedir=%{_localstatedir} \
        --mandir=%{_mandir} \
        --libexecdir=%{_libexecdir} \
        --with-pam-prefix=%{_sysconfdir} \
        --disable-scrollkeeper \
        --with-ctrun=yes \
        --with-default-path=/usr/bin:/usr/X11/bin:/usr/openwin/bin \
        --enable-rbac-shutdown=solaris.system.shutdown

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/var/svc/manifest/application/graphical-login
install --mode=0444 %SOURCE1 $RPM_BUILD_ROOT/var/svc/manifest/application/graphical-login
install -d $RPM_BUILD_ROOT/lib/svc/method 
cp %SOURCE2 $RPM_BUILD_ROOT/lib/svc/method/

rmdir $RPM_BUILD_ROOT/etc/pam.d

# The gdm-factory-slave and the gdm-product-slave are non-functional and
# under development.  Do not ship these until they are ready.
#
rm $RPM_BUILD_ROOT/%{_libexecdir}/gdm-factory-slave
rm $RPM_BUILD_ROOT/%{_libexecdir}/gdm-product-slave

# The /var/run directory should not be included with the packages.
# GDM will create it at run-time.
#
rmdir $RPM_BUILD_ROOT/var/run/gdm
rmdir $RPM_BUILD_ROOT/var/run

install -d $RPM_BUILD_ROOT/%{_sysconfdir}/X11/xinit/xinitrc.d

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/*help/*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/gdm/*-[a-z]*.omf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS

%post root
( echo 'test -x /usr/bin/gconftool-2 || {';
  echo '  echo "ERROR: gconftool-2 not found"';
  echo '  exit 1';
  echo '}';
  echo 'umask 0022';
  echo 'GCONF_CONFIG_SOURCE=xml:merged:/etc/gconf/gconf.xml.defaults';
  echo 'export GCONF_CONFIG_SOURCE';
  echo '/usr/bin/gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/*.schemas > /dev/null'
) | $BASEDIR/var/lib/postrun/postrun -u -c JDS_wait

cat >> $BASEDIR/var/svc/profile/upgrade <<\EOF

# We changed gdm's FMRI.  If the old service exists and is enabled,
# disable it and enable the new one.
gdm=svc:/application/gdm2-login:default
if svcprop -q $gdm; then
	set -- `svcprop -C -t -p general/enabled $gdm`
	if [ $? -ne 0 ]; then
		echo "Could not read whether $gdm was enabled."
	elif [ $2 != boolean ]; then
		echo "general/enabled property of $gdm has bad type."
	elif [ $# -ne 3 ]; then
		echo "general/enabled property of $gdm has the wrong number\c"
		echo " of values."
	elif [ $3 = true ]; then
		svcadm disable $gdm
		svcadm enable svc:/application/graphical-login/gdm:default
	fi
fi

EOF

%postun
test -x $BASEDIR/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS

%preun root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo 'test -x $PKG_INSTALL_ROOT/usr/bin/gconftool-2 || {';
  echo '  echo "WARNING: gconftool-2 not found; not uninstalling gconf schemas"';
  echo '  exit 0';
  echo '}';
  echo 'umask 0022';
  echo 'GCONF_CONFIG_SOURCE=xml:merged:$BASEDIR/etc/gconf/gconf.xml.defaults';
  echo 'GCONF_BACKEND_DIR=$PKG_INSTALL_ROOT/usr/lib/GConf/2';
  echo 'LD_LIBRARY_PATH=$PKG_INSTALL_ROOT/usr/lib';
  echo 'export GCONF_CONFIG_SOURCE GCONF_BACKEND_DIR LD_LIBRARY_PATH';
  echo 'SDIR=$BASEDIR%{_sysconfdir}/gconf/schemas';
  echo 'schemas="$SDIR/gdm-simple-greeter.schemas"';
  echo '$PKG_INSTALL_ROOT/usr/bin/gconftool-2 --makefile-uninstall-rule $schemas > /dev/null'
) | $BASEDIR/var/lib/postrun/postrun -i -c JDS_wait -a

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/gdm
%{_sbindir}/gdm-binary
%{_sbindir}/gdm-restart
%{_sbindir}/gdm-safe-restart
%{_sbindir}/gdm-stop
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/bonobo
%{_libexecdir}/gdm*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gdm
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/gdm/C
%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16/
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32/
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/*/apps
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/omf/gdm/*-C.omf
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/gnome-2.0/*
%{_datadir}/pixmaps/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%dir %attr (0755, root, bin) %{_sysconfdir}/dbus-1
%dir %attr (0755, root, bin) %{_sysconfdir}/dbus-1/system.d
%{_sysconfdir}/dbus-1/system.d/*
%{_sysconfdir}/gconf
%dir %{_sysconfdir}/gdm
%{_sysconfdir}/gdm/*
%dir %{_sysconfdir}/X11/xinit
%dir %{_sysconfdir}/X11/xinit/xinitrc.d
# don't use %_localstatedir for the /var/log and /var/svc directory,
# because these are an absolute path defined by another package, so
# it has to be /var/svc even if this package has its %_localstatedir
# redefined.
%dir %attr (0755, root, sys) /var
%dir %attr (0755, root, sys) /var/log
%dir %attr (1770, root, gdm) /var/log/gdm
/var/svc/*
# SVC method file
%dir %attr (0755, root, bin) /lib
%dir %attr (0755, root, bin) /lib/svc
%dir %attr (0755, root, bin) /lib/svc/method
%attr (0555, root, bin) /lib/svc/method/svc-gdm
%{_localstatedir}/gdm
%dir %attr (0755, root, other) %{_localstatedir}/lib
%dir %attr (1770, root, gdm) %{_localstatedir}/lib/gdm
%dir %attr (1750, root, gdm) %{_localstatedir}/lib/gdm/.gconf.mandatory
%attr (1640, root, gdm) %{_localstatedir}/lib/gdm/.gconf.path
%attr (1640, root, gdm) %{_localstatedir}/lib/gdm/.gconf.mandatory/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%attr (-, root, other) %{_datadir}/locale
%{_datadir}/gnome/*help/*/[a-z]*
%{_datadir}/omf/gdm/*-[a-z]*.omf
%endif

%changelog
* Fri Mar 13 2009 - halton.huo@sun.com
- Bump to 2.25.92
- Remove patch upstreamed layout.diff
- Disable patch dynamic-display.diff for now
- Use --with-default-path=/usr/bin:/usr/X11/bin:/usr/openwin/bin
  instead of --with-path=/usr/openwin/bin
* Fri Feb 13 2009 - brian.cameron@sun.com
- Add patch gdm-01-branding.diff to change default setting of DisallowTCP
  to false.  Add patch gdm-09-default-path.diff to set the default PATH
  via configuration value.
* Sat Feb 07 2009 - brian.cameron@sun.com
- Package should not install anything to /var/run.
* Mon Dec 22 2008 - brian.cameron@sun.com
- Add call to intltoolize, needed when building on Nevada.
* Wed Dec 17 2008 - brian.cameron@sun.com
- Bump to 2.25.2.
* Tue Dec 16 2008 - brian.cameron@sun.com
- Add patch gdm-07-hide-face-browser.diff so that the face browser is
  hidden when the disable_user_list configuration option is TRUE.
  Add patch gdm-08-layout.diff to fix the GDM GUI so that the keyboard
  switcher applet is not shown when it is empty such as when libxklavier
  is not present.
* Fri Dec 12 2008 - brian.cameron@sun.com
- Add patch gdm-06-fixcrash to address crashing issue with 2.25.1.
* Thu Dec 11 2008 - brian.cameron@sun.com
- Bump to 2.25.1.
* Wed Nov 19 2008 - halton.huo@sun.com
- Bump to 2.24.1.
- Remove upstreamed patch 01-lang.diff and reorder
- Add patch 07-Xau.diff to fix bugzilla:561480
- Remove "-L/usr/openwin/lib -lXau -R/usr/openwin/lib -R/usr/sfw/lib" from
  LDFLAGS
- Remove useless X11_CFLAGS and PERL5LIB stuff 
* Tue Nov 04 2008 - brian.cameron@sun.com
- Add patch gdm-07-fixshell.diff to set the SHELL in GDM's Xsession script.
  Otherwise the user's shell will fail to start up if any usage of ksh is
  in the session startup.  For example, this causes problems with Sun Ray
  startup scripts.
* Tue Oct 21 2008 - halton.huo@sun.com
- Add standard patch comment
* Mon Oct 20 2008 - halton.huo@sun.com
- Add Requires: SFEconsolekit
- enable patch5 ICE-optionwidget.diff
* Tue Oct 14 2008 - brian.cameron@sun.com
- Add %{_sysconfdir}/X11/xinit/xinitrc.d to packaging.
* Sat Sep 27 2008 - brian.cameron@sun.com
- Renumber patches.
* Wed Sep 24 2008 - simon.zheng@sun.com
- Bump to 2.24.0. Remove upstream 05-crash.diff.
* Wed Sep 17 2008 - brian.cameron@sun.com
- Bump to 2.23.92.
* Fri Sep 05 2008 - simon.zheng@sun.com
- Add patch 05-crash.diff.
* Tue Aug 26 2008 - brian.cameron@sun.com
- Bump to 2.23.90.
* Thu Aug 11 2008 - simon.zheng@sun.com
- Rework 04-dynamic-display.diff.
* Thu Aug 07 2008 - brian.cameron@sun.com
- Bump to 2.23.2.
* Tue Jun 03 2008 - brian.cameron@sun.com
- Add patch gdm-01-lang.diff, patch by Takao Fujiwara, to fix the language
  support in GDM.  Remove patch gdm-03-fixcrash.diff since it is no longer
  needed.  Renumber patches.
* Tue May 27 2008 - simon.zheng@sun.com
- Remove gdm-01-fixgio.diff. Already fixed in gio bug #533369.
* Thu May 22 2008 - brian.cameron@sun.com
- Add gdm-06-scripts.diff so that PostLogin, PreSession, and PostSession
  scripts get run at the appropriate times.
* Sat May 17 2008 - simon.zheng@sun.com
- Rework 04-dynamic-display.diff for gdm 2.22.0.
* Thu May 08 2008 - brian.cameron@sun.com
- Add SVC method script svc-gdm, which is needed because the new GDM does not
  run as a daemon, so the script launches gdm in the background.
* Mon May 05 2008 - brian.cameron@sun.com
- Add 06-ctrun.diff to add ctrun support.  Otherwise any SEGV in
  the user session will cause GDM to restart.
* Sun May 04 2008 - simon.zheng@sun.com
- Remove 05-setting-daemon.diff because we have another
  fix on gnome-settings-daemon.
- Add 05-xauth-dir.diff.
* Sat May 03 2008 - brian.cameron@sun.com
- bump to 2.22.0.
* Wed May 02 2008 - simon.zheng@sun.com
- Add 05-settings-daemon.diff.
* Thu Apr 24 2008 - simon.zheng@sun.com
- Install greeter schema files in section %post root.
* Mon Apr 14 2008 - simon.zheng@sun.com
- Add 04-dynamic-display.diff. Try to manage display
  on the fly.
* Tue Mar 11 2008 - brian.cameron@sun.com
- Bump to 2.21.9.  Remove upstream gdm-04-logo-name.diff
  patch.
* Fri Feb 29 2008 - simon.zheng@sun.com
- Add patch 04-logo-icon.diff to fix greeter crach.
* Mon Feb 25 2008 - brian.cameron@sun.com
- Bump to 2.21.8.
* Wed Feb 20 2008 - brian.cameron@sun.com
- Add information about SDTLOGIN patch, which is currently
  not enabled.
* Sat Jan 26 2008 - brian.cameron@sun.com
- Created for 2.21 branch.
