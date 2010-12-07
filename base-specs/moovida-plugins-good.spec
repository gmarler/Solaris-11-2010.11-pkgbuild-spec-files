#
# spec file for package moovida-plugins-good
#
# Copyright (c) 2008, 2010, Oracle and/or its affiliates. All rights reserved.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%define owner yippi

%define OSR 12197:1.0.1

#
# bugdb: http://bugs.launchpad.net/moovida/+bug/
#

Name:              moovida-plugins-good
License:           GPL v3
Vendor:            moovidia.com
Summary:           Good plugins for Moovida
URL:               http://www.moovida.com/
Version:           1.0.9
Source:            http://www.moovida.com/media/public/%{name}-%{version}.tar.gz
#date:2008-10-24 owner:yippi type:branding
# We remove winscreensaver plugin since it only works on the Windows platform.
Patch1:		   moovida-plugins-good-01-rm-plugins.diff

%description
The Moovida good plugins set contains plugins known to be well tested, working
and being compatible with the Moovida licensing model.

%prep
%setup -q -n elisa-plugins-good-%{version}
%patch1 -p1

%build

%install
python%{default_python_version} setup.py install --root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{default_python_version}/vendor-packages/elisa
%{_libdir}/python%{default_python_version}/vendor-packages/elisa_plugin_*-nspkg.pth
%{_libdir}/python%{default_python_version}/vendor-packages/elisa_plugin_*.egg-info

%changelog
* Tue Dec 08 2009 Brian Cameron  <brian.cameron@sun.com>
- Bump to 1.0.9.
* Wed Nov 04 2009 Brian Cameron  <brian.cameron@sun.com>
- Bump to 1.0.8.
* Mon Nov 02 2009 Brian Cameron  <brian.cameron@sun.com>
- Bump to 1.0.7.
* Mon Oct 12 2009 Brian Cameron  <brian.cameron@sun.com>
- Now use %{default_python_version}.
* Thu Aug 06 2009 Brian Cameron  <brian.cameron@sun.com>
- Bump to version 1.0.6, and remove upstream patch.
* Wed Jul 15 2009 Brian Cameron  <brian.cameron@sun.com>
- Created with version 1.0.5.
