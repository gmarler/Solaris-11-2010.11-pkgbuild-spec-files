#
# spec file for package SFEopenttd.spec
#
%include Solaris.inc

%define src_name openttd
%define src_version 1.0.0

Name:           SFEopenttd
Version:        1.0.0
Summary:        Transport system simulation game
Source:         http://binaries.openttd.org/releases/%{src_version}/%{src_name}-%{src_version}-source.tar.bz2
Source1:	http://bundles.openttdcoop.org/opengfx/releases/opengfx-0.2.2.zip
Source2:	http://bundles.openttdcoop.org/opensfx/releases/opensfx-0.2.2.zip
Source3:	http://bundles.openttdcoop.org/openmsx/releases/openmsx-0.2.1.zip
Patch1:         openttd-01-makedependlimit.diff
URL:            http://www.openttd.org/
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-build

%include default-depend.inc
BuildRequires:  SUNWlibsdl-devel
Requires:  SUNWlibsdl
BuildRequires:  SUNWpng-devel
Requires:  SUNWpng
BuildRequires:  SUNWunzip
BuildRequires:  SUNWzlib
Requires:  SUNWzlib
BuildRequires:  SUNWfontconfig
Requires:  SUNWfontconfig
BuildRequires:  SUNWicu
Requires:  SUNWicu
BuildRequires:  SUNWfreetype2
Requires:  SUNWfreetype2
BuildRequires:  SUNWdoxygen
Requires:  SFElzo
BuildRequires:	SUNWgsed
BuildRequires:	SUNWgnome-desktop-prefs

%description
OpenTTD is modeled after a popular transportation business simulation game
by Chris Sawyer and enhances the game experience dramatically. Many features
were inspired by TTDPatch while others are original.


%prep
%setup -q -n openttd-%{src_version}


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

CC=/usr/sfw/bin/gcc \
CXX=/usr/sfw/bin/g++ \
bash ./configure \
        --disable-strip \
        --prefix-dir= \
        --binary-dir=%{_bindir} \
        --data-dir=%{_datadir}/openttd \
        --icon-dir=%{_datadir}/pixmaps \
        --icon-theme-dir=%{_datadir}/icons/hicolor \
        --man-dir=%{_mandir}/man6 \
        --menu-dir=%{_datadir}/applications \
        --without-shared-dir \
        --doc-dir=%{_docdir} \
        --install-dir=$RPM_BUILD_ROOT
gmake -j$CPUS
# generate the AI API docs
cd src/ai/api
doxygen


%install
rm -rf $RPM_BUILD_ROOT
%patch1 -p1
make install VERBOSE=1

# Remove the installed docs - we will install subset of those
rm -rf $RPM_BUILD_ROOT%{_docdir}

# install documentation
install -dpm 755 $RPM_BUILD_ROOT%{_datadir}/openttd/docs/
cp -r docs/* $RPM_BUILD_ROOT%{_datadir}/openttd/docs/

# Patch generated desktop file, as desktop-file-install doesn't know 1.1 format yet
sed -i 's/Version=1.1/Version=1.0/' media/openttd.desktop
desktop-file-install --dir=$RPM_BUILD_ROOT%{_datadir}/applications \
        --add-category=StrategyGame \
        media/openttd.desktop

cd $RPM_BUILD_ROOT%{_datadir}/openttd/data && unzip %SOURCE1 && unzip %SOURCE2 && unzip %SOURCE3

%clean
rm -rf $RPM_BUILD_ROOT


%post
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( touch %{_datadir}/icons/hicolor || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
        %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
) | $BASEDIR/var/lib/postrun/postrun -i -a

%postun
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( touch %{_datadir}/icons/hicolor || :
  if [ -x %{_bindir}/gtk-update-icon-cache ]; then
        %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
  fi
) | $BASEDIR/var/lib/postrun/postrun -i -a

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man6
%{_mandir}/man6/*
%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*
%dir %attr (0755, root, other) %{_datadir}/openttd
%{_datadir}/openttd/*

%changelog
* Thu Apr 01 2010 - Milan Jurik
- update to 1.0.0
* Mon Mar 29 2010 - Milan Jurik
- update to 1.0.0-RC3, support for OpenTTD data files
* Wed Mar 24 2010 - Milan Jurik
- freetype from main as build dependency
* Sat jan 16 2010 - Milan Jurik
- update to 0.7.5
- disable makepend because of CR 6917536
* Sun Aug 16 2009 - Milan Jurik
- update to 0.7.2
- fix for post-scripts
* Sun Jul 05 2009 - Milan Jurik
- Initial version based on Fedora spec file
