#
# spec file for package SFEgimpfx-foundry
#
# includes module(s): gimpfx-foundry
#
%include Solaris.inc

%define gimp_api_ver 2.0

Name:		SFEgimpfx-foundry
Summary:	Cross-platform development framework/toolkit
Version:	2.6-1
IPS_component_version:	2.6.1
Group:		Applications/Graphics
Source:		%{sf_download}/gimpfx-foundry/gimpfx-foundry-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-img-editor

%prep
%setup -q -c -n %name-%version

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_datadir}/gimp/%{gimp_api_ver}/scripts
cp *.scm $RPM_BUILD_ROOT%{_datadir}/gimp/%{gimp_api_ver}/scripts
chmod a+r $RPM_BUILD_ROOT%{_datadir}/gimp/%{gimp_api_ver}/scripts/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gimp/%{gimp_api_ver}

%changelog
* Wed May 02 2010 - Milan Jurik
- bump to 2.6-1
* Wed Jan 23 2008 - laca@sun.com
- Initial spec
