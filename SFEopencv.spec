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
URL:                 http://www.opencv.org/

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibC
Requires: SUNWzlib
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

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CXX="$CXX -norunpath"
export CFLAGS="%{optflags}"
export CXXFLAGS="%{cxx_optflags}"
export LDFLAGS="%{_ldflags} -lCrun -lCstd"

cmake	\
	-DCMAKE_INSTALL_PREFIX=%{_prefix}		\
	-DCMAKE_SKIP_RPATH=1				\
	-DBUILD_SWIG_PYTHON_SUPPORT=1			\
	-DBUILD_EXAMPLES=0				\
	-DBUILD_TESTS=0				\
	%{?_without_gstreamer:-DWITH_GSTREAMER=0}	\
	%{!?_with_ffmpeg:-DWITH_FFMPEG=0}		\
	-DWITH_1394=0					\
	-DWITH_JASPER=0

make VERBOSE=1 -j$CPUS

# CR 6860429 cmake installs everything in ./sfw_stage - CMAKE_INSTALL_PREFIX is not used
find . -name Makefile | \
    xargs perl -pi -e 's,-D CMAKE_INSTALL_PREFIX=./sfw_stage/,,g'

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
* Sun May 09 2010 - Albert Lee <trisk@opensolaris.org>
- Initial spec
