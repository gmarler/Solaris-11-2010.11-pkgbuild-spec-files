# 
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#

%include Solaris.inc

# Fixme:
# As root, ln -s /usr/lib/libdb.so.1 /usr/lib/libdb.so, it is build requirement;
# or, depend on package SUNWevolution-bdb-devel, which is in jds spec-files/closed
# now, use second way.
Name:           SFEanjuta
Version:        2.25.4
Summary:        GNOME IDE for C and C++
Group:          Development/Tools
License:        GPL
URL:            http://anjuta.org/
Source:         http://download.gnome.org/sources/anjuta/2.25/anjuta-%{version}.tar.bz2
# date:2007-05-14 owner:nonsea type:branding
Patch1:         anjuta-01-ld-z-text.diff
# date:2009-01-19 owner:halton type:bug bugzilla:567967
Patch2:         anjuta-02-suncc-empty-struct.diff
# date:2009-01-19 owner:halton type:bug bugzilla:568254
Patch3:         anjuta-03-extern-inline.diff

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWbash
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-config
Requires: SUNWgnome-devhelp
Requires: SUNWgnome-gtksourceview
Requires: SUNWgnome-libs
Requires: SUNWgnome-print
Requires: SUNWgnome-terminal
Requires: SUNWgnome-ui-designer
Requires: SUNWgnome-vfs
Requires: SUNWlibC
Requires: SUNWlibms
Requires: SUNWlxml
Requires: SUNWlxsl
Requires: SUNWperl584core
Requires: SUNWpcre
Requires: SUNWapch22u
Requires: SUNWgraphviz
Requires: SUNWsvn
Requires: SUNWneon
Requires: SFEgdl
Requires: SFElibgda
Requires: SFEautogen
BuildRequires: SFEgdl-devel
BuildRequires: SFElibgda-devel
BuildRequires: SFEautogen-devel
BuildRequires: SUNWgraphviz-devel
BuildRequires: SUNWevolution-bdb-devel


%description
Anjuta is a versatile Integrated Development Environment (IDE) for C and C++.
It has been written for GTK/GNOME, and features a number of advanced
programming facilities. It is basically a GUI interface for the collection
of command line programming utilities and tools available for the GNU system.
These are usually run via a text console, and can be unfriendly to use.

This package includes anjuta_create_global_tags.sh, which will allow you to
create an up to date, local system.tags.

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SUNWpostrun-root
Requires: SUNWgnome-config

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
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
%setup -q -n anjuta-%{version}
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

# FIXME: delete -I/usr/incldue/pcre when bug 6654493 is fixed.
export CFLAGS="%optflags -I/usr/include/pcre"
export LDFLAGS="%_ldflags"
export ACLOCAL_FLAGS="-I ."

#glib-gettextize -f
libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf
./configure --prefix=%{_prefix}					\
	--mandir=%{_mandir}					\
	--libdir=%{_libdir}					\
	--includedir=%{_includedir}				\
	--sysconfdir=%{_sysconfdir}				\
	--with-svn-include=%{_includedir}/svn			\
	--with-svn-lib=%{_libdir}/svn				\
	--disable-scrollkeeper					\
	--with-apr-config=%{_prefix}/apache2/2.2/bin/apr-1-config \
	--with-apu-config=%{_prefix}/apache2/2.2/bin/apu-1-config \
	%gtk_doc_option

%patch1 -p1

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%if %{!?_without_gtk_doc:0}%{?_without_gtk_doc:1}
rm -rf $RPM_BUILD_ROOT%{_datadir}/gtk-doc
%endif

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

# generated in the postinstall scripts (update-mime-database)
rm -rf $RPM_BUILD_ROOT%{_datadir}/mime

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS
( touch %{_datadir}/icons/hicolor || :
  touch %{_datadir}/icons/gnome || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/gnome || :
  fi
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%postun
test -x $BASEDIR/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS
( echo 'test -x %{_bindir}/update-mime-database || exit 0';
  echo '%{_bindir}/update-mime-database %{_datadir}/mime'
) | $BASEDIR/lib/postrun -b -u -c JDS
( echo 'test -x /usr/bin/scrollkeeper-update || exit 0';
  echo '/usr/bin/scrollkeeper-update'
) | $BASEDIR/lib/postrun -b -u -c JDS
( touch %{_datadir}/icons/hicolor  || :
  touch %{_datadir}/icons/gnome || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
	%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/gnome || :
  fi
) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u

%post root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo 'test -x /usr/bin/gconftool-2 || {';
  echo '  echo "ERROR: gconftool-2 not found"';
  echo '  exit 1';
  echo '}';
  echo 'umask 0022';
  echo 'GCONF_CONFIG_SOURCE=xml:merged:/etc/gconf/gconf.xml.defaults';
  echo 'export GCONF_CONFIG_SOURCE';
  echo '/usr/bin/gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/*.schemas > /dev/null'
) | $BASEDIR/var/lib/postrun/postrun -u -c JDS_wait

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
  echo 'schemas="$SDIR/anjuta-*.schemas "';
  echo '$PKG_INSTALL_ROOT/usr/bin/gconftool-2 --makefile-uninstall-rule $schemas'
) | $BASEDIR/var/lib/postrun/postrun -i -c JDS -a

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/anjuta
%{_libdir}/glade3
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/anjuta
%{_datadir}/glade3
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/anjuta*
%{_datadir}/omf/anjuta*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/anjuta*
%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/gnome
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/48x48/apps/*.png
%dir %attr (-, root, other) %{_datadir}/icons/gnome/48x48
%dir %attr (-, root, other) %{_datadir}/icons/gnome/48x48/mimetypes
%{_datadir}/icons/gnome/48x48/mimetypes/*.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable/apps
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%dir %attr (-, root, other) %{_datadir}/icons/gnome/scalable
%dir %attr (-, root, other) %{_datadir}/icons/gnome/scalable/mimetypes
%{_datadir}/icons/gnome/scalable/mimetypes/*.svg
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/*.schemas

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%if %{!?_without_gtk_doc:1}%{?_without_gtk_doc:0}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc
%endif

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sun Jan 18 2009 - halton.huo@sun.com
- Bump to 2.25.4
- Remove gnome-build since it is in anjuta's code base
- Add patch suncc-empty-struct.diff to fix bugzilla #567967
- Add patch extern-inline.diff to fix bugzilla #568254
* Tue Sep 02 2008 - halton.huo@sun.com
- Bump to 2.23.91
- Remove upstreamed patch zero-array.diff and miss-vala-sgml.diff
- Add /usr/share/aclocal to ACLOCAL_FLAGS to fix build issue
* Wed Aug 20 2008 - nonsea@users.sourceforge.net
- Bump to 2.5.90
- Use SUNWgraphviz instead of SFEgraphviz
- Add patch zero-array.diff to fix bugzilla #548622
- Add patch miss-vala-sgml.diff to fix bugzilla #548629
- Remove upstreamed patches max-baud.diff and lsocket.diff
* Sat Jun 14 2008 - andras.barna@gmail.com
- $CPUS calculated, but not used
- Fix apr-1-config's path, add apu-1-config, so at least it builds
* Tue Jan 03 2008 - nonsea@users.sourceforge.net
- Bump to 2.5.0
- Add patch max-baud.diff and lsocket.diff
* Tue Apr 22 2008 - nonsea@users.sourceforge.net
- Bump to 2.4.1.
* Tue Mar 10 2008 - nonsea@users.sourceforge.net
- Bump to 2.4.0.
* Mon Mar 03 2008 - nonsea@users.sourceforge.net
- Bump to 2.3.5.
* Mon Feb 18 2008 - nonsea@users.sourceforge.net
- Bump to 2.3.4.
* Fri Nov 02 2007 - nonsea@users.sourceforge.net
- Bump to 2.3.2
- Add new package l10n.
- Add _without_gtk_doc control
* Fri Nov 02 2007 - nonsea@users.sourceforge.net
- Bump to 2.3.0
- Remove SUNWpcre-devel from BuildRequires
* Tue Sep 11 2007 - nonsea@users.sourceforge.net
- Bump to 2.2.1
* Sat Jun 30 2007 - nonsea@users.sourceforge.net
- Bump to 2.2.0
* Sun May 13 2007 - nonsea@users.sourceforge.net
- Bump to 2.1.3
- Remove upstreamed patch and reorder.
- Add patch ld-z-text.diff.
- Add BuildRequires SUNWevolution-bdb-devel
* Sat Apr 20 2007 - dougs@truemail.co.th
- Added Required: SUNWsvn, and modified patch solaris-11-svn.diff
* Fri Apr 06 2007 - nonsea@users.sourceforge.net
  Enable subversion support:
- Add require SUNWapch2u and SUNWneon.
- Add patch solaris-svn.diff.
- Add --with-svn-include --with-svn-lib --with-apr-config
  for ./configure.
* Wed Apr 04 2007 - nonsea@users.sourceforge.net
- Add patch solaris-grep.diff for using /usr/xpg4/bin/grep 
  instead /usr/bin/grep for -e option.
* Wed Apr 04 2007 - nonsea@users.sourceforge.net
- Add patch share-glue.diff.
* Thu Mar 28 2007 - nonsea@users.sourceforge.net
- Bump to 2.1.2
- Remove patch upstreamed anjuta-01-wall.diff and reorder.
* Thu Mar 28 2007 - nonsea@users.sourceforge.net
- Reorganize patches
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Initial spec
