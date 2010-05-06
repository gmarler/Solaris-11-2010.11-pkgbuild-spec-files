#
# spec file for package SFErox-lib2.spec
#
# includes module(s): rox-lib2
#
#

%include Solaris.inc

%define _name ROX-Lib2

Summary:	A library for ROX applications
Name:		rox-lib
Version:	2.0.2
Release:	1
License:	LGPL v2.1
Group:		Libraries/Python
Source0:	http://dl.sourceforge.net/rox/rox-lib-%{version}.tgz
# Source0-md5:	e7d168299e7812d4df729cc175b44e2e
URL:		http://roscidus.com/desktop/ROX-Lib
#BuildRequires:	rpmbuild(macros) >= 1.234
#Requires:	python-pygtk-gtk >= 2.0

Requires:       SUNWgnome-python26-libs
Requires: SUNWPython26

#%pyrequires_eq  python
BuildRoot:      %{_tmppath}/%{name}-%{version}-build


%description
ROX-Lib contains shared code which can be used by other ROX
applications. It is a GTK+2 version.

%package devel
Summary:	ROX-Lib2 library development files
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Documentation for developing applications using ROX-Lib2 library.

%prep
%setup -q -n %name-%version

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{_name}/{bin,Help/python,python/rox} \
	$RPM_BUILD_ROOT%{_libdir}/%{_name}/Messages

install %{_name}/App* $RPM_BUILD_ROOT%{_libdir}/%{_name}
install %{_name}/.DirIcon $RPM_BUILD_ROOT%{_libdir}/%{_name}
install %{_name}/python/rox/* $RPM_BUILD_ROOT%{_libdir}/%{_name}/python/rox
install %{_name}/Help/{Errors,README} $RPM_BUILD_ROOT%{_libdir}/%{_name}/Help
install %{_name}/Help/python/* $RPM_BUILD_ROOT%{_libdir}/%{_name}/Help/python
install %{_name}/Messages/*.gmo $RPM_BUILD_ROOT%{_libdir}/%{_name}/Messages

#%py_comp $RPM_BUILD_ROOT%{_libdir}/%{_name}/python/rox
#%py_ocomp $RPM_BUILD_ROOT%{_libdir}/%{_name}/python/rox

#%py_postclean %{_libdir}/%{_name}/python/rox
find $RPM_BUILD_ROOT \( -name \*.la -o -name \*.a \) -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc %{_name}/Help/{Changes,TODO,findrox.py}
%attr(755,root,root) %{_libdir}/%{_name}/AppRun
%attr(755,root,root) %{_libdir}/%{_name}/python/rox/suchild.sh
%{_libdir}/%{_name}/AppI*
%{_libdir}/%{_name}/.DirIcon
%dir %{_libdir}/%{_name}/Help
%{_libdir}/%{_name}/Help/Errors
%{_libdir}/%{_name}/Help/README
%{_libdir}/%{_name}/Messages/de.gmo
%{_libdir}/%{_name}/Messages/fr.gmo
%{_libdir}/%{_name}/Messages/it.gmo
%{_libdir}/%{_name}/Messages/pt_BR.gmo
%{_libdir}/%{_name}/Messages/zh_CN.gmo
%{_libdir}/%{_name}/Messages/zh_TW.gmo
%{_libdir}/%{_name}/python/rox/*.py
%dir %{_libdir}/%{_name}
%dir %{_libdir}/%{_name}/Messages
%dir %{_libdir}/%{_name}/python
%dir %{_libdir}/%{_name}/python/rox

%attr(755,root,root) %{_libdir}/ROX-Lib2/bin

%files devel
%defattr(644,root,root,755)
%dir %{_libdir}/%{_name}/Help/python
%{_libdir}/%{_name}/Help/python/*.html

%define date	%(echo `LC_ALL="C" date +"%a %b %d %Y"`)
%changelog
* Fri May 05 2010 yuntong.jin@sun.com
- Init spec file
##http://cvs.pld-linux.org/cgi-bin/cvsweb/packages/rox-Lib2/rox-Lib2.spec?rev=1.21

