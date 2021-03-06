#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define cc_is_gcc 1

Name:                SFEqt
Summary:             Cross-platform development framework/toolkit
URL:                 http://trolltech.com/products/qt
License:             GPL v2
Version:             4.4.3
Source:              ftp://ftp.trolltech.com/qt/source/qt-x11-opensource-src-%{version}.tar.bz2
Patch1:              qt-01-use_bash.diff
Patch2:              qt-02-libpng.diff

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWgccruntime
BuildRequires: SUNWgcc
#FIXME: Requires: SUNWxorg-mesa
# Guarantee X/freetype environment concisely (hopefully):
Requires: SUNWxwplt
# The above bring in many things, including SUNWxwice and SUNWzlib
Requires: SUNWxwxft
# The above also pulls in SUNWfreetype2

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n qt-x11-opensource-src-%version
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="-O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointer"
export CXXFLAGS="%gcc_cxx_optflags"
export LDFLAGS="%_ldflags"

echo yes | ./configure -prefix %{_prefix} \
           -platform solaris-g++ \
           -docdir %{_docdir}/qt \
           -headerdir %{_includedir}/qt \
           -plugindir %{_libdir}/qt/plugins \
           -datadir %{_datadir}/qt \
           -translationdir %{_datadir}/qt/translations \
           -examplesdir %{_datadir}/qt/examples \
           -demosdir %{_datadir}/qt/demos \
           -sysconfdir %{_sysconfdir} \
           -no-exceptions \
           -no-webkit \
           -L /usr/gnu/lib \
           -R /usr/gnu/lib 

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install INSTALL_ROOT=$RPM_BUILD_ROOT

rm ${RPM_BUILD_ROOT}%{_libdir}/*.la
rm ${RPM_BUILD_ROOT}%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/lib*.prl
%dir %attr (0755, root, bin) %{_libdir}/qt
%{_libdir}/qt/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/qt


%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, other) %{_includedir}/qt
%{_includedir}/qt/*
%dir %attr (0755, root, bin) %dir %{_libdir} 
%dir %attr (0755, root, other) %{_libdir}/pkgconfig 
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Wed Mar 10 2010 - Brian Cameron
- Add -no-webkit to configure, otherwise the linker crashes.
  Looks like this will go away when binutils is updated to 2.21 (which is not
  yet released).  Refer:
  http://bugs.gentoo.org/show_bug.cgi?id=295765
* Tue Feb 02 2010 - Brian Cameron
- Fix spec-file so it builds.  Now use define cc_is_gcc, for example.
* Mar 07 2009 - Thomas Wagner
- rework shared patch qt-01-use_bash.diff (to be more independent of qt version
  SFEqt SFEqt4 in verison 4.x / 4.5)
* Wed Mar 04 2009 - Thomas Wagner
- can't find libcstd++.6.*, add to configure:
  -L /usr/gnu/lib -R /usr/gnu/lib (gcc4, for gcc3 this would be sfw instead
  gnu)
- enable configure's hint -no-exceptions (smaller code, less memory)
- force to SFEgcc 4.x because sfw/gcc3 failed to compile
  qdrawhelper_mmx3dnow.cpp with missing mm3dnow.h (to be found only in gcc4)
  (change Requires from SUNWgccruntime to SFEgcc(runtime),
   <CC|CXX>=/usr/gnu/bin/<gcc|g++>)
  ##TODO## is this a failure of configure/something else to depend on a *.h not
  present?
* Mon Nov 24 2008 - alexander@skwar.name
- Add qt-01-use_bash.diff, which replaces all calls to sh with bash,
  because Qt won't build when sh isn't bash.
  Cf. http://markmail.org/message/hzb3fypsc5sopf2b ff. and there
  http://markmail.org/message/l7yleonbjqnl7nfv
- Remove tarball_version - version is good enough
* Sun Nov 11 2008 - dick@nagual.nl
- Bump to 4.4.3
* Sun Sep 21 2008 - dick@nagual.nl
- Bump to 4.4.2
* Tue May 13 2008 - nonsea@users.sourceforge.net
- Bump to 4.4.0
* Fri Mar 21 2008 - nonsea@users.sourceforge.net
- Bump to 4.4.0-rc1
- Remove upstreamed patch time.diff
* Fri Mar 21 2008 - nonsea@users.sourceforge.net
- Bump to 4.4.0-beta1, and update %files
- Add patch time.diff
* Mon Mar 19 2007 - dougs@truemail.co.th
- Fixed -fno-omit-frame-pointer flag
- Bump to 4.2.3
* Thu Dec 07 2006 - Eric Boutilier
- Initial spec
