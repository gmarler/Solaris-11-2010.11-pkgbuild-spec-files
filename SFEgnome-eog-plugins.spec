#
# spec file for plugins of package SUNWgnome-img-viewer
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
Summary:                 extra plugins of eog 
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWlibart
Requires: SUNWgtk2
Requires: SUNWgnome-libs
Requires: SUNWglib2 
Requires: SUNWgnome-img-view
Requires: SUNWpython26
Requires: SFElibchamplian
Requires: SUNWgnome-python-libs


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
#gzcat %SOURCE0 | tar xf -

%build
%eog_plugins.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%eog_plugins.install -d %name-%version


%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}(eog_plugins):$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

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
% Tue Jan 19 2010 - yuntong.jin@sun.com
- Init 

