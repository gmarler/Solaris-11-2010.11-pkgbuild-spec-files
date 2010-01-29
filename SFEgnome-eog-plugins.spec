#
# spec file for plugins of SUNWgnome-img-viewer
#
# includes module(s): eog-plugins
#
# Copyright 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%define owner jouby 
#
%include Solaris.inc

%define eog_bindir /usr/bin
%define eog_libdir /usr/lib
%define eog_libexecdir /usr/lib
%define eog_data        /usr/share

%use eog_plugins = eog-plugins.spec

%define _bindir %{eog_bindir}
%define _libexecdir %{eog_libexecdir}
%define _libdir %{eog_libdir}

Name:                    SFEgnome-eog-plugins
Summary:                 A collection of extra eog plugins 
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-img-viewer
Requires: SUNWlibchamplian
Requires: SUNWgnome-python-libs
Requires: SUNWglib2 
Requires: SUNWpython26

BuildRequires: SUNWlibexif
BuildRequires: SUNWgnome-img-viewer-devel
BuildRequires: SUNWgnome-common-devel

%description
It's a collection of plugins for use with the Eye of GNOME Image Viewer.
The included plugins provide a map view for where the picture was taken,
display of Exif information, Zoom to fit, etc. 

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version
%eog_plugins.prep -d %name-%version
cd %{_builddir}/%name-%version


%build
%eog_plugins.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%eog_plugins.install -d %name-%version


%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}(eog_plugins):$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a"  -exec rm -f {} ';

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache gconf-cache

%postun
%restart_fmri desktop-mime-cache

%files
%dir %attr (0755, root, bin) %{_libdir}
%{eog_libdir}/eog
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/locale
%{_datadir}/locale/*


%changelog
* Fri Jan 29 2010 - yuntong.jin@sun.com
- Remove .la .a file from package, disable postr plugins
* Fri Jan 22 2010 - yuntong.jin@sun.com
- Update dependency,license
* Tue Jan 19 2010 - yuntong.jin@sun.com
- Init 

