#
# spec file for package SFEsugar-presence-service
#
# includes module(s): sugar-presence-service
#

%define pythonver 2.6

%include Solaris.inc
Name:                    SFEsugar-presence-service
Summary:                 Sugar Presence Service
URL:                     http://www.sugarlabs.org/
Version:                 0.88.0
Source:                  http://download.sugarlabs.org/sources/sucrose/glucose/sugar-presence-service/sugar-presence-service-%{version}.tar.bz2
Patch1:                  sugar-presence-service-01-python.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:		 SFEsugar
BuildRequires:		 SFEsugar

%prep
%setup -q -n sugar-presence-service-%version
%patch1 -p1

%build
export PYTHON=/usr/bin/python%{pythonver}
./configure --prefix=%{_prefix}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

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
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/dbus-1/services
%{_datadir}/sugar-presence-service

%changelog
* Tue Apr 27 2010 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.88.0.
* Tue Feb 02 2010 - Brian Cameron  <brian.cameron@sun.com>
- Created with 0.87.1.
