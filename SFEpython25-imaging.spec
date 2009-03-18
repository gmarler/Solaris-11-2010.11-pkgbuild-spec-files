#
# spec file for package SUNWpython-imaging
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dkenny
#

%include Solaris.inc

%define pythonver 2.5
%use pil = python-imaging.spec

Name:                    SFEpython25-imaging
Summary:                 %{pil.summary}
URL:                     %{pil.url}
Version:                 %{pil.version}
Release:                 1
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:           SUNWgnome-base-libs-devel
BuildRequires:           SUNWPython25-devel
BuildRequires:           SUNWzlib
BuildRequires:           SUNWjpg-devel
BuildRequires:           SUNWpng-devel
BuildRequires:           SUNWfreetype2
BuildRequires:           SUNWpython25-setuptools
Requires:                SUNWPython25
Requires:                SUNWjpg

%include default-depend.inc

%description
The Python Imaging Library (PIL) adds image processing capabilities
to your Python interpreter.

This library provides extensive file format support, an efficient
internal representation, and powerful image processing capabilities.

%prep
rm -rf %{name}-%{version}
mkdir -p %{name}-%{version}
%pil.prep -d %{name}-%{version}

%build
%pil.build -d %{name}-%{version}


%install
rm -rf $RPM_BUILD_ROOT
%pil.install -d %{name}-%{version}

# remove /usr/bin/ files since they conflict with python 2.6 version.
rm -rf $RPM_BUILD_ROOT/%{_bindir}

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/PIL
%{_libdir}/python%{pythonver}/vendor-packages/PIL.pth
%doc -d Imaging-%{version} Sane/README
%doc(bzip2) -d Imaging-%{version} CHANGES README Sane/CHANGES Scripts/README
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc

%changelog
* Wed Mar 18 2009 - jeff.cai@sun.com
- Moved from spec-files-other
* Thu Nov 27 2008 - darren.kenny@sun.com
- Created based off SUNWpython-imaging.spec
* Tue Sep 16 2008 - matt.keenn@sun.com
- Update copyright
* Wed May 14 2008 - darren.kenny@sun.com
- Add SUWNjpg dependency.
* Fri Feb 15 2008 - dermot.mccluskey@sun.com
- remove *.pyo
* Tue Feb 12 2008 - dermot.mccluskey@sun.com
- initial version
