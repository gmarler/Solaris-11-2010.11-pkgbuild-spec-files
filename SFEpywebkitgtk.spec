#
# spec file for package SFEpywebkitgtk.spec
#
# includes module(s): pywebkitgtk
#
%define owner: jouby
#

%include Solaris.inc

%define pythonver 2.6

Name:           pywebkitgtk
Version:        1.1.6
Summary:        Python Bindings for WebKit-gtk
SUNW_BaseDir:   %{_basedir}
SUNW_Copyright: SFEpywebkitgtk.copyright
Group:          Development/Languages
License:        GPLv2+
URL:            http://code.google.com/p/pywebkitgtk/
Source0:        http://pywebkitgtk.googlecode.com/files/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

#BuildRequire
Requires:       SUNWgnome-python26-libs
BuildRequires: SUNWPython26-devel
Requires: SUNWPython26

%description
GTK WebKit bindings for Python.

%prep
rm -rf %name-%version
mkdir -p %name-%version

%setup -q -n %name-%version

%build
./configure --prefix=%{_prefix}
make PYGTK_CODEGEN=pygobject-codegen-2.0

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT \( -name \*.la -o -name \*.a \) -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%attr(755,root,root) %{_libdir}/python%{pythonver}/site-packages/webkit-1.0/webkit.so

%dir %attr (0755, root, sys) %{_datadir}
%dir %{_datadir}/pywebkitgtk
%dir %{_datadir}/pywebkitgtk/defs
%{_datadir}/pywebkitgtk/defs/webkit*.defs

%doc AUTHORS ChangeLog COPYING MAINTAINERS NEWS README

%changelog
* Fri Apl 23 2010 yuntong.- jin@sun.com
- Init spec file
