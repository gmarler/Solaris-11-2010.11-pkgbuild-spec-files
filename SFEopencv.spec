#
# Copyright (c) 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: trisk
#
%include Solaris.inc

%define python_version 2.6
%define src_name OpenCV

Name:                SFEopencv
Summary:             OpenCV - Open Computer Vision Library
Version:             2.1.0
License:             BSD
Source:              %{sf_download}/opencvlibrary/files/%{src_name}-%{version}.tar.bz2
Patch1:              opencv-01-namespace.diff
Patch2:              opencv-02-stdc.diff
Patch3:              opencv-03-sunpro.diff
Patch4:              opencv-04-v4l2.diff
Patch5:              opencv-05-static.diff
URL:                 http://www.opencv.org/

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibC
Requires: SUNWlibms
Requires: SUNWpng
BuildRequires: SUNWpng-devel
Requires: SUNWjpg
BuildRequires: SUNWjpg-devel
Requires: SUNWTiff
BuildRequires: SUNWTiff-devel
Requires: SUNWPython26
Requires: SUNWPython26-extra
BuildRequires: SUNWcmake
BuildRequires: SUNWswig
%if %{?_without_gstreamer:0}%{?!_without_gstreamer:1}
Requires: SUNWglib2
BuildRequires: SUNWglib2-devel
Requires: SUNWgtk2
BuildRequires: SUNWgtk2-devel
Requires: SUNWgnome-media
BuildRequires: SUNWgnome-media-devel
%endif
%if %{?_with_ffmpeg:1}%{?!_with_ffmpeg:0}
Requires: SFEffmpeg
BuildRequires: SFEffmpeg-devel
%endif

%package devel
Summary:             %{summary} - development files
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CXX="$CXX -norunpath"
export CFLAGS="%{optflags} -mt -xlibmil -xlibmopt"
export CXXFLAGS="%{cxx_optflags} -mt -xlibmil -xlibmopt -features=tmplife"
export LDFLAGS="%{_ldflags} -lCrun -lCstd"
CMAKE_C_FLAGS_RELEASE="-xO4 -DNDEBUG" # override -xO2 from CMake
CMAKE_CXX_FLAGS_RELEASE="-xO4 -DNDEBUG" # override -xO2 from CMake

%ifarch i386 amd64
# Intel Integrated Performance Primitives
%if %{?_with_ipp:1}%{?!_with_ipp:0}
export CXXFLAGS="$CXXFLAGS -features=tmplrefstatic"
if [ -n "$IPP_PATH" ]; then
  for dir in /opt/intel/ipp/*/{ia,lp}32/sharedlib ""; do
    if [ -d "$dir" ]; then
      IPP_PATH=$dir
      break
    fi
done
fi
%endif
%endif

cmake	\
	-DCMAKE_C_FLAGS_RELEASE="$CMAKE_C_FLAGS_RELEASE"	\
	-DCMAKE_CXX_FLAGS_RELEASE="$CMAKE_CXX_FLAGS_RELEASE"	\
	-DCMAKE_INSTALL_PREFIX=%{_prefix}			\
	-DCMAKE_SKIP_RPATH=ON					\
	-DBUILD_SWIG_PYTHON_SUPPORT=ON				\
	-DBUILD_EXAMPLES=OFF					\
	-DBUILD_TESTS=OFF					\
	%{?_without_gstreamer:-DWITH_GSTREAMER=OFF}		\
	%{!?_with_ffmpeg:-DWITH_FFMPEG=OFF}			\
	-DWITH_1394=OFF						\
	-DWITH_JASPER=OFF					\
	%{?_with_ipp:-DUSE_IPP=ON}				\
	%{?_with_ipp:-DIPP_PATH="$IPP_PATH"}

# CR 6860429 cmake installs everything in ./sfw_stage - CMAKE_INSTALL_PREFIX is not used
find . -name Makefile | \
    xargs perl -pi -e 's,-D CMAKE_INSTALL_PREFIX=./sfw_stage/,,g'

make VERBOSE=1 -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# bug 329
cp cvconfig.h $RPM_BUILD_ROOT%{_includedir}/opencv/cvconfig.h

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages

# move (large) docs to docdir
mkdir -p $RPM_BUILD_ROOT%{_docdir}
mv $RPM_BUILD_ROOT%{_datadir}/opencv/doc \
   $RPM_BUILD_ROOT%{_docdir}/opencv

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}/vendor-packages
%{_libdir}/python%{python_version}/vendor-packages/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/opencv
%{_datadir}/opencv/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, other) %{_docdir}/opencv
%{_docdir}/opencv/*

%changelog
* Wed May 12 2010 - Albert Lee <trisk@opensolaris.org>
- Update compiler options
- Add support for Intel Integrated Performance Primitives
- Apply patch4
- Add patch5
* Sun May 09 2010 - Albert Lee <trisk@opensolaris.org>
- Initial spec
