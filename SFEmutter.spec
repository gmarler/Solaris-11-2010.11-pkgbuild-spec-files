#
# spec file for package SFEmutter
#
# includes module(s): mutter
#
%include Solaris.inc

%define pythonver 2.6

Name:                    SFEmutter
Summary:                 Clutter enabled metacity window manager
Version:                 2.27.5
Source:	                 http://ftp.gnome.org/pub/GNOME/sources/mutter/2.27/mutter-%{version}.tar.bz2
Patch1:                  mutter-01-suncc-xc99.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:           SUNWPython26-devel
BuildRequires:           SUNWgnome-base-libs-devel
BuildRequires:           SUNWclutter-devel
BuildRequires:           SUNWgobject-introspection-devel
BuildRequires:           SUNWgir-repository
BuildRequires:           SFEgjs-devel
Requires:                SUNWPython26
Requires:                SUNWgnome-base-libs
Requires:                SUNWclutter
Requires:                SUNWgobject-introspection
Requires:                SUNWgir-repository
Requires:                SFEgjs
%include default-depend.inc

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir: %{_basedir}
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n mutter-%version
%patch1 -p1

%build
export CFLAGS="%optflags"
export PYTHON=/usr/bin/python%{pythonver}

libtoolize --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf
./configure \
   --prefix=%{_prefix} \
   --libexecdir=%{_libexecdir} \
   --mandir=%{_mandir} \
   --sysconfdir=%{_sysconfdir} \
   --with-clutter
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT/%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT/%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

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
  echo 'schemas="$SDIR/mutter.schemas"';
  echo '$PKG_INSTALL_ROOT/usr/bin/gconftool-2 --makefile-uninstall-rule $schemas'
) | $BASEDIR/var/lib/postrun/postrun -i -c JDS -a

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%{_libdir}/mutter
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/wm-properties
%{_datadir}/mutter
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%files root
%defattr(-, root, sys)
%attr(0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/mutter.schemas

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Wed Sep 16 2009 - Halton Huo <halton.huo@sun.com>
- Bump to 2.27.5.
* Sat Sep 05 2009 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 2.27.4.
* Sat Aug 29 2009 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 2.27.3.
* Tue Aug 04 2009 - Halton Huo <halton.huo@sun.com>
- Add patch suncc-xc99.diff to fix suncc build issue.
- Add patch solaris-shell.diff to fix bugzilla #590719.
* Mon Aug 03 2009 - Brian Cameron  <brian.cameron@sun.com>
- Update to build against 2.27.1 tarball.
* Tue Jul 07 2009 - Brian Cameron  <brian.cameron@sun.com>
- Remove upstream patch mutter-01-xopen-source.diff.
* Sat Apr 06 2009 - Brian Cameron  <brian.cameron@sun.com>
- Created.
