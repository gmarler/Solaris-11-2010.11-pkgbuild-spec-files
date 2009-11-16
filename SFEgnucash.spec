#
# spec file for package SFEgnucash
#
# includes module(s): gnucash
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
# NOTE: You need build this spec with SS12, check 
# http://bugzilla.gnome.org/show_bug.cgi?id=548956 for detail.
#

%include Solaris.inc

%use gnucash = gnucash.spec
%use docs = gnucash-docs.spec

Name:               SFEgnucash
Summary:            gnucash - Financial-accounting software
Version:            %{gnucash.version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:           SUNWgnome-libs
# TODO: by default, this slib can not be found by gnucash
# build will fail on ./configure time with following error:
#  Cannot find SLIB.  Are you sure you have it installed?
#  See http://bugzilla.gnome.org/show_bug.cgi?id=347922
#  and http://bugzilla.gnome.org/show_bug.cgi?id=483631
# workaround is run following command as root:
# ln -s /usr/lib/slib /usr/share/guile/1.8/slib
# mkdir /usr/share/guile/site/
# guile -c "(use-modules (ice-9 slib)) (require 'new-catalog)"
Requires:           SUNWslib
Requires:           SUNWlibgoffice
Requires:           SUNWguile
BuildRequires:      SUNWgnome-libs-devel
BuildRequires:      SUNWlibgoffice-devel
BuildRequires:      SUNWperl-xml-parser
BuildRequires:      SUNWlxsl
BuildRequires:      SUNWswig

%package devel
Summary:            %{summary} - development files
SUNW_BaseDir:       %{_basedir}
%include default-depend.inc
Requires: %name

%if %build_l10n
%package l10n
Summary:            %{summary} - l10n files
SUNW_BaseDir:       %{_basedir}
%include default-depend.inc
Requires:           %{name}
%endif

%package root
Summary:            %{summary} - / filesystem
SUNW_BaseDir:       /
%include default-depend.inc
Requires:           SUNWpostrun-root
Requires:           SUNWgnome-config

%prep
rm -rf %name-%version
mkdir -p %name-%version
%gnucash.prep -d %name-%version
%docs.prep -d %name-%version


%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags"
%if %option_with_gnu_iconv
export CFLAGS="$CFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl"
%endif
export RPM_OPT_FLAGS="$CFLAGS"
%gnucash.build -d %name-%version
%docs.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gnucash.install -d %name-%version
%docs.install -d %name-%version

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/gnucash/??_??
rm -f $RPM_BUILD_ROOT%{_datadir}/omf/gnucash-docs/*-??_??.omf
%endif

# Remove /usr/share/info/dir, it's a generated file and shared by multiple
# packages
rm -f $RPM_BUILD_ROOT%{_datadir}/info/dir

# Remove /etc/gconf/gconf.xml.defaults, it is empty
rm -r $RPM_BUILD_ROOT%{_sysconfdir}/gconf/gconf.xml.defaults

%clean
rm -rf $RPM_BUILD_ROOT

%post
%include desktop-database-install.script
%include scrollkeeper-update.script
%include icon-cache.script

%postun
test -x $BASEDIR/lib/postrun || exit 0
%include desktop-database-uninstall.script
%include scrollkeeper-update.script
%include icon-cache.script

%post root
%include gconf-install.script

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
  echo 'schemas="$SDIR/apps_gnucash*.schemas"';
  echo '$PKG_INSTALL_ROOT/usr/bin/gconftool-2 --makefile-uninstall-rule $schemas'
) | $BASEDIR/var/lib/postrun/postrun -i -c JDS -a


%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libgnc*.so*
%{_libdir}/gnucash
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gnucash
%{_datadir}/info
%{_datadir}/xml
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/gnucash/C
%{_datadir}/omf/gnucash-docs/*-C.omf
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/*
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/*/apps
%{_datadir}/icons/hicolor/*/apps/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/gnucash/??_??
%{_datadir}/omf/gnucash-docs/*-??_??.omf
%endif

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/apps_gnucash*.schemas
%{_sysconfdir}/gnucash/*


%changelog
* Mon Nov 16 2009 - halton.huo@sun.com
- guile integrate into snv_125, use SUNWguile 
* Mon Oct 20 2008 - halton.huo@sun.com
- swig integrate into snv_100, rename SFEswig to SUNWswig
- slib integrate into snv_93, rename SFEslib to SUNWslib
* Mon Aug 18 2008 - nonsea@users.sourceforge.net
- Add BuildRequires: SUNWperl-xml-parser
* Wed Jun 25 2008 - nonsea@users.sourceforge.net
- Add gnucash-docs
* Wed Jun 25 2008 - nonsea@users.sourceforge.net
- Update %files
* Tue Jun 24 2008 - nonsea@users.sourceforge.net
- Add Requires:SFEgoffice BuildRequires:SFEgoffice-devel
* Tue Jun 24 2008 - nonsea@users.sourceforge.net
- Add BuildRequires SFEswig 
* Fri Jun 20 2008 - nonsea@users.sourceforge.net
- Move base part to gnucash.spec
- Add -root package
- Add %post and %postun for root
- Move .pc to -devel
- Add Requires/BuildRequires to SFEguile and SFEslib
* Mon Mar 10 2008 - nonsea@users.sourceforge.net
- Bump to 2.2.4
* Tue Sep 04 2007  - Thomas Wagner
- bump to 0.15.1, add %{version} to Download-Dir (might change again)
- conditional !%build_l10n rmdir $RPM_BUILD_ROOT/%{_datadir}/locale
* Sat May 26 2007  - Thomas Wagner
- bump to 0.15.0
- set compiler to gcc
- builds with Avahi, if present
* Thu Apr 06 2007  - Thomas Wagner
- Initial spec
