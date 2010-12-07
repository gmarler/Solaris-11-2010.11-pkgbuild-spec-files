#
# spec file for package SFEsongbird
#
# includes module(s): songbird
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define OSR 10735:1.x

%if %option_with_debug
%define build_type debug
%else
%define build_type release
%endif

Name:          SFEsongbird
IPS_package_name: desktop/media-player/songbird
Meta(info.classification): %{classification_prefix}:Applications/Sound and Video
Summary:       The desktop media player mashed-up with the Web.
Version:       1.4.3
Vendor:        getsongbird.com
Source:        http://download.songbirdnest.com/source/Songbird%{version}-1438.tar.bz2
Source1:       http://download.songbirdnest.com/source/Songbird%{version}-1438-vendor.tar.bz2
Source2:       nspr-nss-config

# date:2009-03-31 type:branding
# The patch will be removed when the apache C++ standard library is integrated.
Patch1:        songbird-01-cpp-template.diff
# date:2008-07-16 type:bug
# bugzilla.songbirdnest.com 7800. The patch was backed out as it breaks Windows build.
Patch2:        songbird-02-taglib.diff
# date:2008-06-25 type:bug
# bugzilla.mozilla.org 440714
Patch3:        songbird-03-remap-pixman-functions.diff
# date:2009-01-07 type:branding
Patch4:        songbird-04-startup-script.diff
# date:2009-03-31 type:bug
# bugzilla.songbirdnest.com 16898
Patch5:        songbird-05-build.diff
# date:2008-09-08 type:bug
# bugster:6724471 bugzilla:451007
Patch6: songbird-06-donot-delay-stopping-realplayer.diff
# ginnchen date:2009-01-15 type:bug
# bugzilla.mozilla.org 455670
Patch8: songbird-08-runpath.diff
# ginnchen date:2009-05-21 type:branding
Patch9: songbird-09-system-nss-nspr.diff
# date:2009-10-23 type:bug d.o.o 12202
Patch10: songbird-10-moz-nss-nspr.diff
# date:2009-10-23 type:bug d.o.o 12038
Patch11: songbird-11-use-sun-cc.diff
# date:2009-10-30 type:bug d.o.o 12317 
Patch12: songbird-12-using-bash.diff
# date:2010-01-11 type:bug 
Patch13: songbird-13-type-cast.diff
# date:2010-04-28 type:bug:bug d.o.o 15069
Patch14: songbird-14-check-readable-core.diff

URL:           http://www.songbirdnest.com/
SUNW_BaseDir:  %{_basedir}
License:       GPL v2.1/LGPL v2.1/Public Domain
BuildRoot:     %{_tmppath}/%{name}-%{version}-build

#####################################
##  Package Requirements Section   ##
#####################################

%include default-depend.inc
Requires: SUNWgtk2
Requires: SUNWfontconfig
Requires: SUNWfreetype2
Requires: SUNWgnome-config
Requires: SUNWgnome-libs
Requires: SUNWgnome-media
Requires: SUNWgnome-vfs
Requires: SUNWlibC
Requires: SUNWlibms
Requires: SUNWlibmsr
Requires: SUNWsqlite3
Requires: SUNWjpg
Requires: SUNWpng
Requires: SUNWmlib
Requires: SUNWzlib
Requires: SUNWpr
BuildRequires: SUNWgtk2-devel

# Songbird depends on Firefox's plugins.
Requires: SUNWfirefox

BuildRequires: SUNWgnome-media-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWbzip
BuildRequires: SUNWgtar
BuildRequires: SUNWcmake

%description
Songbird is a free software media player and web browser, designed to
catalyze and champion a diverse, open Media Web.

%prep
%setup -q -n %name-%version -c -a1

rm -rf Songbird%{version}/dependencies/vendor
mv Songbird%{version}-vendor Songbird%{version}/dependencies/vendor

mkdir -p build/checkout/solaris-%{base_arch}
mkdir -p build/solaris-%{base_arch}

cd Songbird%{version}
%patch1 -p1
%patch2 -p1
%patch4 -p1
%patch5 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1

cd dependencies/vendor/xulrunner/mozilla
%patch3 -p1
%patch6 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

# Build the vendor library (taglib)
export LDFLAGS="-norunpath"
cd Songbird%{version}/dependencies/vendor/taglib
export SB_VENDOR_BUILD_ROOT=%{_builddir}/%name-%version/build
/usr/gnu/bin/make -f Makefile.songbird %{build_type}
cd ../../../../

# Move compiled taglib into the dependecies area
cd build/solaris-%{base_arch}
mkdir ../../Songbird%{version}/dependencies/solaris-%{base_arch}
mv taglib ../../Songbird%{version}/dependencies/solaris-%{base_arch}
cd ../../Songbird%{version}

LDFLAGS="-norunpath -z ignore -R'\$\$ORIGIN:\$\$ORIGIN/..'"
export LDFLAGS

export CFLAGS="-xlibmil"
export CXXFLAGS="-D__FUNCTION__=__func__ -xlibmil -xlibmopt -features=tmplrefstatic -features=tmplife,extensions -lCrun -lCstd"
%if %option_with_debug
%else
%ifarch sparc
export CFLAGS="$CFLAGS -xO5"
export CXXFLAGS="$CXXFLAGS -xO5"
%else
export CFLAGS="$CFLAGS -xO4"
export CXXFLAGS="$CXXFLAGS -xO4"
%endif
%endif

cd dependencies/vendor/xulrunner/mozilla
# Build XULRunner
cat << "EOF" > .mozconfig
MOZILLA_OFFICIAL=1
export MOZILLA_OFFICIAL

BUILD_OFFICIAL=1
export BUILD_OFFICIAL

mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/compiled/xulrunner
ac_add_options --prefix=%{_prefix}
ac_add_options --libdir=%{_libdir}
ac_add_options --mandir=%{_mandir}
ac_add_options --enable-application=xulrunner
ac_add_options --with-xulrunner-stub-name=songbird-bin
%if %option_with_debug
ac_add_options --enable-debug
ac_add_options --disable-optimize
ac_add_options --enable-tests
%else
ac_add_options --enable-optimize
ac_add_options --disable-debug
ac_add_options --disable-tests
%endif
ac_add_options --disable-auto-deps
ac_add_options --disable-crashreporter
ac_add_options --disable-javaxpcom
ac_add_options --disable-updater
ac_add_options --enable-dtrace
ac_add_options --enable-system-cairo
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --enable-system-sqlite
ac_add_options --with-system-jpeg
ac_add_options --disable-installer
ac_add_options --enable-extensions=default,inspector,venkman
ac_add_options --enable-jemalloc

mk_add_options BUILD_OFFICIAL=1
mk_add_options MOZILLA_OFFICIAL=1
mk_add_options MOZ_DEBUG_SYMBOLS=1
EOF

mkdir -p compiled/xulrunner

cp %{SOURCE2} compiled/xulrunner
chmod +x compiled/xulrunner/nspr-nss-config
export NSPR_CONFIG=$PWD/compiled/xulrunner/nspr-nss-config\ nspr
export NSS_CONFIG=$PWD/compiled/xulrunner/nspr-nss-config\ nss

make -f client.mk build_all

# Package XULRunner
cd ../../../..

mkdir -p dependencies/solaris-%{base_arch}/mozilla/%build_type
mkdir -p dependencies/solaris-%{base_arch}/xulrunner/%build_type

cd tools/scripts
chmod +x make-mozilla-sdk.sh
chmod +x make-xulrunner-tarball.sh
./make-mozilla-sdk.sh ../../dependencies/vendor/xulrunner/mozilla ../../dependencies/vendor/xulrunner/mozilla/compiled/xulrunner ../../dependencies/solaris-%{base_arch}/mozilla/%build_type
./make-xulrunner-tarball.sh ../../dependencies/vendor/xulrunner/mozilla/compiled/xulrunner/dist/bin ../../dependencies/solaris-%{base_arch}/xulrunner/%build_type xulrunner.tar.gz

cd ../../
echo ac_add_options --with-media-core=gstreamer-system > songbird.config
echo ac_add_options --enable-breakpad=no >> songbird.config

export SB_ENABLE_MOZBROWSER_CHECK=
export SB_DISABLE_DEPENDENT_PKG_MGMT=1
export SB_DISABLE_PKG_AUTODEPS=1

# Build Songbird
%if %option_with_debug
%else
export SB_ENABLE_INSTALLER=1
export SONGBIRD_OFFICIAL=1
%endif

export LDFLAGS="$LDFLAGS -R'\$\$ORIGIN/../xulrunner'"

export CFLAGS="$CFLAGS -I%{_includedir}/mps"
export CXXFLAGS="$CXXFLAGS -I%{_includedir}/mps"
export LDFLAGS="$LDFLAGS -L%{_libdir}/mps -R%{_libdir}/mps"

export SB_ENABLE_JARS=1
export LD=CC
export PATH=/usr/gnu/bin:$PATH

%if %option_with_debug
make -f songbird.mk debug
cp ./app/branding/songbird-512.png compiled/dist
%else
make -f songbird.mk
%endif

%install
rm -rf $RPM_BUILD_ROOT

cd %{_builddir}/%name-%version/Songbird%{version}/compiled
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cp -R dist $RPM_BUILD_ROOT%{_libdir}/songbird

# Remove unnecessary libraries/tools
rm -f $RPM_BUILD_ROOT%{_libdir}/xulrunner/libjemalloc.so
rm -f $RPM_BUILD_ROOT%{_libdir}/xulrunner/mangle
rm -f $RPM_BUILD_ROOT%{_libdir}/xulrunner/mozilla-xremote-client
rm -f $RPM_BUILD_ROOT%{_libdir}/xulrunner/nsinstall
rm -f $RPM_BUILD_ROOT%{_libdir}/xulrunner/regxpcom
rm -f $RPM_BUILD_ROOT%{_libdir}/xulrunner/shlibsign
rm -f $RPM_BUILD_ROOT%{_libdir}/xulrunner/ssltunnel
rm -f $RPM_BUILD_ROOT%{_libdir}/xulrunner/updater.ini
rm -f $RPM_BUILD_ROOT%{_libdir}/xulrunner/xp*
rm -f $RPM_BUILD_ROOT%{_libdir}/xulrunner/xulrunner*
rm -rf $RPM_BUILD_ROOT%{_libdir}/xulrunner/plugins

# Make use of Firefox's plugins
rmdir $RPM_BUILD_ROOT%{_libdir}/songbird/plugins
ln -s ../firefox/plugins $RPM_BUILD_ROOT%{_libdir}/songbird/

mv $RPM_BUILD_ROOT%{_libdir}/songbird/songbird-512.png $RPM_BUILD_ROOT%{_datadir}/pixmaps
mv $RPM_BUILD_ROOT%{_libdir}/songbird/songbird.desktop $RPM_BUILD_ROOT%{_datadir}/applications
ln -s ../lib/songbird/songbird $RPM_BUILD_ROOT%{_bindir}/songbird

#install man page
rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/Songbird%{version}/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%doc(bzip2) -d Songbird%{version} LICENSE
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/songbird
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/songbird
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/songbird.desktop
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*.png
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Tue Dec 07 2010 - brian.cameron@oracle.com
- Migrated to SFE.
* Wen Apl 28 2010 - yuntong.jin@sun.com
- Add patch songbird-14-check-readable-core.diff to fix d.0.0:15069
* Fri Oct 30 2009 - brian.lu@sun.com
- Add patch songbird-12-using-bash.diff
* Fri Oct 23 2009 - brian.lu@sun.com
- Add patch songbird-10-moz-nss-nspr.diff and songbird-11-use-sun-cc.diff 
* Fri Aug 28 2009 - yuntong.jin@sun.com
- Change owner to jouby
* Thu Jul 30 2009 - alfred.peng@sun.com
- Fix for packaging (songbird-512.png).
* Mon Jul 27 2009 - alfred.peng@sun.com
- Use GNU make to build the vendor library and enable system sqlite.
  Fix d.o.o bug #10284 for the missing image.
* Wed Jul 01 2009 - alfred.peng@sun.com
- Update to include $ORIGIN/../xulrunner to Songbird runtime path.
* Tue Jun 23 2009 - alfred.peng@sun.com
- Bump to 1.2.0. Rework build.diff to fix the 1.2.0 build failure.
* Tue Jun 02 2009 - alfred.peng@sun.com
- Bump to 1.1.2.
  Use system NSS NSPR libraries by default (from firefox.spec by Ginn Chen).
  Remove patch system-sqlite.diff and wait for the system sqlite to upgrade.
  Add patch xulrunner-elif.diff for bugzilla #478843.
* Tue Mar 31 2009 - alfred.peng@sun.com
- Bump to 1.1.1 and fix bugster CR#6819948.
  Remove patches: songbird-01-taglib-build.diff, songbird-05-1.0.0-build.diff.
  Add patches: songbird-01-cpp-template.diff, songbird-05-1.0.0-build.diff.
* Thu Jan 15 2009 - alfred.peng@sun.com
- Fix the RPATH and RUNPATH for XULRunner.
  bugster bug: 6786843. 
* Wed Jan 07 2009 - alfred.peng@sun.com
- Bump to 1.0.0.
  Update source tarball links and depend on SUNWcmake.
  Enable system cairo and sqlite, build taglib with the new build script.
  Remove patches: menu-item.diff, system-zlib-for-taglib.diff and
  build-system.diff. Add patches: taglib-build.diff, startup-script.diff,
  1.0.0-build.diff and system-sqlite.diff.
  Create link to Firefox's plugins directory to share all the plugins.
  Fix certificate authority issue. d.o.o bugzilla #4576.
* Fri Sep 19 2008 - alfred.peng@sun.com
- Add option to LDFLAGS to avoid redundant RPATH and RUNPATH.
  bugster bug: 6748456.
* Fri Sep 12 2008 - alfred.peng@sun.com
- Add %doc to %files for new copyright.
* Mon Sep 08 2008 - alfred.peng@sun.com
- remove unnecessary patch songbird-06-no-nss-nspr.diff.
  copy ginn's gecko patch songbird-06-donot-delay-stopping-realplayer.diff
  from Firefox to fix realplayer plugin issue.
* Mon Sep 08 2008 - alfred.peng@sun.com
- add patch songbird-06-no-nss-nspr.diff to make Songbird use Firefox's
  nss/nspr.
* Fri Aug 22 2008 - alfred.peng@sun.com
- bump to 0.7.0.
  add new patch songbird-05-build-system.diff.
  update patch songbird-03-remap-pixman-functions.diff.
* Wed Aug 20 2008 - alfred.peng@sun.com
- add new manpage into the package.
  replace %debug_build with pre-defined %option_with_debug.
  sync songbird-01-menu-item.diff with the up-streamed one.
* Mon Aug 11 2008 - alfred.peng@sun.com
- update the link to source tarball.
  add the placeholder for Songbird's copyright.
* Sat Jul 26 2008 - alfred.peng@sun.com
- bump to 0.6.1.
  add Package Requirements Section.
  add patch songbird-03-remap-pixman-functions.diff to fix songbird crash.
  add patch songbird-04-system-zlib-for-taglib.diff to build taglib with
  system zlib.
* Wed Jun 18 2008 - trisk@acm.jhu.edu
- Merge with alfred's SFEsongbird-06.spec (yay 0.6)
* Fri May 09 2008 - stevel@opensolaris.org
- cmake is needed for building taglib
- gawk is needed for building Songbird
* Mon Apr 21 2008 - alfred.peng@sun.com
- add support for SPARC platform.
* Sun Apr 13 2008 - alfred.peng@sun.com
- add option --without-vendor-binary. use the vendor binary by default
  to speed the build process.
* Thu Apr 10 2008 - alfred.peng@sun.com
- created

