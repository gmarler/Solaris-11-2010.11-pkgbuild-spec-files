#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEtypo3
Summary:             Typo 3 
Version:             4.2.10
Source:              %{sf_download}/typo3/typo3_src-%{version}.tar.gz
SUNW_BaseDir:        /
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

#pause, seems all is contained in recent builds of the OS # Requires: SFEphp

%prep
%setup -q -n typo3_src-%version

#%build

#dummy - noting to make

%install
rm -rf $RPM_BUILD_ROOT

#make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/var/typo3/typo3_src-%version
cp -pr * $RPM_BUILD_ROOT/var/typo3/typo3_src-%version
ln -s typo3_src-%version $RPM_BUILD_ROOT/var/typo3/typo3_src

%clean
rm -rf $RPM_BUILD_ROOT

%files
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, webservd, webservd) %{_localstatedir}/typo3
%defattr (-, webservd, webservd)
%{_localstatedir}/typo3/*



%changelog
* Sun Nov 22 2009 - Thomas Wagner
- bump to 4.2.10, pause Requires SFEphp (to be verified)
* Sun Sep 06 2009 - Thomas Wagner
- bump to 4.2.8
* Sun Mar 11 2007 - Thomas Wagner
- Initial spec
