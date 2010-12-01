#
# spec file for package SFEliferea.spec
#
# includes module(s): liferea
#
%include Solaris.inc

Name:		SFEliferea
Summary:	Liferea - aggregator for online news feeds
Version:	1.6.5
Source:		%{sf_download}/liferea/liferea-%{version}.tar.gz
URL:		http://liferea.sourceforge.net/
Group:		Applications/Internet
License:	GPLv2
Patch3:		liferea-03-no-unix03.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWdbus-devel
BuildRequires: SUNWfirefox-devel
Requires: SUNWgnome-libs
Requires: SUNWdbus
Requires: SUNWfirefox
Requires: SUNWpostrun
Requires: %{name}-root
Requires: SUNWbash
%if %option_with_gnu_iconv
Requires: SUNWgnu-libiconv
Requires: SUNWgnu-gettext
%else
Requires: SUNWuiu8
%endif
BuildRequires: SFEwebkitgtk-devel
Requires: SFEwebkitgtk

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
%setup -q -n liferea-%version
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
%if %option_with_gnu_iconv
export CFLAGS="$CFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl"
%endif
export CXXFLAGS="%cxx_optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="-R/usr/lib/firefox"

glib-gettextize -f
libtoolize --copy --force
intltoolize --force --copy
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f 
autoconf

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}

# FIXME: adding INTLLIBS=-lresolv is cheating, instead,
# src/Makefile.am and configure.in should be updated to link to resolv
# when needed.
make -j$CPUS INTLLIBS=-lresolv

%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make DESTDIR=$RPM_BUILD_ROOT install
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post root
( echo 'test -x /usr/bin/gconftool-2 || {';
  echo '  echo "ERROR: gconftool-2 not found"';
  echo '  exit 0';
  echo '}';
  echo 'umask 0022';
  echo "GCONF_CONFIG_SOURCE=xml:merged:%{_sysconfdir}/gconf/gconf.xml.defaults";
  echo 'export GCONF_CONFIG_SOURCE';
  echo "SDIR=%{_sysconfdir}/gconf/schemas";
  echo '/usr/bin/gconftool-2 --makefile-install-rule $SDIR/liferea.schemas'
) | $PKG_INSTALL_ROOT/usr/lib/postrun

%preun root
( echo 'test -x /usr/bin/gconftool-2 || {';
  echo '  echo "ERROR: gconftool-2 not found"';
  echo '  exit 0';
  echo '}';
  echo 'umask 0022';
  echo "GCONF_CONFIG_SOURCE=xml:merged:%{_sysconfdir}/gconf/gconf.xml.defaults";
  echo 'export GCONF_CONFIG_SOURCE';
  echo "SDIR=%{_sysconfdir}/gconf/schemas";
  echo '/usr/bin/gconftool-2 --makefile-uninstall-rule $SDIR/liferea.schemas'
) | $PKG_INSTALL_ROOT/usr/lib/postrun

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/liferea
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16/apps
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/apps
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/apps
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/apps
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/apps
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/apps
%{_datadir}/liferea/*
%{_datadir}/icons/hicolor/16x16/apps/*
%{_datadir}/icons/hicolor/22x22/apps/*
%{_datadir}/icons/hicolor/24x24/apps/*
%{_datadir}/icons/hicolor/32x32/apps/*
%{_datadir}/icons/hicolor/48x48/apps/*
%{_datadir}/icons/hicolor/scalable/apps/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%files root
%defattr (0755, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/liferea.schemas

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (0755, root, other) %{_datadir}/locale
%endif

%changelog
* Wed Dec 01 2010 - Milan Jurik
- bump to 1.6.5
* Sun Aug 08 2010 - Milan Jurik
- bump to 1.6.4, remove upstream patches
* Fri May 21 2010 - Milan Jurik
- update to 1.6.3, dependency on webkit
* Mon Jun 23 2008 - river@wikimedia.org
- 1.4.16b
* Sun Nov 18 2007 - daymobrew@users.sourceforge.net
- Add support for building on Indiana systems.
* Thu Jun 22 2006 - laca@sun.com
- bump to 1.0.15
- rename to SFEliferea
- delete -share pkg
- use %post/%preun scripts for installing gconf schemas
- add patch that fixes the wrapper script
* Fri May 05 2006 - damien.carbery@sun.com
- Point to sourceforge mirror for tarball.
* Wed May 03 2006 - damien.carbery@sun.com
- Bump to 1.0.11.
* Tue Apr 11 2006 - glynn.foster@sun.com
- Initial spec file
