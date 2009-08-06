#
# spec file for package SFEmoovida-plugins
#
# includes modules: moovida-plugins-good, moovida-plugins-bad
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi 
#
# bugdb: https://bugs.launchpad.net/elisa
#
%include Solaris.inc

%define pythonver 2.6

%use moovida_plugins_good = moovida-plugins-good.spec
%use moovida_plugins_bad = moovida-plugins-bad.spec

Name:              SFEmoovida-plugins
License:           GPL v3, MIT
Summary:           Media center plugins
Version:           %{default_pkg_version}
SUNW_BaseDir:      %{_basedir}

%ifnarch sparc
# these packages are only available on x86
BuildRoot:         %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires:     SFEmoovida
BuildRequires:     SUNWdbus-python26
BuildRequires:     SUNWPython26-devel
BuildRequires:     SUNWPython26-extra
BuildRequires:     SUNWimagick
BuildRequires:     SUNWsqlite3
BuildRequires:     SUNWgnome-python26-extras
BuildRequires:     SUNWlibpigment-devel
BuildRequires:     SUNWpython26-simplejson
BuildRequires:     SUNWpython26-pyopenssl
BuildRequires:     SUNWpython26-setuptools
Requires:          SFEmoovida
Requires:          SUNWgnome-media
Requires:          SUNWimagick
Requires:          SUNWPython
Requires:          SUNWsqlite3
Requires:          SUNWPython26-extra
Requires:          SUNWdbus-python26
Requires:          SUNWgnome-python26-extras
Requires:          SUNWgst-python26
Requires:          SUNWlibpigment
Requires:          SUNWlibpigment-python26
Requires:          SUNWpython26-imaging
Requires:          SUNWpython26-pyopenssl
Requires:          SUNWpython26-setuptools
Requires:          SUNWpython26-twisted
Requires:          SUNWpython26-twisted-web2
Requires:          SUNWpython26-simplejson
Requires:          SUNWpython26-cssutils
Requires:          SUNWdesktop-cache

%description
Moovida is an open source cross-platform media center solution.
Moovida runs on top of the GStreamer multimedia framework and takes
full advantage of harware acceleration provided by modern graphic
cards by using OpenGL APIs. You can watch movies, listen to music 
and view pictures with Moovida.


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
%moovida_plugins_good.prep -d %name-%version
%moovida_plugins_bad.prep -d %name-%version

%build
%moovida_plugins_bad.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%moovida_plugins_good.install -d %name-%version
%moovida_plugins_bad.install -d %name-%version

# move to verndor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages


%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/elisa/plugins/[a-z]*/i18n
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache

%postun
%restart_fmri desktop-mime-cache


%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/elisa
%{_libdir}/python%{pythonver}/vendor-packages/elisa_plugin_*-py%{pythonver}.egg-info
%{_libdir}/python%{pythonver}/vendor-packages/elisa_plugin_*-py%{pythonver}-nspkg.pth
%dir %attr (0755, root, sys) %{_datadir}

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

# endif for "ifnarch sparc"
%endif

%changelog
* Wed Jul 15 2009 - brian.cameron@sun.com
- Created 
