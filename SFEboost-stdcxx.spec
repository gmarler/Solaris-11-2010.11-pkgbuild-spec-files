#
# spec file for package: [pkg name]
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s): [pkg module(s)]
#
%include Solaris.inc
%include stdcxx.inc

%define _prefix /usr/stdcxx
%define _libdir %{_prefix}/lib
%define _includedir %{_prefix}/include
%define _datadir %{_prefix}/share
%define _docdir %{_datadir}/doc

%define        major      1
%define        minor      40
%define        patchlevel 0
%define src_url http://easynews.dl.sourceforge.net/sourceforge/boost

Name:                SFEboost-stdcxx
Summary:             Boost - free peer-reviewed portable C++ source libraries
Version:             %{major}.%{minor}.%{patchlevel}
License:             Boost Software License
Source:              %{src_url}/boost_%{major}_%{minor}_%{patchlevel}.tar.bz2
Patch1:              boost-01-studio.diff
Patch2:              boost-02-gcc34.diff
Patch3:              boost-03-fixinclude.diff
Patch4:              boost-04-fixthread.diff
URL:                 http://www.boost.org/

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWicu
BuildRequires: SUNWicud
BuildRequires: SUNWPython
Requires: SUNWicu
Requires: SFEstdcxx

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc

%prep
%setup -q -n boost_%{major}_%{minor}_%{patchlevel}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CXXFLAGS="%cxx_optflags -library=%none -staticlib=%none -norunpath -features=tmplife -features=tmplrefstatic -L%{stdcxx_lib} -R%{stdcxx_lib} -I%{stdcxx_include} -lstd -lm -UBOOST_DISABLE_THREADS -DBOOST_HAS_THREADS=1 -DBOOST_HAS_PTHREADS=1 -UBOOST_NO_STD_ITERATOR_TRAITS -UBOOST_NO_TEMPLATE_PARTIAL_SPECIALIZATION -DHAVE_ICU=1 -DBOOST_HAS_ICU=1 -UBOOST_NO_STDC_NAMESPACE -DSUNPROCC_BOOST_COMPILE=1 -UBOOST_NO_STDC_NAMESPACE -DSUNPROCC_BOOST_COMPILE=1 -DPy_TRACE_REFS -DPy_USING_UNICODE"
export LDFLAGS="-library=%none -staticlib=%none -L%{stdcxx_dir} -R%{stdcxx_dir}"

BOOST_ROOT=`pwd`
TOOLSET=sun
PYTHON_VERSION=`python -c "import sys; print (\"%%d.%%d\" %% (sys.version_info[0], sys.version_info[1]))"`
PYTHON_ROOT=`python -c "import sys; print sys.prefix"`

# Overwrite user-config.jam
cat > user-config.jam <<EOF
# Compiler configuration
import toolset : using ;
using $TOOLSET : : $CXX : <cxxflags>"$CXXFLAGS" <linkflags>"$LDFLAGS" ; 

# Python configuration
using python : $PYTHON_VERSION : $PYTHON_ROOT ;
EOF

# Build bjam
cd "tools/jam/src" && ./build.sh "$TOOLSET"
cd $BOOST_ROOT

# Build Boost
BJAM=`find tools/jam/src -name bjam -a -type f`
$BJAM --v2 -j$CPUS -sBUILD="release <threading>single/multi" -sICU_PATH=/usr \
  --layout=system --user-config=user-config.jam release stage

%install
BOOST_ROOT=`pwd`
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}
mkdir -p $RPM_BUILD_ROOT%{_docdir}
mkdir -p $RPM_BUILD_ROOT%{_docdir}/boost-%{version}

for i in stage/lib/*.a; do
  cp $i $RPM_BUILD_ROOT%{_libdir}
done
for i in stage/lib/*.so; do
  NAME=`basename $i`
  cp $i $RPM_BUILD_ROOT%{_libdir}/$NAME.%{version}
  ln -s $NAME.%{version} $RPM_BUILD_ROOT%{_libdir}/$NAME
done

for i in `find "boost" -type d`; do
  mkdir -p $RPM_BUILD_ROOT%{_includedir}/$i
done
for i in `find "boost" -type f`; do
  cp $i $RPM_BUILD_ROOT%{_includedir}/$i
done

cd "doc/html"
for i in `find . -type d`; do
  mkdir -p $RPM_BUILD_ROOT%{_docdir}/boost-%{version}/$i
done
for i in `find . -type f`; do
  cp $i $RPM_BUILD_ROOT%{_docdir}/boost-%{version}/$i
done
cd $BOOST_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.a
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/boost
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, other) %{_docdir}/boost-%{version}
%{_docdir}/boost-%{version}/*

%changelog
* Wed Nov 04 2009 - sobotkap@gmail.com
- Bump version to 1.40.0
* Tue Oct 06 2009 - sobotkap@gmail.com
- Uncomment SUNWicud and add cpp flags for stdcxx.
* Thu Nov 22 2007 - daymobrew@users.sourceforge.net
- Comment out SUNWicud dependency to get module to build.
* Mon Aug 13 2007 - trisk@acm.jhu.edu
- Initial version
