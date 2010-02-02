#
# spec file for package SFEsugar-datastore
#
# includes module(s): sugar-datastore
#

%define pythonver 2.6

%include Solaris.inc
Name:                    SFEsugar-datastore
Summary:                 Sugar Datastore
URL:                     http://www.sugarlabs.org/
Version:                 0.87.2
Source:                  http://download.sugarlabs.org/sources/sucrose/glucose/sugar-datastore/sugar-datastore-%{version}.tar.bz2
Patch1:                  sugar-datastore-01-python.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:                SFEsugar
Requires:                SFEpython26-cjson
Requires:                SFExapian-bindings
BuildRequires:           SFEsugar
BuildRequires:           SFEpython26-cjson
BuildRequires:           SFExapian-bindings

%prep
%setup -q -n sugar-datastore-%version
%patch1 -p1

%build
export PYTHON=/usr/bin/python%{pythonver}
./configure --prefix=%{_prefix}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# move to verndor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

# replace the old scripts with script files
%post
%restart_fmri gconf-cache desktop-mime-cache icon-cache

%postun
%restart_fmri desktop-mime-cache

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/carquinyol
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/dbus-1/services

%changelog
* Tue Feb 02 2010 - Brian Cameron  <brian.cameron@sun.com>
- Created with 0.87.2
