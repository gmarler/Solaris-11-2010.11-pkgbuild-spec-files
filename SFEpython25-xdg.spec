#
# spec file for package SUNWpython-xdg
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dkenny
#

%include Solaris.inc

%define pythonver 2.5
%use pyxdg = python-xdg.spec

Name:            SFEpython25-xdg
Summary:         %{pyxdg.summary}
URL:             %{pyxdg.url}
Version:         %{pyxdg.version}
SUNW_BaseDir:    %{_basedir}
BuildRoot:       %{_tmppath}/%{name}-%{version}-build
BuildRequires:   SUNWPython25-devel
BuildRequires:   SUNWpython25-setuptools
Requires:        SUNWPython25

%include default-depend.inc

%description
Extensions to python-distutils for large or complex distributions.

%prep
rm -rf %{name}-%{version}
mkdir -p %{name}-%{version}
%pyxdg.prep -d  %{name}-%{version}

%build
%pyxdg.build -d  %{name}-%{version}

%install
rm -rf $RPM_BUILD_ROOT
%pyxdg.install -d  %{name}-%{version}

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/*
%doc -d  pyxdg-%version AUTHORS README PKG-INFO
%doc(bzip2) -d  pyxdg-%version COPYING ChangeLog
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc

%changelog
* Wed Mar 18 2009 - jeff.cai@sun.com
- Moved from spec-files-other
* Thu Nov 27 2008 - darren.kenny@sun.com
- Created based on SUNWpython-xdg.spec
* Tue Nov 18 2008 - jedy.wang@sun.com
- Fix installation directory problem.
* Wed Oct 29 2008 - brian.cameron@sun.com
- Add patch xdg-01-indentation.diff to fix runtime bugzilla bug #18289.
* Mon Oct 27 2008 - brian.cameron@sun.com
- Bump to 0.16.
* Fri Sep 12 2008 - matt.keenn@sun.com
- Update copyright
* Wed May 14 2008 - darren.kenny@sun.com
- Add dependency for SUNWPython
* Tue Feb 12 2008 - dermot.mccluskey@sun.com
- initial version
