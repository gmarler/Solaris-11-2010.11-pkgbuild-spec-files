#
# spec file for package SFEconsolekit
#
# includes module(s): ConsoleKit
#
# bugdb: http://bugs.freedesktop.org/show_bug.cgi?id=
#
%include Solaris.inc

# build with dbus support unless --without-dbus is used
%define with_dbus %{?_without_dbus:0}%{?!_without_dbus:1}

# Option to decide whether or not build library pam_ck_connector,
# which implements pam_sm_open_session(3PAM) and pam_sm_close_session(3PAM).
# By default, we don't build it.
#
# Note: To enable this pam module, you have to manually add 
# an entry to /etc/pam.conf after installing SFEconsolekit-pam,
# like this.
# "login   session required       pam_ck_connector.so debug"
#
%define build_pam_module 1

Name:                    SFEconsolekit
Summary:                 Framework for tracking users, login sessions, and seats.
Version:                 0.3.0
URL:                     http://www.freedesktop.org/wiki/Software/ConsoleKit
Source:                  http://people.freedesktop.org/~mccann/dist/ConsoleKit-%{version}.tar.bz2
Source1:                 consolekit.xml
# date:2008-01-31 owner:yippi type:bug bugid:18149
Patch1:                  ConsoleKit-01-emptystruct.diff
# date:2008-03-02 owner:halton type:bug bugid:18173
Patch2:                  ConsoleKit-02-pam.diff
# date:2008-03-04 owner:halton type:bug bugid:18261
Patch3:                  ConsoleKit-03-ck-history.diff
# date:2008-12-30 owner:halton type:bug bugid:19333
Patch4:                  ConsoleKit-04-ck-dynamic.diff
# date:2008-06-24 owner:halton type:bug bugid:15866
# Disable getcurrentsession.diff for now, since halton think it is not
# a bug actually
#Patch5:                  ConsoleKit-05-getcurrentsession.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWPython
BuildRequires: SUNWdbus-devel
BuildRequires: SUNWdbus-bindings-devel
Requires: SUNWgnome-libs
Requires: SUNWdbus
Requires: SUNWdbus-bindings
Requires: %name-root

%if %option_with_gnu_iconv
Requires: SUNWgnu-libiconv
Requires: SUNWgnu-gettext
%else
Requires: SUNWuiu8
%endif

%if %option_with_fox
Requires: FSWxorg-clientlibs
Requires: FSWxwrtl
BuildRequires: FSWxorg-headers
%else
Requires: SUNWxwrtl
Requires: SUNWxwplt
Requires: SUNWxorg-clientlibs
%endif

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SUNWpostrun
Requires: SUNWgnome-config

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%if %build_pam_module
%package pam
Summary:		 %{summary} - PAM module to register simple text logins. 
SUNW_BaseDir:		 %{_basedir}
%include default-depend.inc
Requires: %name
%endif

%prep
%setup -q -n ConsoleKit-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
#%patch5 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags -I/usr/sfw/include -DANSICPP"
%if %option_with_gnu_iconv
export CFLAGS="$CFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl"
%endif
%if %option_with_fox
# for <X11/Xlib.h>
export CFLAGS="$CFLAGS -I/usr/X11/include"
%endif
export RPM_OPT_FLAGS="$CFLAGS"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CPPFLAGS="-I/usr/sfw/include"
export LDFLAGS="-L/usr/sfw/lib -R/usr/sfw/lib"
export MSGFMT="/usr/bin/msgfmt"

glib-gettextize -f
libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f 
autoconf
./configure --prefix=%{_prefix}                     \
            --libdir=%{_libdir}                     \
            --libexecdir=%{_libexecdir}             \
            --localstatedir=%{_localstatedir}       \
            --sysconfdir=%{_sysconfdir}             \
	    --mandir=%{_mandir}			    \
%if %build_pam_module
	    --enable-pam-module			    \
	    --with-pam-module-dir=%{_libdir}/security	\
%endif
            --enable-rbac-shutdown=solaris.system.shutdown

make
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
%if %build_pam_module
%else
# delete useless directory /usr/man/man8 which stores pam_ck_connector.8 
rm -rf $RPM_BUILD_ROOT/%{_mandir}
%endif

# These programs are intended to be used if you want ConsoleKit to be
# like utmp/wtmp and log system start/restart/stop events.  There are
# no plans to support using ConsoleKit like utmp/wtmp, so do not
# install these for now.
#
rm $RPM_BUILD_ROOT/%{_sbindir}/ck-log-system-start
rm $RPM_BUILD_ROOT/%{_sbindir}/ck-log-system-restart
rm $RPM_BUILD_ROOT/%{_sbindir}/ck-log-system-stop


install -d $RPM_BUILD_ROOT/var/svc/manifest/system
install --mode=0444 %SOURCE1 $RPM_BUILD_ROOT/var/svc/manifest/system

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/lib*.so*
%{_libdir}/ConsoleKit
%{_libexecdir}/ck-collect-session-info
%{_libexecdir}/ck-get-x11-server-pid
%{_libexecdir}/ck-get-x11-display-device
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/dbus-1

%files root
%defattr (-, root, sys)
%{_sysconfdir}/ConsoleKit/seats.d/00-primary.seat
%{_sysconfdir}/ConsoleKit/run-session.d
%dir %attr (0755, root, bin) %{_sysconfdir}/dbus-1
%dir %attr (0755, root, bin) %{_sysconfdir}/dbus-1/system.d
%{_sysconfdir}/dbus-1/system.d/ConsoleKit.conf
%dir %attr (0755, root, sys) %dir %{_localstatedir}
# don't use %_localstatedir here, because this is an absolute path
# defined by another package, so it has to be /var/svc even if this
# package's %_localstatedir is redefined
/var/svc/*
%dir %attr (0755, root, sys) %{_localstatedir}/log
%dir %attr (0755, root, root) %{_localstatedir}/log/ConsoleKit
%dir %attr (0755, root, root) %{_localstatedir}/run/ConsoleKit

%files devel
%defattr (-, root, bin)
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%if %build_pam_module
%files pam
%defattr (-, root, bin)
%{_libdir}/security/pam*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}/man8/*
%endif

%changelog
* Tue Dec 30 2008 - halton.huo@sun.com
- Add patch ck-dynamic.diff to fix bug #19333
* Tue Oct 21 2008 - halton.huo@sun.com
- Add standard patch comment
* Thu Aug 07 2008 - brian.cameorn@sun.com
- Bump to 0.3.0.
* Tue Jun 24 2008 - simon.zheng@sun.com
- Add patch 05-getcurrentsession.diff for freedesktop bug #15866.
* Tue Mar 11 2008 - brian.cameron@sun.com
- Minor cleanup
* Tue Mar 04 2008 - simon.zheng@sun.com
- Add patch 04-ck-history.diff to fix crash.
* Sat Mar 01 2008 - simon.zheng@sun.com
- Add patch 03-pam.diff to build pam module library 
  pam-ck-connector that registers text login session into 
  ConsoleKit. And this library is packed as a separate 
  package called SFEconsolekit-pam.
* Mon Feb 25 2008 - brian.cameron@sun.com
- Bump release to 0.2.10.  Worked with the maintainer to get seven
  recent patches upstream.
* Mon Feb 25 2008 - simon.zheng@sun.com
- Rework ConsoleKit-06-fixvt.diff for better macro definition.
* Fri Feb 22 2008 - brian.cameron@sun.com
- Add the patch ConsoleKit-05-devname.diff that Simon wrote, patch
  ConsoleKit-06-fixvt.diff so that patch 4 builds properly when you
  do not have VT installed, patch ConsoleKit-07-fixactiveconsole.diff
  so that Active device is set to "/dev/console" when not using VT,
  ConsoleKit-08-fixseat.diff to correct a crash due to a NULL string
  in a printf, and ConsoleKit-09-novt.diff to fix ConsoleKit so that
  it sets x11-display-device to "/dev/console" when not using
  VT.
* Tue Feb 19 2008 - simon.zheng@sun.com
- Add patch ConsoleKit-04-vt.diff. Use sysnchronous event notification
  in STREAMS to monitor VT activation. 
* Fri Feb 15 2008 - brian.cameron@sun.com
- Rework ConsoleKit-03-paths.diff so it makes better use of #ifdefs.
* Fri Feb 15 2008 - simon.zheng@sun.com
- Bump to 0.2.9. Add ConsoleKit-03-noheaderpaths.diff because there's not
  header paths.h on Solaris.
* Thu Feb 07 2008 - Brian.Cameron@sun.com
- Add /var/log/ConsoleKit/history file to packaging.
* Thu Jan 31 2008 - Brian.Cameron@sun.com
- Bump to 0.2.7.  Remove two upstream patches added on January 25,
  2007.
* Fri Jan 25 2008 - Brian.Cameron@sun.com
- Bump to 0.2.6.  Rework patches.  Add patch ConsoleKit-02-RBAC.diff
  to make ConsoleKit use RBAC instead of PolicyKit on Solaris.
  Patch ConsoleKit-03-fixbugs.diff fixes some bugs I found.
* Tue Sep 18 2007 - Brian.Cameron@sun.com
- Bump to 0.2.3.  Remove upstream ConsoleKit-01-head.diff
  patch and add ConsoleKit-02-fixsolaris.diff to fix some
  issues building ConsoleKit when VT is not present.
* Mon Aug 16 2007 - Brian.Cameron@sun.com
- Created.
