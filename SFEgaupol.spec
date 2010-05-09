#
# spec file for package SFEgaupol
#
# Copyright 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#
# Note: On Solaris, this often chews up my X server. I can get it back by 
# logging in remotely and killing the application. So... it's not perfect, 
# but it's here as a stopgap until totem gains (stable) ass/ssa support.
# YMMV.


%include Solaris.inc

%include base.inc

Name:                    SFEgaupol
Summary:                 gaupol - subtitle editor
Version:                 0.15.1
Release:                 1
License:                 BSD
Group:                   Applications/Multimedia
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
URL:                     http://home.gna.org/gaupol
Source:                  http://download.gna.org/gaupol/0.15/gaupol-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-python26-libs
Requires: SUNWPython26
Requires: SFEgettext
BuildRequires: SUNWgnome-python26-libs-devel
BuildRequires: SUNWPython26-devel


%prep
%setup -q -n gaupol-%version

%build
# build!

%install
rm -rf $RPM_BUILD_ROOT
python2.6 setup.py clean install --prefix=$RPM_BUILD_ROOT/usr

rm $RPM_BUILD_ROOT/usr/share/applications/mimeinfo.cache

# Fix some annoying hardcoded paths
b=`echo $RPM_BUILD_ROOT | sed 's/\\//\\\\\\//g'` 
perl -pi -e 's/'$b'//g' $RPM_BUILD_ROOT/usr/lib/python2.6/site-packages/gaupol/paths.py


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_bindir}
%{_bindir}/gaupol
%{_mandir}/*
%dir %attr (0755, root, bin) %{_cxx_libdir}
%{_cxx_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gaupol/*
%attr (-, root, other) %{_datadir}/icons
%attr (-, root, other) %{_datadir}/locale
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/gaupol.desktop


%changelog
* Sat May 08 2010 - jchoi42@pha.jhu.edu
- initial spec
