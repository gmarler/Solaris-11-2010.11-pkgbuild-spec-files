#
# spec file for package SFEopenttd.spec
#
%include Solaris.inc

%define src_name openttd

Name:           SFEopenttd
Version:        0.7.1
Summary:        Transport system simulation game
Source:         http://binaries.openttd.org/releases/%{version}/%{src_name}-%{version}-source.tar.bz2
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
BuildRequires:  SFEfreetype-devel
Requires:  SFEfreetype
BuildRequires:  SUNWdoxygen

%description
OpenTTD is modeled after a popular transportation business simulation game
by Chris Sawyer and enhances the game experience dramatically. Many features
were inspired by TTDPatch while others are original.


%prep
%setup -q -n openttd-%{version}%{?prever:-%{prever}}


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


%clean
rm -rf $RPM_BUILD_ROOT


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) /usr
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
* Sun Jul 05 2009 - Milan Jurik
- Initial version based on Fedora spec file