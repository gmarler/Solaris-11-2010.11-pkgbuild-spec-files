#
# spec file for package SFEsugar-artwork
#
# includes module(s): sugar-artwork
#

%define pythonver 2.6

%include Solaris.inc
Name:                    SFEsugar-artwork
Summary:                 Sugar Artwork
URL:                     http://www.sugarlabs.org/
Version:                 0.87.1
Source:                  http://download.sugarlabs.org/sources/sucrose/glucose/sugar-artwork/sugar-artwork-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:                SUNWgtk2
Requires:                SFEicon-slicer
Requires:                SUNWicon-naming-utils
BuildRequires:           SUNWgtk2-devel
BuildRequires:           SFEicon-slicer
BuildRequires:           SUNWicon-naming-utils

%prep
%setup -q -n sugar-artwork-%version

%build
export PYTHON=/usr/bin/python%{pythonver}
./configure --prefix=%{_prefix} \
            --sysconfdir=%{_sysconfdir}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/gtk-2.0
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/sugar
%{_datadir}/themes/sugar-100
%{_datadir}/themes/sugar-72

%changelog
* Tue Feb 02 2010 - Brian Cameron  <brian.cameron@sun.com>
- Created with 0.87.1.
