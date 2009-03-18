#
# spec file for package SUNWpython-zope-interface
#
# Owner: dkenny
#

%include Solaris.inc

%define pythonver 2.5
%use pzi = python-zope-interface.spec

Name:                    SFEpython25-zope-interface
Summary:                 %{pzi.summary}
URL:                     %{pzi.url}
Version:                 %{pzi.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython25
BuildRequires:           SUNWPython25-devel
BuildRequires:           SUNWpython25-setuptools

%include default-depend.inc

%prep
rm -rf %{name}-%{version}
mkdir -p  %{name}-%{version}
%pzi.prep -d %{name}-%{version}

%build
%pzi.build -d %{name}-%{version}

%install
rm -rf $RPM_BUILD_ROOT
%pzi.install -d %{name}-%{version}

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/python%{pythonver}
%{_libdir}/python%{pythonver}/vendor-packages
%doc -d zope.interface-%version README.txt
%doc(bzip2) -d zope.interface-%version CHANGES.txt PKG-INFO src/zope/interface/README.txt
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc


%changelog
* Wed Mar 18 2009 - jeff.cai@sun.com
- Moved from spec-files-other
* Tue Sep 16 2008 - matt.keenn@sun.com
- Update copyright
* Mon May 26 2008 - damien.carbery@sun.com
- Add Build/Requires SUNWPython/-devel.
* Wed Feb 19 2008 - darren.kenny@sun.com
- Revert to 3.3.0 since 3.4.x series seems to be too unstable (and version
  number keeps changing). Wait until 3.4.x stabilises before returning to it.
* Tue Feb 19 2008 - ghee.teo@sun.com
- Updated version to 3.4.1
* Tue Feb 12 2008 - dermot.mccluskey@sun.com
- Initial version
