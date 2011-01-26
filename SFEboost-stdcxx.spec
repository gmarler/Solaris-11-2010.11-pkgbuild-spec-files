#
# spec file for package: [pkg name]
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s): [pkg module(s)]
#
%define _basedir /usr/stdcxx
%include Solaris.inc
%include stdcxx.inc

%define		major	1
%define		minor	45
%define		patchlevel 0
%define		src_url	http://easynews.dl.sourceforge.net/sourceforge/boost

Name:		SFEboost-stdcxx
Summary:	Boost - free peer-reviewed portable C++ source libraries
Version:	%{major}.%{minor}.%{patchlevel}
License:	Boost Software License
URL:		http://www.boost.org/
Source:		%{src_url}/boost_%{major}_%{minor}_%{patchlevel}.tar.bz2
Patch0:		boost-stdcxx-00-sun-jam.diff
# These are from http://solaris.bionicmutton.org/hg/kde4-specs-460/raw-file/243b8041ba78/specs/patches/boost
Patch1:		boost-stdcxx-01-solaris.diff
Patch2:		boost-stdcxx-02-typenames.diff
Patch3:		boost-stdcxx-03-python.diff
Patch4:		boost-stdcxx-04-transform-width-min.diff
Patch5:		boost-stdcxx-05-graphviz.diff
Patch6:		boost-stdcxx-06-stdcxx.diff

SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEicu-devel
BuildRequires: SUNWPython
Requires: SFEicu
Requires: SUNWlibstdcxx4

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc

%prep
%setup -q -n boost_%{major}_%{minor}_%{patchlevel}
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p1
%patch4	
%patch5	
%patch6

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CXXFLAGS="%stdcxx_cxxflags -features=tmplrefstatic -UBOOST_DISABLE_THREADS -DBOOST_HAS_THREADS=1 -DBOOST_HAS_PTHREADS=1 -UBOOST_NO_STD_ITERATOR_TRAITS -UBOOST_NO_TEMPLATE_PARTIAL_SPECIALIZATION -DHAVE_ICU=1 -DBOOST_HAS_ICU=1 -UBOOST_NO_STDC_NAMESPACE -DSUNPROCC_BOOST_COMPILE=1 -DSUNPROCC_BOOST_COMPILE=1 -DPy_USING_UNICODE -D_XOPEN_SOURCE=500 -D__EXTENSIONS__ -erroff"
export LDFLAGS="%stdcxx_ldflags"

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
%define bjamdir tools/build/v2/engine/src
cd "%bjamdir" && ./build.sh "$TOOLSET"
cd $BOOST_ROOT

for i in tools/**/*.jam tools/**/*.py
do
  sed -i -e 's,stlport,stdcxx,g' $i
done
sed -i -e 's,stlport,stdcxx,g' Jamroot


# Build Boost
BJAM=`find %bjamdir -name bjam -a -type f`
$BJAM --v2 -j$CPUS -sBUILD="release <threading>single/multi" -sICU_PATH=/usr/stdcxx \
  --layout=system --user-config=user-config.jam release stage

%install
BOOST_ROOT=`pwd`
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}
mkdir -p $RPM_BUILD_ROOT%{_docdir}
mkdir -p $RPM_BUILD_ROOT%{_docdir}/boost-%{version}

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
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/boost
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, other) %{_docdir}/boost-%{version}
%{_docdir}/boost-%{version}/*

%changelog
* Wed Jan 26 2011 - Alex Viskovatoff
- Clean up CXXFLAGS
* Mon Jan 24 2011 - Alex Viskovatoff
- Use patches from KDE Solaris (other than the patch for sun.jam), to avoid
  duplication of effort
- Add -D_XOPEN_SOURCE=500 -D__EXTENSIONS__ to CXXFLAGS to make all targets build
- Create and use "feature.extend stdlib : sun-stdcxx" in sun.jam
* Sun Nov 28 2010 - Alex Viskovatoff
- Update to 1.45
- Remove -DPy_TRACE_REFS from CXXFLAGS, since it makes libboost_python.so
  incompatible with libpython2.6.so
* Sat Nov 20 2010 - Alex Viskovatoff
- Bump to 1.44 (filesystem library does not get built with 1.43)
- Use SFEicu, since library/icu is built against libcStd
- Use %stdcxx_cxxflags and %stdcxx_ldflags
- Do not package static libs
* Sat Aug 07 2010 - sobotkap@gmail.com
- Add patch to not link with stlport4
* Sun May 16 2010 - sobotkap@gmail.com
- Bump version to 1.43
* Wed Nov 04 2009 - sobotkap@gmail.com
- Bump version to 1.40.0
* Tue Oct 06 2009 - sobotkap@gmail.com
- Uncomment SUNWicud and add cpp flags for stdcxx.
* Thu Nov 22 2007 - daymobrew@users.sourceforge.net
- Comment out SUNWicud dependency to get module to build.
* Mon Aug 13 2007 - trisk@acm.jhu.edu
- Initial version
