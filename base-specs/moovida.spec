#
# spec file for package moovida
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# You may need to add the following line to /etc/mime.types for
# the sample OGG files to be visible in moovida.
#
# application/ogg ogg
#
# Owner: yippi 
#
# bugdb: https://bugs.launchpad.net/elisa
#

%{?!pythonver:%define pythonver 2.6}

Name:              moovida
License:           GPL v3, MIT
Summary:           Media center written in Python
URL:               http://www.moovida.com/
Version:           1.0.6
Source:            http://www.moovida.com/media/public/%{name}-%{version}.tar.gz
#date:2008-12-01 owner:fujiwara type:feature bugid:249822
Patch1:            moovida-01-g11n-localedir.diff
#date:2009-03-03 owner:yippi type:feature
Patch2:            moovida-02-noautoupdate.diff
#date:2008-11-26 owner:yippi type:branding 
Patch3:            moovida-03-manpage.diff
#date:2009-08-06 owner:yippi type:bug bugid:400134
Patch4:            moovida-04-pidof.diff

%description
Moovida is an open source cross-platform media center solution.
Moovida runs on top of the GStreamer multimedia framework and takes
full advantage of harware acceleration provided by modern graphic
cards by using OpenGL APIs. You can watch movies, listen to music 
and view pictures with Moovida.

%prep
%setup -q -n elisa-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build

%install
python%{pythonver} setup.py install --root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/elisa
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/elisa
%{_libdir}/python%{pythonver}/vendor-packages/elisa-*-py%{pythonver}.egg-info
%{_libdir}/python%{pythonver}/vendor-packages/elisa-*-py%{pythonver}-nspkg.pth

%changelog
* Thu Aug 06 2009 Brian Cameron <brian.cameron@sun.com>
- Update to 1.0.6 and remove upstream patches.
* Tue Jul 21 2009 Brian Cameron <brian.cameron@sun.com>
- Merge patch 1 and 4, and also fix upstream bug #400137.  Add patch 
  moovida-05-pidof.diff to address bug #400134.
* Wed Jul 15 2009 Brian Cameron <brian.cameron@sun.com>
- Created with version 1.0.5.
