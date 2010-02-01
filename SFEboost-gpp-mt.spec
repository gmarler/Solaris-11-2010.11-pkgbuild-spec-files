#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define cc_is_gcc 1
%define boost_with_mt 1

%include base.inc

%use boost = boost.spec

Name:                SFEboost-gpp-mt
Summary:             Boost - free peer-reviewed portable C++ source libraries (g++-built) mt libs
Version:             %{boost.version}
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SUNWicud
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
* Fri Jan 29 2010 - Brian Cameron <brian.cameron@sun.com>
- Initial version of spec-file to build mt variants of boost libraries.
