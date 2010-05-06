#
# spec file for package SFErox-lib2.spec
#
# includes module(s): rox-lib2
#
#

%include Solaris.inc

Summary:	File manager

Name:		rox
Version:	2.5
Release:	2
License:	GPL v2
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/rox/rox-filer-%{version}.tar.bz2
# Source0-md5:	56e6a29f2dbdf11d6f4b74a3f03ff959
#Source1:	          %{name}.desktop
#Patch0:		%{name}-01-help.diff
URL:		http://rox.sourceforge.net/
URL:           http://roscidus.com/desktop/ROX-Filer
#BuildRequires:	shared-mime-info >= 0.14
#BuildRequires:	xorg-lib-libSM-devel
#Requires:	glib2 >= 2.0.3
#Requires:	gtk+2 >= 2:2.4.0
#Requires:	libxml2 >= 2.0.0
#Requires(post,postun):	shared-mime-info >= 0.14
Conflicts:	rox-base
#BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%define         _platform %(echo `uname -s`-`uname -m|sed 's/i.86/ix86/'`)
%define		_roxdir %{_libdir}/rox

%description
ROX-Filer is a small, fast and powerful file manager for Linux and
Unix systems.

%prep
%setup -q -n rox-filer-%{version}
#%patch0 -p1

%build
cd ROX-Filer/src
%{__autoconf}

cd -

mkdir ROX-Filer/build
cd ROX-Filer/build
../src/configure

make

%install
rm -rf $RPM_BUILD_ROOT

install -d \
	$RPM_BUILD_ROOT%{_bindir} \
	$RPM_BUILD_ROOT%{_datadir}/mime/packages \
	$RPM_BUILD_ROOT%{_mandir}/man1 \
	$RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_iconsdir} \
	$RPM_BUILD_ROOT%{_pixmapsdir} \
	$RPM_BUILD_ROOT%{_roxdir}/ROX-Filer/{Help,Messages} \
	$RPM_BUILD_ROOT/etc/xdg/rox.sourceforge.net

cat >> $RPM_BUILD_ROOT%{_bindir}/rox << 'EOF'
#!/bin/sh
exec %{_roxdir}/ROX-Filer/AppRun "$@"
EOF

install rox.xml $RPM_BUILD_ROOT%{_datadir}/mime/packages

install rox.1 $RPM_BUILD_ROOT%{_mandir}/man1

#install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

install ROX-Filer/.DirIcon $RPM_BUILD_ROOT%{_pixmapsdir}/rox.png

install ROX-Filer/Help/Manual*.html $RPM_BUILD_ROOT%{_roxdir}/ROX-Filer/Help

install ROX-Filer/Messages/*.gmo $RPM_BUILD_ROOT%{_roxdir}/ROX-Filer/Messages

cp -r ROX-Filer/ROX $RPM_BUILD_ROOT%{_iconsdir}

cp -r ROX-Filer/images $RPM_BUILD_ROOT%{_roxdir}/ROX-Filer

install ROX-Filer/AppRun $RPM_BUILD_ROOT%{_roxdir}/ROX-Filer
install ROX-Filer/ROX-Filer $RPM_BUILD_ROOT%{_roxdir}/ROX-Filer

install ROX-Filer/*.{css,xml} $RPM_BUILD_ROOT%{_roxdir}/ROX-Filer

install ROX-Filer/.DirIcon $RPM_BUILD_ROOT%{_roxdir}/ROX-Filer

cp -r Choices/* $RPM_BUILD_ROOT/etc/xdg/rox.sourceforge.net

find $RPM_BUILD_ROOT \( -name \*.la -o -name \*.a \) -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri gconf-cache desktop-mime-cache icon-cache mime-types-cache

%postun
%restart_fmri desktop-mime-cache mime-types-cache

%files
%defattr(644,root,root,755)
%doc ROX-Filer/Help/{Changes,README,TODO}
%doc ROX-Filer/Help/README-es
%attr(755,root,root) %{_bindir}/rox
%dir %{_roxdir}
%dir %{_roxdir}/ROX-Filer
%dir %{_roxdir}/ROX-Filer/Help
%{_roxdir}/ROX-Filer/Help/Manual.html
%{_roxdir}/ROX-Filer/Help/Manual-fr.html
%{_roxdir}/ROX-Filer/Help/Manual-it.html
%dir %{_roxdir}/ROX-Filer/Messages
%{_roxdir}/ROX-Filer/Messages/cs.gmo
%{_roxdir}/ROX-Filer/Messages/da.gmo
%{_roxdir}/ROX-Filer/Messages/de.gmo
%{_roxdir}/ROX-Filer/Messages/es.gmo
%{_roxdir}/ROX-Filer/Messages/et_EE.gmo
%{_roxdir}/ROX-Filer/Messages/eu.gmo
%{_roxdir}/ROX-Filer/Messages/fi.gmo
%{_roxdir}/ROX-Filer/Messages/fr.gmo
%{_roxdir}/ROX-Filer/Messages/hu.gmo
%{_roxdir}/ROX-Filer/Messages/it.gmo
%{_roxdir}/ROX-Filer/Messages/ja.gmo
%{_roxdir}/ROX-Filer/Messages/nl.gmo
%{_roxdir}/ROX-Filer/Messages/no.gmo
%{_roxdir}/ROX-Filer/Messages/pl.gmo
%{_roxdir}/ROX-Filer/Messages/pt_PT.gmo
%{_roxdir}/ROX-Filer/Messages/pt_BR.gmo
%{_roxdir}/ROX-Filer/Messages/ro.gmo
%{_roxdir}/ROX-Filer/Messages/ru.gmo
%{_roxdir}/ROX-Filer/Messages/sv.gmo
%{_roxdir}/ROX-Filer/Messages/uk.gmo
%{_roxdir}/ROX-Filer/Messages/vi_VN.gmo
%{_roxdir}/ROX-Filer/Messages/zh_CN.gmo
%{_roxdir}/ROX-Filer/Messages/zh_TW.gmo
%{_roxdir}/ROX-Filer/images
%attr(755,root,root) %{_roxdir}/ROX-Filer/AppRun
%attr(755,root,root) %{_roxdir}/ROX-Filer/ROX-Filer
%{_roxdir}/ROX-Filer/*.xml
%{_roxdir}/ROX-Filer/*.css
%{_roxdir}/ROX-Filer/.DirIcon
%dir /etc/xdg/rox.sourceforge.net
%dir /etc/xdg/rox.sourceforge.net/MIME-types
%attr(755,root,root) /etc/xdg/rox.sourceforge.net/MIME-types/*
%{_datadir}/mime/packages/rox.xml
#%{_desktopdir}/rox.desktop
#%{_iconsdir}/ROX
#%{_pixmapsdir}/rox.png
%{_mandir}/man1/*

%define date	%(echo `LC_ALL="C" date +"%a %b %d %Y"`)
%changelog
* Fri May 05 2010 yuntong.jin@sun.com
- Init spec file

