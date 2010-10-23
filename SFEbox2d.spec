#
# Copyright 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
%include Solaris.inc

%define cc_is_gcc 1
%define pythonver 2.6
%include base.inc

Name:                SFEbox2d
Summary:             2D physics library
URL:                 http://www.box2d.org
Version:             2.1.2
Source:              http://box2d.googlecode.com/files/Box2D_v%{version}.zip
Patch1:              box2d-01-sun.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SFEfreeglut
BuildRequires: SFEfreeglut-devel
BuildRequires: SUNWcmake


%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n Box2D_v%{version}
%patch1 -p1
cd Box2D/Build
cmake -DBOX2D_INSTALL=ON -DBOX2D_BUILD_SHARED=ON ..

%build
cd Box2D/Build
make

%install
cd Box2D/Build
# Hack to work around bug #6860429, where cmake installs everything to sfw_stage
/bin/rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT%{_prefix}
ln -s $RPM_BUILD_ROOT%{_prefix} sfw_stage
make install

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/Box2D

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, other) %{_includedir}/Box2D
%{_includedir}/Box2D/*

%changelog
* Sat Oct 23 2010 - brian.cameron@oracle.com
- Initial spec based on 2.1.2.
