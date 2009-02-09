#
# spec file for package SFEprism
#
# includes module(s): prism
#
# Owner: alfred
#

%include Solaris.inc

Name:          SFEprism
Summary:       split the Web app to the desktop
Version:       0.9.1
Source:        http://ftp.mozilla.org/pub/mozilla.org/firefox/releases/3.0.5/source/firefox-3.0.5-source.tar.bz2
Source1:       http://release.mozilla.com/sun/prism/%{version}/source/prism-%{version}-source.tar.bz2

# default: not with Mozilla's nss/nspr libs, but the system ones.
%define without_moz_nss_nspr %{?_without_moz_nss_nspr:0}%{?!_without_moz_nss_nspr:1}

URL:           http://labs.mozilla.com/projects/prism/
SUNW_BaseDir:  %{_basedir}
BuildRoot:     %{_tmppath}/%{name}-%{version}-build

#####################################
##  Package Requirements Section   ##
#####################################

%include default-depend.inc
Requires: SUNWgnome-base-libs
Requires: SUNWsongbird
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
Prism (formerly, Webrunner) is a prototype application that lets users split
web applications out of their browser and run them directly on their desktop. 

%prep
%setup -q -n %name-%version -c -a1

mv prism mozilla

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
# Build XULRunner/Prism
cat << "EOF" > .mozconfig
mk_add_options MOZ_BUILD_PROJECTS="xulrunner prism"
mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/../prism

ac_add_options --disable-tests
ac_add_options --enable-dtrace
ac_add_options --enable-xinerama
ac_add_options --with-system-jpeg
ac_add_options --disable-javaxpcom
ac_add_options --enable-system-cairo
ac_add_options --disable-crashreporter
ac_add_options --disable-jemalloc
ac_add_options --disable-auto-deps

ac_add_app_options xulrunner --enable-application=xulrunner
ac_add_app_options xulrunner --disable-installer

ac_add_app_options prism --enable-application=prism
ac_add_app_options prism --with-libxul-sdk=../xulrunner/dist
EOF

make -f client.mk build

# Package XULRunner
cd ../prism/prism/prism/installer

make

%install
rm -rf $RPM_BUILD_ROOT

cd %{_builddir}/%name-%version/prism/prism/dist
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
cp -R prism $RPM_BUILD_ROOT%{_libdir}/prism
#rm -rf $RPM_BUILD_ROOT%{_libdir}/prism/xulrunner
#ln -s /usr/lib/songbird/xulrunner $RPM_BUILD_ROOT%{_libdir}/prism/

cp $RPM_BUILD_ROOT%{_libdir}/prism/chrome/icons/default/install-shortcut48.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/prism.png
ln -s %{_libdir}/prism/prism $RPM_BUILD_ROOT%{_bindir}/prism

# Don't deliver nss, nspr libraries on OpenSolaris
%if %without_moz_nss_nspr
rm -rf $RPM_BUILD_ROOT%{_libdir}/prism/xulrunner/libfreebl*
rm -rf $RPM_BUILD_ROOT%{_libdir}/prism/xulrunner/libnss*
rm -rf $RPM_BUILD_ROOT%{_libdir}/prism/xulrunner/libnspr*
rm -rf $RPM_BUILD_ROOT%{_libdir}/prism/xulrunner/libpl*
rm -rf $RPM_BUILD_ROOT%{_libdir}/prism/xulrunner/libs*
ln -s ../../firefox/libnssckbi.so $RPM_BUILD_ROOT%{_libdir}/prism/xulrunner/
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/prism
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/prism
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/prism.png

%changelog
* Mon Feb 09 2009 - alfred.peng@sun.com
- created
