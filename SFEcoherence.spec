#
# spec file for package SUNWcoherence
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# bugdb: http://coherence.beebits.net/ticket/$bugid

%include Solaris.inc


Name:                    SFEcoherence
Summary:                 DLNA/UPnP framework for the digital living 
URL:                     http://coherence.beebits.net
Version:                 0.6.0
Source:                  http://coherence.beebits.net/download/Coherence-%{version}.tar.gz

# date:2009-02-16 owner:alfred type:bug bugid:190
Patch1:                  coherence-01-path-blank.diff

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython

%include default-depend.inc

%define pythonver 2.4

%prep
%setup -q -n Coherence-%{version}
mv misc/Desktop\ Applet/ misc/Desktop-Applet
%patch1 -p1

%build
python%{pythonver} setup.py build

%install
rm -rf $RPM_BUILD_ROOT

python%{pythonver} setup.py install --root=$RPM_BUILD_ROOT --prefix=%_prefix

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/site-packages/Coherence-%{version}-py%{pythonver}.egg-info
%{_libdir}/python%{pythonver}/site-packages/coherence/*
%{_libdir}/python%{pythonver}/site-packages/misc/*

%changelog
* Mon Feb 16 2009 - alfred.peng@sun.com
* Add patch path-blank.diff to fix packaging problem.
  Bump to 0.6.0.
* Thu Oct 09 2008 - jijun.yu@sun.com
- Initial version.
