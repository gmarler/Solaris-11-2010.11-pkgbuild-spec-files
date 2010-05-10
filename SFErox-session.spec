#
# spec file for package SFErox-session.spec
#
# includes module(s): rox-session
#
#

%include Solaris.inc

%define _name ROX-Session
Summary:	ROX-Session - a really simple session manager
Name:		rox-Session
Version:	0.28
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://heanet.dl.sourceforge.net/rox/rox-session-%{version}.tar.bz2
URL:		http://rox.sourceforge.net/desktop/ROX-Session
#Requires:	dbus >= 0.33
#Requires:	python-dbus >= 0.33
#Requires:	rox >= 2.3
Requires:	SFErox
#Requires:	rox-Lib2 >= 1.9.16
#BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%define		_roxdir	%{_libdir}/rox

%description
ROX-Session is a simple and easy to use session manager. It is part of
the ROX project, but can also be used on its own. It sets up your
desktop when you log in, and starts any applications you ask it to.
ROX-Session allows you to set various settings, such as the default
font, cursor blinking and mouse behaviour. It also allows you to
choose a window manager, and change between window managers without
logging out.


%prep
%setup -q -n rox-session-%{version}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_roxdir}/%{_name}/{Messages,images}

cd %{_name}
install images/*.png $RPM_BUILD_ROOT%{_roxdir}/%{_name}/images
install Messages/*.gmo $RPM_BUILD_ROOT%{_roxdir}/%{_name}/Messages
install .DirIcon AppRun RunROX Login SetupPanel Styles browser $RPM_BUILD_ROOT%{_roxdir}/%{_name}
install *.py *.xml $RPM_BUILD_ROOT%{_roxdir}/%{_name}

#%py_comp $RPM_BUILD_ROOT%{_roxdir}/%{_name}
#%py_ocomp $RPM_BUILD_ROOT%{_roxdir}/%{_name}
find $RPM_BUILD_ROOT \( -name \*.la -o -name \*.a \) -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc %{_name}/Help/{Changes,DBUS-API,README}
%dir %{_roxdir}/%{_name}
%attr(755,root,root) %{_roxdir}/%{_name}/AppRun
%attr(755,root,root) %{_roxdir}/%{_name}/Login
%attr(755,root,root) %{_roxdir}/%{_name}/RunROX
%attr(755,root,root) %{_roxdir}/%{_name}/SetupPanel
%attr(755,root,root) %{_roxdir}/%{_name}/browser
%{_roxdir}/%{_name}/.DirIcon
%{_roxdir}/%{_name}/Styles
%{_roxdir}/%{_name}/*.py
%{_roxdir}/%{_name}/*.xml
%{_roxdir}/%{_name}/images
%dir %{_roxdir}/%{_name}/Messages
%{_roxdir}/%{_name}/Messages/da.gmo
 %{_roxdir}/%{_name}/Messages/de.gmo
 %{_roxdir}/%{_name}/Messages/es.gmo
%{_roxdir}/%{_name}/Messages/fr.gmo
%{_roxdir}/%{_name}/Messages/it.gmo
%{_roxdir}/%{_name}/Messages/ja.gmo
%{_roxdir}/%{_name}/Messages/lt.gmo
 %{_roxdir}/%{_name}/Messages/nl.gmo
 %{_roxdir}/%{_name}/Messages/pt_BR.gmo
%{_roxdir}/%{_name}/Messages/ru.gmo
%{_roxdir}/%{_name}/Messages/zh_CN.gmo
 %{_roxdir}/%{_name}/Messages/zh_TW.gmo

%define date	%(echo `LC_ALL="C" date +"%a %b %d %Y"`)
%changelog
* Fri May 05 2010 yuntong.jin@sun.com
- Init spec file
#http://cvs.pld-linux.org/cgi-bin/cvsweb/packages/rox-Session/rox-Session.spec?rev=1.26
