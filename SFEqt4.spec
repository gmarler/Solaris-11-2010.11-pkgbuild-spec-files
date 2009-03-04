#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEqt4
Summary:             Cross-platform development framework/toolkit
URL:                 http://trolltech.com/products/qt
License:             GPL v2
Version:             4.4.3
Source:              ftp://ftp.trolltech.com/qt/source/qt-x11-opensource-src-%{version}.tar.bz2
Source1:             qt4-solaris-cc-ss12
Patch1:              qt-01-use_bash.diff
Patch2:              qt4-02-misc_CC.diff

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWgccruntime
#FIXME: Requires: SUNWxorg-mesa
# Guarantee X/freetype environment concisely (hopefully):
Requires: SUNWGtku
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
%patch1 -p10
cd ..
%patch2 -p0
cd qt-x11-opensource-src-%version
cd mkspecs
cp -rp solaris-cc solaris-cc-ss12
cp %{SOURCE1}  solaris-cc-ss12/qmake.conf

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

##TODO## this might be omitted, if pkgbuild/environment was installed with SunStudio as default compiler
export CC=cc
export CXX=CC
##TODO## check build flags if they better be jds cbe default and make sure they are honored by configure
export CFLAGS=""
export CXXFLAGS="-library=stlport4"
export LDFLAGS="%_ldflags"

echo yes | ./configure -prefix %{_prefix} \
           -platform solaris-cc-ss12 \
           -docdir %{_docdir}/qt \
           -headerdir %{_includedir}/qt \
           -plugindir %{_libdir}/qt/plugins \
           -datadir %{_datadir}/qt \
           -translationdir %{_datadir}/qt/translations \
           -examplesdir %{_datadir}/qt/examples \
           -demosdir %{_datadir}/qt/demos \
           -no-exceptions \
           -sysconfdir %{_sysconfdir}

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
* Wed Mar 04 2009 - Thomas Wagner
- fix path to SunStudio compiler. Tested with SunStudioExpress November 2008 in /opt/SUNWspro/bin
- enable configure's hint -no-exceptions (smaller code, less memory)
* Sat Nov 29 2008 - dauphin@enst.fr
- Try to compile with studio12
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
