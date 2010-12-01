#
# spec file for package SFEguake.spec
#
# includes module(s): guake
#
%include Solaris.inc

%define src_name	guake

Name:		SFEguake
URL:		http://guake.org/
Summary:	Guake is a top-down terminal for Gnome
Version:	0.4.2
Group:		Applications/System 
License:	GPLv2+ 
URL:		http://guake.org/
Source:		http://guake.org/files/%{src_name}-%{version}.tar.gz 
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:	%name-root
BuildRequires:	SUNWgnome-common-devel
BuildRequires:	SUNWgnome-python26-desktop
Requires:	SUNWgnome-python26-desktop
BuildRequires:	SUNWgnome-python26-extras
Requires:	SUNWgnome-python26-extras
BuildRequires:	SUNWgnome-python26-libs
Requires:	SUNWgnome-python26-libs
BuildRequires:	SUNWpython26-notify
Requires:	SUNWpython26-notify
BuildRequires:	SUNWperl-xml-parser
BuildRequires:	SUNWgnome-config
Requires:	SUNWgnome-config
BuildRequires:	SUNWpython26-xdg
Requires:	SUNWpython26-xdg
Requires:	SUNWpostrun
BuildRequires:	SUNWgnome-terminal
Requires:	SUNWgnome-terminal
BuildRequires:	SUNWxwinc
Requires:	SUNWxwplt


%description
Guake is a drop-down terminal for Gnome Desktop Environment,
so you just need to press a key to invoke him, and press again to hide.

%package root
Summary:	%summary - platform dependent files, / filesystem
SUNW_BaseDir:	/
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:	%{summary} - l10n files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%{name}
%endif

%prep
%setup -q -n %{src_name}-%{version}

%build
./configure --prefix=%{_prefix}	\
	--sysconfdir=%{_sysconfdir} \
	--disable-static 

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
test -x $PKG_INSTALL_ROOT/usr/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $PKG_INSTALL_ROOT/usr/lib/postrun

%postun
test -x $PKG_INSTALL_ROOT/usr/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $PKG_INSTALL_ROOT/usr/lib/postrun

%post root
test -x $PKG_INSTALL_ROOT/usr/lib/postrun || exit 0
( echo 'test -x /usr/bin/gconftool-2 || {';
  echo '  echo "ERROR: gconftool-2 not found"';
  echo '  exit 0';
  echo '}';
  echo 'umask 0022';
  echo 'GCONF_CONFIG_SOURCE=xml:merged:/etc/gconf/gconf.xml.defaults';
  echo 'export GCONF_CONFIG_SOURCE';
  echo '/usr/bin/gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/*.schemas'
) | $PKG_INSTALL_ROOT/usr/lib/postrun

%preun root
test -x $PKG_INSTALL_ROOT/usr/lib/postrun || exit 0
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
  echo 'schemas="$SDIR/gnome-sync.schemas"';
  echo '$PKG_INSTALL_ROOT/usr/bin/gconftool-2 --makefile-uninstall-rule $schemas'
) | $PKG_INSTALL_ROOT/usr/lib/postrun


%files
%defattr (-, root, bin)
%{_bindir}
%{_libdir}/%{src_name}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/%{src_name}
%{_mandir}/man1/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/%{src_name}.desktop
%{_datadir}/applications/%{src_name}-prefs.desktop
%{_datadir}/dbus-1/services/org.guake.Guake.service
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/%{src_name} 

%files root
%defattr (0755, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/%{src_name}.schemas
%{_sysconfdir}/xdg/autostart/%{src_name}.desktop

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Wed Dec 01 2010 - Milan Jurik
- bump to 0.4.2
* Sun Jun 06 2010 - Milan Jurik
- Initial version
