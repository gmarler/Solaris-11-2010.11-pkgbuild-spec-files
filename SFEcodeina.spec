#
# spec file for package SFEcodeina
#
# includes module(s): codeina
#
# Copyright (c) 2008, 2010, Oracle and/or its affiliates. All rights reserved.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%define owner yippi
# bugdb: https://core.fluendo.com/gstreamer/trac/
#

%define OSR 10184:0.10.3.1

%include Solaris.inc

%define pythonver 2.6

Name:           SFEcodeina
IPS_package_name: codec/install/codeina
Meta(info.classification): %{classification_prefix}:Applications/Sound and Video
Summary:        Codec Installer
License:        GPL v3
Vendor:         fluendo.com
URL:            https://core.fluendo.com/gstreamer/trac/wiki/codeina
Version:        0.10.6
#FIXME: We should use the community official released source tarball
Source:         http://core.fluendo.com/gstreamer/src/codeina/codeina-%{version}.tar.bz2
#owner:yippi date:2008-11-06 type:branding
Patch1:         codeina-01-fixpython.diff
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/codeina-%{version}-build
Requires:       SUNWPython26
Requires:       SUNWgnome-python26-libs
# SUNWgnome-python-extras contains gtkmozembed.
Requires:       SUNWgnome-python26-extras
Requires:       SUNWgnome-media
Requires:       SUNWgst-python26
Requires:       SUNWpyyaml26
Requires:       SUNWpython26-notify
Requires:       SUNWpython26-twisted
Requires:       SUNWpython26-pyopenssl
Requires:       SUNWpython26-xdg
BuildRequires:  SUNWPython26-devel
BuildRequires:  SUNWgst-python26
BuildRequires:  SUNWpyyaml26
BuildRequires:  SUNWpython26-notify-devel
BuildRequires:  SUNWpython26-twisted
BuildRequires:  SUNWpython26-pyopenssl
BuildRequires:  SUNWpython26-xdg
BuildRequires:  SUNWpython26-setuptools

%include default-depend.inc

%description
Codeina functions as a codec installer for GStreamer applications.

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n codeina-%{version}
%patch1 -p1

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export PYTHON="/usr/bin/python%{pythonver}"
intltoolize --copy --force --automake
aclocal $ACLOCAL_FLAGS -I common/m4
autoconf
automake -a -c -f
./configure --prefix=%{_prefix} --sysconfdir=%{_sysconfdir}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Remove distro-specific files that do not apply to Solaris.
rm $RPM_BUILD_ROOT%{_datadir}/codeina/logo/mandrivalinux.png
rm $RPM_BUILD_ROOT%{_datadir}/codeina/logo/ubuntu.png
rm $RPM_BUILD_ROOT%{_sysconfdir}/codeina/providers/fedora*xml
rm $RPM_BUILD_ROOT%{_sysconfdir}/codeina/providers/mandrivalinux*xml
rm $RPM_BUILD_ROOT%{_sysconfdir}/codeina/providers/plf*xml
rm $RPM_BUILD_ROOT%{_sysconfdir}/codeina/providers/ubuntu*xml

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.pyo" -exec rm -f {} ';'

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -f $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z][a-z].omf
rm -f $RPM_BUILD_ROOT%{_datadir}/omf/*/*-??_??.omf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/codeina
%{_bindir}/codeina.bin
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/codeina.desktop
%dir %attr (0755, root, sys) %{_datadir}/autostart
%{_datadir}/autostart/*
%{_datadir}/codeina/*
%doc AUTHORS README common/m4/README
%doc(bzip2) COPYING NEWS
%doc(bzip2) ChangeLog common/ChangeLog
%doc(bzip2) po/ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc

%files root
%defattr(-, root, sys)
%attr(0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/codeina/*
%{_sysconfdir}/xdg/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
#FIXME: %dir %attr (0755, root, other) %{_datadir}/gnome
#FIXME: %{_datadir}/gnome/help/*/[a-z]*
#FIXME: %{_datadir}/omf/*/*-[a-z][a-z].omf
#FIXME: Not in 2.22.0:%{_datadir}/omf/*/*-[a-z][a-z]_[A-Z][A-Z].omf
%endif

%changelog
* Tue Nov 02 2010 - brian.cameron@oracle.com
- New spec file with version 0.10.6.

