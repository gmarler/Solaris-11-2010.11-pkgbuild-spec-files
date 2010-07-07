# spec file for package SUNWlibggz
#
# includes module(s): libggz, ggz-client-libs
#
# Copyright 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%define owner migi
#
%include Solaris.inc

%define makeinstall make install DESTDIR=$RPM_BUILD_ROOT
%use libggz = libggz.spec
%use ggz_client_libs = ggz-client-libs.spec

Name:                    SUNWlibggz
IPS_package_name:        games/libggz
Meta(info.classification): %{classification_prefix}:Applications/Games
Summary:                 GGZ Gaming Zone
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SUNWgtk2-devel
BuildRequires: SUNWlibrsvg-devel
BuildRequires: SUNWPython26-devel
BuildRequires: SUNWpython26-setuptools
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWlibsdl-devel
BuildRequires: SUNWgnome-media-devel
Requires: SUNWgtk2
Requires: SUNWgnome-libs
Requires: SUNWgnome-config
Requires: SUNWlibms
Requires: SUNWlibrsvg
Requires: SUNWPython26
Requires: SUNWdesktop-cache
Requires: SUNWgnome-media
Requires: %{name}-root

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%prep
rm -rf %name-%version
mkdir %name-%version
%libggz.prep -d %name-%version
%ggz_client_libs.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
%define libggz_build_dir %{_builddir}/%name-%version/libggz-%{libggz.version}
%define ggzclient_build_dir %{_builddir}/%name-%version/ggz-client-libs-%{ggz_client_libs.version}

export PKG_CONFIG_PATH=%{_pkg_config_path}:/usr/lib/python%{default_python_version}/pkgconfig
export CFLAGS="%optflags -I%{_includedir} -I/usr/sfw/include -xc99 -I%{libggz_build_dir}/src -I%{ggzclient_build_dir}/ggzmod -I%{ggzclient_build_dir}/ggzcore"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags -lX11 -L/usr/sfw/lib -lexpat -L%{libggz_build_dir}/src/.libs -L%{ggzclient_build_dir}/ggzmod/.libs -L%{ggzclient_build_dir}/ggzcore/.libs"
export LD_LIBRARY_PATH="%{libggz_build_dir}/src/.libs:%{ggzclient_build_dir}/ggzmod/.libs:%{ggzclient_build_dir}/ggzcore/.libs"
export PATH="$PATH:"`dirname $CXX`
export CXX=`basename $CXX`
export ACLOCAL_FLAGS="-I%{_datadir}/aclocal"

# find GNU xgettext
IFS=:
for dir in $PATH; do
  test -x "$dir/xgettext" && \
       "$dir/xgettext" --version 2>&1 | egrep -s 'GNU gettext' && \
       XGETTEXT="$dir/xgettext"
done
export XGETTEXT

%libggz.build -d %name-%version
%ggz_client_libs.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_mandir}
%libggz.install -d %name-%version
%ggz_client_libs.install -d %name-%version

# Delete the include files as we're not delivering a devel package. It's not
# useful.
#rm -rf $RPM_BUILD_ROOT%{_includedir}
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%if %build_l10n
%else
# REMOVE l10n FILES*files-list*
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/[a-z]*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z][a-z].omf
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z][a-z]_[A-Z][A-Z].omf
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*latin.omf
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):unsupported" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc libggz-%{libggz.version}/AUTHORS
%doc libggz-%{libggz.version}/README
%doc libggz-%{libggz.version}/README.GGZ
%doc libggz-%{libggz.version}/COPYING
%doc(bzip2) libggz-%{libggz.version}/ChangeLog
%doc(bzip2) libggz-%{libggz.version}/NEWS
%doc ggz-client-libs-%{ggz_client_libs.version}/AUTHORS
%doc ggz-client-libs-%{ggz_client_libs.version}/README
%doc ggz-client-libs-%{ggz_client_libs.version}/README.GGZ
%doc ggz-client-libs-%{ggz_client_libs.version}/COPYING 
%doc(bzip2) ggz-client-libs-%{ggz_client_libs.version}/ChangeLog
%doc(bzip2) ggz-client-libs-%{ggz_client_libs.version}/NEWS

%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libggz*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/desktop-directories
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%dir %attr(0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/*
%dir %attr(0755, root, bin) %{_mandir}/man6
%{_mandir}/man6/*
%dir %attr(0755, root, bin) %{_mandir}/man7
%{_mandir}/man7/*


%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%attr (-, root, other) %{_datadir}/locale
%{_datadir}/gnome/help/[a-z]*/[a-z]*
%{_datadir}/omf/*/*-[a-z][a-z].omf
%{_datadir}/omf/*/*-[a-z][a-z][_@]*.omf
%endif

%files root
%defattr (-, root, sys)
%attr(0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/xdg

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Wed Jul 07 2010 - brian.cameron@oracle.com
- Convert into SFElibggz.spec file.
* Thu Apr 22 2010 - christian.kelly@oracle.com
- Fix %files.
* Mon Mar 22 2010 - christian.kelly@sun.com
- Add Requires: SUNWclutter-gtk.
* Sat Mar 14 2010 - christian.kelly@sun.com
- Add Requires: SUNWclutter.
* Mon Nov 02 2009 - Michal.Pryc@Sun.Com
- Move deos from Python2.4 to Python2.6.
* Mon Jul 27 2009 - christian.kelly@sun.com
- Minor changes to %files.
* Mon Jul 27 2009 - christian.kelly@sun.com
- Correct PKG_CONFIG_PATH again.
* Sun Jul 26 2009 - christian.kelly@sun.com
- Add path to PKG_CONFIG_PATH.
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Tue Mar 03 2009 - brian.cameron@sun.com
- Remove gnometris again.
* Wed Feb 18 2009 - dave.lin@sun.com
- Removed %doc gnome-games:same-gnome/help/ChangeLog po/ChangeLog which are n/a
  in 2.25.91.
* Thu Oct 02 2008 - brian.cameron@sun.com
- Add blackjack and gnometris back to gnome-games.
* Sat Sep 20 2008 - christian.kelly@sun.com
- Set perms on /usr/share/doc.
* Fri Jun 6 2008 - michal.pryc@sun.com
- Added additional manual pages: libggz, libggzmod, libggzcore
* Fri May 30 2008 - damien.carbery@sun.com
- Delete %{_sysconfdir}/ggz.modules in %install. It is only created by gnect
  game when it finds /usr/bin/ggz-config. This happens when the module is built
  but already installed, not on first build.
* Tue May 13 2008 - damien.carbery@sun.com
- Comment out %{_sysconfdir}/ggz.modules in %files as it's not being installed
  this week.
* Sun May 11 2008 - Michal.Pryc@Sun.Com
- Adjusted %files after enabling encryption for libggz 
* Mon Mar 24 2008 - patrick.ale@gmail.com
- Add %_datadir/gnome-games/sounds to the package list
* Wed Mar 19 2008 - damien.carbery@sun.com
- Add Build/Requires SUNWgnome-games/-devel as sounds require gstreamer.
* Fri Mar 14 2008 - damien.carbery@sun.com
- Remove 'sounds' dir from %files as it is not installed by 2.22 tarball.
* Sun Mar 09 2008 - damien.carbery@sun.com
- Fix perms for -devel package.
* Thu Mar 06 2008 - Michal.Pryc@Sun.Com
- Moved man packages for headers to the devel package.
* Thu Feb 28 2008 - brian.cameron@sun.com
- Remove ggz-python since it isn't needed.  Sorry about the churn.
* Wed Feb 27 2008 - brian.cameron@sun.com
- Add gst-python, since glchess needs it.  Rename %{ggzmod_build_dir} to
  %{ggzclient_build_dir} since this is more accurate - the module is named
  ggz_client_libs.  Also add the ggzcore library to LD_LIBRARY_PATH and
  LDFLAGS since this is needed by gst-python.
* Mon Feb 18 2008 - Michal.Pryc@Sun.Com
- Update %files for ggz-client-libs patch, which removes ggzwrap manpages 
* Fri Feb 15 2008 - damien.carbery@sun.com
- Update %files for new tarball.
* Tue Jan 29 2008 - damien.carbery@sun.com
- Remove empty %{_libdir}/ggz dir.
* Fri Jan 25 2008 - damien.carbery@sun.com
- Add BuildRequires SUNWlibsdl-devel so that the modified sdl.m4 will be
  available to configure.
* Sun Jan 20 2008 - patrick.ale@gmail.com
- Rework the XGETTEXT detection.
* Thu Jan 17 2008 - patrick.ale@gmail.com
- Add export XGETTEXT=`which` to pickup GNU getetxt shipped by CBE
* Wed Jan 09 2008 - damien.carbery@sun.com
- Set ACLOCAL_FLAGS to pick up modified intltool.m4.
* Mon Jan 07 2008 - damien.carbery@sun.com
- Update CFLAGS to find ggzcore.h. Update %files. Add devel package but don't
  enable it as it is probably not useful.
* Mon Jan 07 2008 - damien.carbery@sun.com
- Add variable to specify location of ggzmod sources (in ggz-client-libs) and
  add info to CFLAGS and LDFLAGS.
* Thu Jan  3 2008 - laca@sun.com
- use gconf-install.script instead of an inline script
* Wed Jan 02 2008 - damien.carbery@sun.com
- Add ggz-client-libs module.
- Add variable to specify location of libggz sources. Add info to CFLAGS and
  LDFLAGS.
* Tue Dec 18 2007 - damien.carbery@sun.com
- Add libggz module.
* Wed Nov 21 2007 - damien.carbery@sun.com
- Correct non-l10n build.
* Mon Jun 11 2007 - damien.carbery@sun.com
- Update %files to 2.19.6 tarball - add %{_datadir}/gnome-games/gnotski.
* Mon Jun 11 2007 - damien.carbery@sun.com
- Update %files to 2.19.3 tarball.
* Wed Jun 06 2007 - damien.carbery@sun.com
- Add $CXX dir to PATH so that configure can find it. Set $CXX to 'CC', again so
  configure can find it (via PATH).
* Fri Mar 23 2007 - damien.carbery@sun.com
- Add en_GB omf files to %files.
* Tue Feb 20 2007 - damien.carbery@sun.com
- Remove %if/%endif with_guile code as aisleriot is no longer built - it is
  excluded via a configure option in gnome-games.spec.
* Fri Feb 16 2007 - damien.carbery@sun.com
- Add Build/Requires SUNWgnome-python-desktop/-devel.
* Mon Feb 12 2007 - damien.carbery@sun.com
- aisleriot game is only built when SFEguile is installed. Use %if/%endif to 
  include its files only when SFEguile is installed.
* Sat Feb 10 2007 - damien.carbery@sun.com
- Add sol-games dir to %files and aisleriot.schemas to %files and %preun root.
* Sun Jan 28 2007 - laca@sun.com
- add -xc99 to CFLAGS
* Tue Jan 09 2007 - damien.carbery@sun.com
- Add glchess.schemas to %preun root and to %files.
* Thu Dec 07 2006 - damien.carbery@sun.com
- Add python libs dir and glchess/gnome-sudoku dirs.
* Fri Nov 24 2006 - damien.carbery@sun.com
- Remove empty %{_libdir}. Remove glchess and gnome-sudoku games as they were
  not installed.
* Wed Nov 22 2006 - damien.carbery@sun.com
- 2.17.1 changes - remove gataxx references; add glchess, gnome-sudoku and ggz
  games.
* Thu Nov 09 2006 - damien.carbery@sun.com
- Add BuildRequires SUNWgnome-vfs-devel as gnome-libs pc file requires
  gnome-vfs.
* Mon Aug 21 2006 - damien.carbery@sun.com
- Fix l10n package - C locale omf file was in base and l10n package.
* Thu Aug 17 2006 - damien.carbery@sun.com
- Change 'icons' line in %files to pick up files.
* Sat Aug 12 2006 - laca@sun.com
- delete some unnecessary env variables
* Sat Aug 12 2006 - laca@sun.com
- change datadir/icons permissions back to root:other since it's a stable
  interface and wasn't supposed to be changed
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Thu Jun 29 2006 - laca@sun.com
- update postrun scripts
* Mon Jun 26 2006 - laca@sun.com
- move back to /usr, part of CR 6412650
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Sat Jun 10 2006 - laca@sun.com
- delete -devel pkg: it was empty
* Thu May 25 2006 - laca@sun.com
- use post/preun scripts to install schemas into the merged gconf files
* Wed May 10 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Mon Feb 20 2006 - damien.carbery@sun.com
- Complete update of Build/Requires after running check-deps.pl script.
* Thu Feb 16 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Fri Jan 06 2006 - damien.carbery@sun.com
- Fix %files for updated file list.
* Sat Dec  3 2005 - laca@sun.com
- add %post script that runs update-desktop-database
* Tue Nov 29 2005 - laca@sun.com
- remove javahelp stuff
* Tue Sep 13 2005 - laca@sun.com
- Remove unpackaged files or add to %files
* Thu Jul 28 2005 - damien.carbery@sun.com
- Add SUNWlibrsvg-devel build dependency. Add SUNWlibrsvg runtime dependency.
* Tue May 24 2005 - brian.cameron@sun.com
- Bump to 2.10 and fix packaging.
* Mon Dec 13 2004 - damien.carbery@sun.com
- Move to /usr/sfw to implement ARC decision.
* Fri Nov 12 2004 - laca@sun.com
- move to /usr/demo/jds
* Tue Oct 05 2004 - matt.keenan@sun.com
- Added localized help to l10n package
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Mon Aug 23 2004 - laca@sun.com
- s/SUNWpl5u/SUNWperl584usr/
* Sat Jun 26 2004  shirley.woo@sun.com
- Changed install location to /usr/...
* Wed Jun  2 2004 - takao.fujiwara@sun.com
- Added %{_datadir}/locale to install l10n messages
* Thu May 27 2004 - damien.carbery@sun.com
- Comment out SUNWcspu lines. Will uncomment when Metropolis branch created.
* Wed May 26 2004 - damien.carbery@sun.com
- Add SUNWcspu (with libucb.so and scandir) to Requires and BuildRequires.
  configure was breaking because of its absense.
* Mon May 10 2004 - brian.cameron@sun.com
- Putting back %{_sysconfig}/gconf into packaging which got 
  accidently simplified away in Laca's last change.  Now the
  games work again.
* Tue Apr 20 2004 - laca@sun.com
- simlify %files
- add javahelp
* Thu Apr 08 2004 - laca@sun.com
- added missing %defattr
* Fri Mar 26 2004 - brian.cameron@sun.com
- Created,

