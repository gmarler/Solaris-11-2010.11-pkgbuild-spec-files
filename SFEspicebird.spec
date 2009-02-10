#
# spec file for package SFEspicebird
#
# includes module(s): spicebird
#
# Owner: alfred
#

%include Solaris.inc

Name:          SFEspicebird
Summary:       collaboration client for email, contacts, calendaring and IM.
Version:       0.7
Source:        http://files.spicebird.org/pub/spicebird.org/spicebird/releases/%{version}/source/spicebird-beta-%{version}-full_source.tar.bz2

# default: not with Mozilla's nss/nspr libs, but the system ones.
%define without_moz_nss_nspr %{?_without_moz_nss_nspr:0}%{?!_without_moz_nss_nspr:1}

URL:           http://www.spicebird.com/
SUNW_BaseDir:  %{_basedir}
BuildRoot:     %{_tmppath}/%{name}-%{version}-build

#####################################
##  Package Requirements Section   ##
#####################################

%include default-depend.inc
Requires: SUNWdbus-bindings
Requires: SUNWgnome-base-libs
Requires: SUNWtelepathy-glib
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

# Songbird depends on Firefox's plugins.
Requires: SUNWfirefox

BuildRequires: SUNWdbus-bindings-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWtelepathy-glib-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWbzip
BuildRequires: SUNWgtar

%description
Spicebird is a collaboration client that provides integrated access to email,
contacts, calendaring and instant messaging in a single application.

%prep
%setup -q -n %name-%version -c

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

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

# Build
cd mozilla

cat << "EOF" > .mozconfig
mk_add_options MOZ_CO_TAG="THUNDERBIRD_3_0a2_RELEASE"
mk_add_options MOZ_CO_PROJECT="mail calendar"

ac_add_options --with-branding=collab/branding
ac_add_options --with-system-telepathy-stack
ac_add_options --enable-application=collab
ac_add_options --disable-tests
ac_add_options --disable-crashreporter
ac_add_options --disable-jemalloc
ac_add_options --disable-auto-deps
ac_add_options --with-system-jpeg
ac_add_options --disable-javaxpcom
ac_add_options --disable-shared
ac_add_options --enable-static
EOF

make -f client.mk build

# Package XULRunner
cd collab/installer

make

%install
rm -rf $RPM_BUILD_ROOT
cd %{_builddir}/%name-%version/mozilla/dist/

mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
cp -R spicebird-beta $RPM_BUILD_ROOT%{_libdir}/spicebird

cd ../
cp collab/branding/content/icon64.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/spicebird.png
ln -s %{_libdir}/spicebird/spicebird $RPM_BUILD_ROOT%{_bindir}/spicebird


# Don't deliver nss, nspr libraries on OpenSolaris
%if %without_moz_nss_nspr
rm -rf $RPM_BUILD_ROOT%{_libdir}/spicebird/libfreebl*
rm -rf $RPM_BUILD_ROOT%{_libdir}/spicebird/libnss*
rm -rf $RPM_BUILD_ROOT%{_libdir}/spicebird/libnspr*
rm -rf $RPM_BUILD_ROOT%{_libdir}/spicebird/libpl*
rm -rf $RPM_BUILD_ROOT%{_libdir}/spicebird/libs*
ln -s ../../firefox/libnssckbi.so $RPM_BUILD_ROOT%{_libdir}/spicebird/
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/spicebird
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/spicebird
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/spicebird.png

%changelog
* Tue Feb 10 2009 - alfred.peng@sun.com
- created
