#
# spec file for package SFErox-lib2.spec
#
# includes module(s): rox-lib2
#
#

%include Solaris.inc

Summary:	ROX-Filer's base-package

Name:		rox-base
Version:	1.0.2
Release:	5
License:	GPL
Group:		X11/Applications
Source0:	http://download.sourceforge.net/rox/%{name}-%{version}.tgz
# Source0-md5:	46de53c01c6ccea7f3467ce7e37717cc
URL:		http://rox.sourceforge.net/
PreReq:		sh-utils
BuildArch:	noarch

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Base package needed to run ROX-Filer.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/Choices/{MIME-info,MIME-types,MIME-icons} \
	$RPM_BUILD_ROOT%{_pixmapsdir}/rox

install Choices/MIME-icons/*.xpm $RPM_BUILD_ROOT%{_datadir}/Choices/MIME-icons
ln -s %{_datadir}/Choices/MIME-icons $RPM_BUILD_ROOT%{_pixmapsdir}/rox
install Choices/MIME-info/{Standard,gnome-vfs.mime} \
	$RPM_BUILD_ROOT%{_datadir}/Choices/MIME-info
install Choices/MIME-types/{application_postscript,text} \
	$RPM_BUILD_ROOT%{_datadir}/Choices/MIME-types

%clean
rm -rf $RPM_BUILD_ROOT

%pre
test -h %{_pixmapsdir}/rox/MIME-icons || rm -rf %{_pixmapsdir}/rox/MIME-icons

%files
%defattr(644,root,root,755)
%doc README
%dir %{_datadir}/Choices
%{_datadir}/Choices/MIME-icons
%{_datadir}/Choices/MIME-info
%dir %{_datadir}/Choices/MIME-types
%attr(755,root,root) %{_datadir}/Choices/MIME-types/*
#%{_pixmapsdir}/rox
%{_datadir}/pixmaps/rox/*

%define date	%(echo `LC_ALL="C" date +"%a %b %d %Y"`)
%changelog
* Fri May 10 2010 - yuntong.jin@sun.com
- Init spec file

