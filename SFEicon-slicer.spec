#
# spec file for package SFEicon-slicer
#
# Copyright 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                    SFEicon-slicer
Summary:                 Utility for generating icon themes
Version:                 0.3
Source:                  http://freedesktop.org/software/icon-slicer/releases/icon-slicer-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:       SUNWgtk2
BuildRequires:  SUNWgtk2-devel

%include default-depend.inc

%prep
%setup -q -n icon-slicer-%{version}

%build
./configure --prefix=%{_prefix}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%changelog
* Tue Feb 02 2010 - brian.cameron@sun.com
- Created with version 0.3
