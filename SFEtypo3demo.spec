#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEtypo3demo
Summary:             Typo 3 Demo Site - needed to start new installations
Version:             4.2.10
Source:              %{sf_download}/typo3/dummy-%{version}.tar.gz
SUNW_BaseDir:        /
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SFEtypo3

%prep
%setup -q -n dummy-%version

%build

#dummy - noting to make

%install
rm -rf $RPM_BUILD_ROOT

#make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/var/typo3/dummy
[ -L typo3_src ] || ln -s ../typo3_src
cp -pr * $RPM_BUILD_ROOT/var/typo3/dummy

%clean
rm -rf $RPM_BUILD_ROOT

%files
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, webservd, webservd) %{_localstatedir}/typo3/dummy
%defattr (-, webservd, webservd)
%{_localstatedir}/typo3/dummy/*



%changelog
* Sun Nov 22 2009 - Thomas Wagner
- bump to 4.2.10
- adjust detection for existing symlink
* Sun Sep 06 2009 - Thomas Wagner
- bump to 4.2.8
* Sun Mar 11 2007 - Thomas Wagner
- Initial spec
