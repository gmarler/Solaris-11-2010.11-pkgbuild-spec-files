#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%use boost = boost.spec

Name:                SFEboost-gpp
Summary:             Boost - free peer-reviewed portable C++ source libraries (g++-built)
Version:             %{boost.version}
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SUNWicu
BuildRequires: SUNWPython
Requires: SUNWicu

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%boost.prep -d %name-%version


%build

%boost.build -d %name-%version


%install
rm -rf $RPM_BUILD_ROOT
cd %{_builddir}/%name-%version/boost_%{boost.ver_boost}

mkdir -p $RPM_BUILD_ROOT%{_cxx_libdir}

for i in stage/lib/*.a; do
  cp $i $RPM_BUILD_ROOT%{_cxx_libdir}
done
for i in stage/lib/*.so; do
  NAME=`basename $i`
  cp $i $RPM_BUILD_ROOT%{_cxx_libdir}/$NAME.%{version}
  ln -s $NAME.%{version} $RPM_BUILD_ROOT%{_cxx_libdir}/$NAME
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_cxx_libdir}
%{_cxx_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_cxx_libdir}
%{_cxx_libdir}/lib*.a

%changelog
* Mon Oct 12 2009 - jchoi42@pha.jhu.edu
- changed %builddir, created base-specs/boost.spec
* Wed Apr 23 2008 - laca@sun.com
- create, based on SFEboost.spec
- force building with g++ and install the libs to /usr/lib/g++/<version>
* Thu Nov 22 2007 - daymobrew@users.sourceforge.net
- Comment out SUNWicud dependency to get module to build.
* Mon Aug 13 2007 - trisk@acm.jhu.edu
- Initial version
