#
# spec file for package SFEpython26-telepathy
#
# Copyright 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                    SFEpython26-telepathy

Summary:                 Telepathy Python Bindings
Version:                 0.15.15
Source:                  http://telepathy.freedesktop.org/releases/telepathy-python/telepathy-python-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython
Requires:                SUNWlibtelepathy
BuildRequires:           SUNWPython-devel
BuildRequires:           SUNWlibtelepathy

%include default-depend.inc

%define python_version 2.6

%prep
%setup -q -n telepathy-python-%{version}

%build
export PYTHON=/usr/bin/python%{python_version}
./configure --prefix=%{_prefix}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{python_version}/vendor-packages/*

%changelog
* Tue Feb 02 2010 - brian.cameron@sun.com
- Created with version 0.15.15.
