#
# spec file for package SFEsongbird
#
# includes module(s): songbird
#
# Owner: alfred
#

%include Solaris.inc

# use --with-debug to enable debug build.
# default: non-debug build
%define with_debug %{?_with_debug:1}%{?!_with_debug:0}

# use --without-vendor-binary to build your own XULRunner/zlib/taglib.
# default: build with vendor binary
%define without_vendor_binary %{?_without_vendor_binary:1}%{?!_without_vendor_binary:0}

%if %with_debug
%define build_type debug
%else
%define build_type release
%endif

%ifarch sparc
%define arch sparc
%else
%define arch i386
%endif

Name:          SFEsongbird
Summary:       The desktop media player mashed-up with the Web.
Version:       0.6
Source:        http://releases.mozilla.com/sun/songbird-%{version}-source.tar.bz2
%if %without_vendor_binary
Source1:       http://releases.mozilla.com/sun/xulrunner-3.0rc1-source-patched-for-songbird.tar.bz2
%else
%if %with_debug
Source1:       http://releases.mozilla.com/sun/solaris-vendor-binaries/songbird-vendor-binary-solaris-%{arch}-firefox30rc1tag-debug.tar.bz2
%else
Source1:       http://releases.mozilla.com/sun/solaris-vendor-binaries/songbird-vendor-binary-solaris-%{arch}-firefox30rc1tag.tar.bz2
%endif
%endif
Patch1:        songbird-01-menu-item.diff
Patch2:        songbird-02-taglib.diff
URL:           http://www.songbirdnest.com/
SUNW_BaseDir:  %{_basedir}
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWbzip
BuildRequires: SUNWgtar
BuildRequires: SFEgawk
BuildRequires: SFEcmake

%description
Songbird provides a public playground for Web media mash-ups by providing developers with both desktop and Web APIs, developer resources and fostering Open Web media standards.

%prep
%setup -q -n %name-%version -c -a1
cd songbird%version
%patch1 -p1
%patch2 -p0
%if %without_vendor_binary
%else
mv ../solaris-%{arch} dependencies/
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif

# Build the vendor libraries(zlib, taglib)
cd songbird%version/dependencies/vendor/zlib
./songbird_zlib_make.sh
cd ../taglib/
./songbird_taglib_make.sh
cd ../../../../

export LDFLAGS="-z ignore -L%{_libdir} -L/usr/sfw/lib -R'\$\$ORIGIN:\$\$ORIGIN/..' -R%{_libdir}/mps"
export CFLAGS="-xlibmil"
export CXXFLAGS="-norunpath -xlibmil -xlibmopt -features=tmplife -lCrun -lCstd"
%if %with_debug
%else
%ifarch sparc
export CFLAGS="$CFLAGS -xO5"
export CXXFLAGS="$CXXFLAGS -xO5"
%else
export CFLAGS="$CFLAGS -xO4"
export CXXFLAGS="$CXXFLAGS -xO4"
%endif
%endif

%if %without_vendor_binary
cd mozilla
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
ac_add_options --with-xulrunner-stub-name=songbird
%if %with_debug
ac_add_options --enable-debug
ac_add_options --disable-optimize
%else
ac_add_options --enable-optimize
ac_add_options --disable-debug
%endif
ac_add_options --disable-tests
ac_add_options --disable-auto-deps
ac_add_options --disable-crashreporter
ac_add_options --disable-javaxpcom
ac_add_options --disable-updater
ac_add_options --disable-installer
ac_add_options --enable-extensions=default,inspector,venkman
ac_add_options --disable-dbus

mk_add_options BUILD_OFFICIAL=1
mk_add_options MOZILLA_OFFICIAL=1
mk_add_options MOZ_DEBUG_SYMBOLS=1
EOF

mkdir -p compiled/xulrunner

make -f client.mk build_all

# Package XULRunner
cd ../songbird%version

mkdir -p dependencies/solaris-i386/mozilla/%build_type
mkdir -p dependencies/solaris-i386/xulrunner/%build_type

cd tools/scripts
./make-mozilla-sdk.sh ../../../mozilla ../../../mozilla/compiled/xulrunner ../../dependencies/solaris-i386/mozilla/%build_type
./make-xulrunner-tarball.sh ../../../mozilla/compiled/xulrunner/dist/bin ../../dependencies/solaris-i386/xulrunner/%build_type xulrunner.tar.gz

cd ../../
%else
cd songbird%version
%endif

# Build Songbird
%if %with_debug
%else
export SB_ENABLE_INSTALLER=1
export SONGBIRD_OFFICIAL=1
%endif

export SB_ENABLE_JARS=1
export LD=CC
export PATH=/usr/gnu/bin:$PATH

%if %with_debug
make -f songbird.mk debug
%else
make -f songbird.mk
%endif

%install
rm -rf $RPM_BUILD_ROOT

cd %{_builddir}/%name-%version/songbird%version/compiled
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cp -R dist $RPM_BUILD_ROOT%{_libdir}/songbird-%version
cp ../app/branding/icon64.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/songbird.png
cp ../app/branding/songbird.desktop $RPM_BUILD_ROOT%{_datadir}/applications
ln -s ../lib/songbird-%version/songbird $RPM_BUILD_ROOT%{_bindir}/songbird

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/songbird
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/songbird-%{version}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/songbird.desktop
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/songbird.png

%changelog
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
