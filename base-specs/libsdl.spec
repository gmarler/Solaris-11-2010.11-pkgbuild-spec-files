#
# spec file for package libsdl
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: davelam
#
Name:         libsdl
License:      LGPL
Group:        System/Libraries
Version:      1.2.14
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      libsdl - Simple DirectMedia Layer
Source:       http://www.libsdl.org/release/SDL-%{version}.tar.gz
Patch1:	      libsdl-01-AUXDIR.diff
Patch3:	      libsdl-03-sunpro.diff
URL:          http://www.libsdl.org/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on

%description
Simple DirectMedia Layer is a cross-platform multimedia library designed to
provide low level access to audio, keyboard, mouse, joystick, 3D hardware via
OpenGL, and 2D video framebuffer. It is used by MPEG playback software,
emulators, and many popular games.

%package devel
Summary: Headers for developing programs that will use libsdl
Group:      Development/Libraries
Requires:   %{name}

%description   devel
This package contains the headers that programmers will need to develop
applications which will use libsdl.

%prep
%setup -q -n SDL-%{version}
%patch1 -p1
%patch3 -p1

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

libtoolize --force
aclocal
autoconf --force

export CPPFLAGS="-I/usr/X11/include"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure \
	--prefix=%{_prefix}		\
        --libdir=%{_libdir}		\
        --bindir=%{_bindir}		\
	--mandir=%{_mandir}		\
	--sysconfdir=%{_sysconfdir}	\
        --with-esd-prefix=%{_prefix}	\
	--disable-alsa			\
        --enable-joystick               \
	%nasm_option

%if %arch_sse2
# allow relocations against non-writeable sections - needed for nasm code
printf "/-z text/\ns/-z text/-z textoff/\nw\nq\n" | ex - libtool
%endif

make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

# delete libtool .la files and static libs
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr (-, root, root)
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root)
%{_libdir}/*.so

%changelog
* Tue Mar  2 2010 - matt@greenviolet.net
- Bump version to 1.2.14
* Wed Aug 15 2007 - trisk@acm.jhu.edu
- Bump to 1.2.12
- Drop libsdl-02-rpath.diff: applied upstream 
* Wed Jul 15 2007 - dougs@truemail.co.th
- added --disable-alsa
* Tue Jun  5 2007 - dougs@truemail.co.th
- Initial version, modified from spec-files
