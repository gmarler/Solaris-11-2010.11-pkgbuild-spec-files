#
# spec file for package SFEbluegriffon
#
# includes module(s): bluegriffon
#
# Owner: alfred
#

%include Solaris.inc

Name:          SFEbluegriffon
Summary:       The next-generation Web Editor.
Version:       20090212
Source:        http://ftp.mozilla.org/pub/mozilla.org/firefox/releases/3.0.6/source/firefox-3.0.6-source.tar.bz2
Source1:       http://release.mozilla.com/sun/source/bluegriffon-%{version}-source.tar.bz2

# owner:alfred date:2009-02-13 type:bug
Patch1:        bluegriffon-01-base-jar-mn.diff

# default: not with Mozilla's nss/nspr libs, but the system ones.
%define without_moz_nss_nspr %{?_without_moz_nss_nspr:0}%{?!_without_moz_nss_nspr:1}

URL:           http://bluegriffon.org
SUNW_BaseDir:  %{_basedir}
BuildRoot:     %{_tmppath}/%{name}-%{version}-build

#####################################
##  Package Requirements Section   ##
#####################################

%include default-depend.inc
Requires: SUNWgnome-base-libs
Requires: SUNWfontconfig
Requires: SUNWfreetype2
Requires: SUNWgnome-config
Requires: SUNWgnome-libs
Requires: SUNWgnome-vfs
Requires: SUNWlibC
Requires: SUNWlibms
Requires: SUNWlibmsr
Requires: SUNWsqlite3
Requires: SUNWjpg
Requires: SUNWpng
Requires: SUNWmlib
Requires: SUNWzlib
%if %without_moz_nss_nspr
Requires: SUNWpr
%endif

BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWbzip
BuildRequires: SUNWgtar

%description
The next-generation Web Editor based on the rendering engine of Firefox.

%prep
%setup -q -n %name-%version -c -a1

mv bluegriffon mozilla

%patch1 -p0

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

# Build the vendor library (taglib)
LDFLAGS="-norunpath -z ignore -R'\$\$ORIGIN:\$\$ORIGIN/..'"
%if %without_moz_nss_nspr
#FIXME: update this after the system nss/nspr libraries are upgraded.
LDFLAGS="$LDFLAGS -R%{_libdir}/firefox"
%endif
export LDFLAGS

export CFLAGS="-xlibmil"
export CXXFLAGS="-xlibmil -xlibmopt -features=tmplife -lCrun -lCstd"
%ifarch sparc
export CFLAGS="$CFLAGS -xO5"
export CXXFLAGS="$CXXFLAGS -xO5"
%else
export CFLAGS="$CFLAGS -xO4"
export CXXFLAGS="$CXXFLAGS -xO4"
%endif

cd mozilla
# Build bluegriffon
cat << "EOF" > .mozconfig
mk_add_options MOZ_BUILD_PROJECTS="bluegriffon"
mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/../bluegriffon

ac_add_options --disable-tests
ac_add_options --enable-dtrace
ac_add_options --enable-xinerama
ac_add_options --with-system-jpeg
ac_add_options --disable-javaxpcom
ac_add_options --enable-system-cairo
ac_add_options --disable-crashreporter
ac_add_options --enable-jemalloc
ac_add_options --disable-auto-deps

#ac_add_app_options xulrunner --enable-application=xulrunner
#ac_add_app_options xulrunner --disable-installer

ac_add_app_options prism --enable-application=bluegriffon
ac_add_app_options prism --with-libxul-sdk=../xulrunner/dist
EOF

make -f client.mk build

# Package XULRunner
cd ../bluegriffon/bluegriffon/bluegriffon/installer

make

%install
rm -rf $RPM_BUILD_ROOT

cd %{_builddir}/%name-%version/bluegriffon/bluegriffon/dist
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
#mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
cp -R bluegriffon $RPM_BUILD_ROOT%{_libdir}/bluegriffon
cp bin/run-mozilla.sh $RPM_BUILD_ROOT%{_libdir}/bluegriffon/

#rm -rf $RPM_BUILD_ROOT%{_libdir}/bluegriffon/xulrunner
#ln -s /usr/lib/songbird/xulrunner $RPM_BUILD_ROOT%{_libdir}/bluegriffon/

#cp $RPM_BUILD_ROOT%{_libdir}/bluegriffon/chrome/icons/default/install-shortcut48.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/bluegriffon.png
ln -s %{_libdir}/bluegriffon/bluegriffon $RPM_BUILD_ROOT%{_bindir}/bluegriffon

# Don't deliver nss, nspr libraries on OpenSolaris
%if %without_moz_nss_nspr
rm -rf $RPM_BUILD_ROOT%{_libdir}/bluegriffon/libfreebl*
rm -rf $RPM_BUILD_ROOT%{_libdir}/bluegriffon/libnss*
rm -rf $RPM_BUILD_ROOT%{_libdir}/bluegriffon/libnspr*
rm -rf $RPM_BUILD_ROOT%{_libdir}/bluegriffon/libpl*
rm -rf $RPM_BUILD_ROOT%{_libdir}/bluegriffon/libs*
ln -s ../../firefox/libnssckbi.so $RPM_BUILD_ROOT%{_libdir}/bluegriffon/
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/bluegriffon
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/bluegriffon
#%dir %attr (0755, root, sys) %{_datadir}
#%dir %attr (0755, root, other) %{_datadir}/pixmaps
#%{_datadir}/pixmaps/bluegriffon.png

%changelog
* Mon Feb 16 2009 - alfred.peng@sun.com
- created
