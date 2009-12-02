#
# spec file for package boost
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jchoi42
#

%define        major      1
%define        minor      40
%define        patchlevel 0
%define        ver_boost  %{major}_%{minor}_%{patchlevel}

Name:         boost
License:      Boost License Version
Group:        System/Libraries
Version:      %{major}.%{minor}.%{patchlevel}
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      boost - free peer-reviewed portable C++ source libraries
Source:       %{sf_download}/boost/boost_%{ver_boost}.tar.bz2

# date:2007-08-13 owner:trisk 
Patch1:       boost-01-studio.diff

# date:2007-08-13 owner:laca
Patch2:       boost-02-gcc34.diff

# date:2009-11-04 owner:sobi
Patch4:       boost-04-fixthread.diff

URL:          http://www.boost.org/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{name}_%{major}_%{minor}_%{patchlevel}
%patch1 -p1
%patch2 -p1
%patch4 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

BOOST_ROOT=`pwd`
%if %cc_is_gcc
TOOLSET=gcc
export CC=gcc
export CXX=g++
export CXXFLAGS="%gcc_cxx_optflags"
export LDFLAGS="%_ldflags"
%else
TOOLSET=sun
export CXXFLAGS="%cxx_optflags -library=stlport4 -staticlib=stlport4 -norunpath -features=tmplife -features=tmplrefstatic"
export LDFLAGS="%_ldflags -library=stlport4 -staticlib=stlport4"
%endif

#PYTHON_VERSION=`python -c "import sys; print (\"%%d.%%d\" %% (sys.version_info[0], sys.version_info[1]))"`
PYTHON_VERSION=`python -c 'import platform; print platform.python_version()' | cut -d '.' -f1-2`
PYTHON_ROOT=`python -c "import sys; print sys.prefix"`

# Overwrite user-config.jam
cat > user-config.jam <<EOF
# Compiler configuration
import toolset : using ;
%if %cc_is_gcc
using $TOOLSET : : $CXX : <cxxflags>"$CXXFLAGS" <linkflags>"$LDFLAGS" <linker-type>sun ;
%else
using $TOOLSET : : $CXX : <cxxflags>"$CXXFLAGS" <linkflags>"$LDFLAGS" ;
%endif

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


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Wed Dec 02 2009 - Albert Lee <trisk@opensolaris.org>
- Add patch4 from upstream for #2602
- Update URL
* Mon Oct 12 2009 - jchoi42@pha.jhu.edu
- Bump to 1.40.0, updated boost-01-studio patch
- Initial base spec
