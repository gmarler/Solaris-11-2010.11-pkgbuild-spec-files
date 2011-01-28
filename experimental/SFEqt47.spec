#
# spec file for package SFEqt47
#
# includes module: qt
#

# NOTE: Build with
# pkgtool build --patches=patches/qt47 experimental/SFEqt47.spec

# NOTE: This spec makes use of patches which are hard-coded to enable features
# of the Intel Nehalem processor, specifically, the SSE 4.2 instruction set.
# However, the enabling of these features is overriden in the call to configure
# below, to conform with the practice at SFE of assuming that an i386 CPU is not
# higher than Pentium.  Thus, if your CPU has a bigger feature set than a
# Pentium CPU, you should remove the corresponding flags in the call to
# configure.

# TODO: Autodetect CPU features and configure correspondingly.

# NOTE FOR USERS:
# If you want nice looking fonts with aliasing, you should create .fonts.conf in your homedir
# qt apps don't respect GNOME settings without KDE stuff installed
# Example .fonts.conf from my machine:
#<?xml version='1.0'?>
#<!DOCTYPE fontconfig SYSTEM 'fonts.dtd'>
#<fontconfig>
#    <match target="font" >
#        <edit mode="assign" name="hinting" >
#            <bool>true</bool>
#        </edit>
#    </match>
#
#    <match target="font" >
#        <edit mode="assign" name="antialias" >
#            <bool>true</bool>
#        </edit>
#

# NOTE: To build software using this library which uses qmake, use
# export PATH=$PATH:/usr/stdcxx/bin
# export QMAKESPEC=solaris-cc-stdcxx
# export QTDIR=/usr/stdcxx

%define _basedir /usr/stdcxx
%include Solaris.inc
%define srcname qt-everywhere-opensource-src

Name:                SFEqt47
Summary:             Cross-platform development framework/toolkit
URL:                 http://trolltech.com/products/qt
License:             LGPLv2
Version:             4.7.1
Source:              ftp://ftp.trolltech.com/qt/source/%srcname-%version.tar.gz
Source1:	     qmake.conf
Patch1:		     qt471-01-configure-ext.diff
Patch2:		     qt471-02-ext.diff
Patch3:		     qt471-03-ext2.diff
Patch4:		     qt471-04-sse42.diff
#These patches are stolen from KDE guys and affect WebKit 
#(I'm not first who stole them, most of them are stolen from cvsdude old repo)
Patch5:		     webkit01-17.diff
Patch6:		     webkit04-17.diff
Patch7:		     webkit05-17.diff
Patch8:		     webkit08-17.diff
Patch9:		     webkit10-17.diff
Patch10:	     webkit11-17.diff
Patch11:	     webkit13-17.diff
Patch12:	     webkit14-17.diff
Patch13:	     webkit15-17.diff
Patch14:	     webkit16-17.diff
Patch15:	     webkit17-17.diff
#These don't affect Webkit, I've decided they are nice and steal from KDE guys
Patch16:	     qt-fastmalloc.diff
Patch17:	     qt-align.diff 
Patch18:	     qt-qglobal.diff
Patch19:	     qt-4.6.2-iconv-XPG5.diff
Patch20: 	     qt-thread.diff
Patch21:	     qt-arch.diff 
Patch22:	     qt-4.6.2-webkit-CSSComputedStyleDeclaration.cpp.221.diff
Patch23:	     qt-4.6.2-networkaccessmanager.cpp.233.diff
Patch24:	     qt-4.7.0-webkit-runtime_array.h.234.diff
Patch25:	     qt-MathExtras.diff
Patch26:	     qt-webkit-exceptioncode.diff 
Patch27:	     qt-uistring.diff 
Patch28:	     template.diff 
Patch29:	     plugin-loader.diff 
Patch30:	     qt-qxmlquery.cpp.diff
Patch31:	     qt-clucene.diff 
Patch32:	     qt-configure-iconv.diff 
Patch33:	     qt-4.6.2-iconv.diff
Patch34:	     qt-qmutex_unix.cpp.diff
#These exclusive to SFE
Patch35:	     qt471-05-pluginqlib.diff
Patch36:	     qt-4.7.1-webkit-jscore-munmap.diff
Patch37:	     qt-4.7.1-webkit-jsc-wts-systemalloc.diff
Patch38:	     qt-4.7.1-mathextras.diff
Patch39: 	     qt-4.7.1-qiconvcodec.diff
Patch40:	     qt-471-shm.diff 
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SUNWlibstdcxx4
Requires: SUNWlibstdcxx4

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
%setup -q -n %{srcname}-%version
# Don't pass --fuzz=0 to patch
%define _patch_options --unified
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p0
%patch18 -p1
%patch19 -p1
%patch20 -p0
%patch21 -p0
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p0
%patch26 -p0
%patch27 -p0
%patch28 -p0
%patch29 -p0
%patch30 -p0
%patch31 -p0
%patch32 -p0
%patch33 -p0
%patch34 -p1
%patch35 -p0
%patch36 -p0
%patch37 -p0
%patch38 -p0
%patch39 -p0
%patch40 -p0


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags -library=stdcxx4 -I/usr/lib/dbus-1.0/include -I/usr/include/libpng14 -features=extensions,nestedaccess,tmplrefstatic -xalias_level=compatible"
export LDFLAGS="%_ldflags -library=stdcxx4"


# 4.6.3 runs into trouble with examples, so disable examples and demos.
# 4.7.0 runs into trouble with phonon, so don't build that.

# Assume i386 CPU is not higher than Pentium
echo yes | ./configure -prefix %{_prefix} \
           -no-sse -nosse2 -no-sse3 -no-ssse3 -no-sse4.1 -no-sse4.2 \
           -platform solaris-cc \
           -opensource \
           -docdir %{_docdir}/qt \
           -headerdir %{_includedir}/qt \
           -plugindir %{_libdir}/qt/plugins \
           -datadir %{_datadir}/qt \
           -translationdir %{_datadir}/qt/translations \
           -nomake examples \
           -nomake demos \
           -no-phonon \
           -no-phonon-backend \
           -no-exceptions \
           -sysconfdir %{_sysconfdir}

# Elliminate -Winline, which Solaris Studio 12.2 rejects
cd src/gui
sed 's/ -Winline//' Makefile > Makefile.fixed
mv Makefile.fixed Makefile
cd ../..
	   
gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

gmake install INSTALL_ROOT=$RPM_BUILD_ROOT

rm ${RPM_BUILD_ROOT}%{_libdir}/*.*a

# Eliminate QML imports stuff for now:
# Who is Nokia to create a new subdirectary in /usr?
rm -r ${RPM_BUILD_ROOT}%_prefix/imports

# Create qmake.conf for building against this library
cd ${RPM_BUILD_ROOT}%_datadir/qt/mkspecs
mkdir solaris-cc-stdcxx
cd solaris-cc-stdcxx
install %SOURCE1 .
cp -p ../solaris-cc-stlport/qplatformdefs.h .

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
* Thu Jan 27 2011 - Alex Viskovatoff
- Use -library=stdcxx4 instead of include/stdcxx.inc
- Install in /usr/stdcxx (no longer conflicting with SFEqt4)
* Dec 10 2010 - Alex Viskovatoff
- Add 40 patches supplied by russiane39 which enable WebKit among other things.
- Install qmake.conf file for solaris-cc-stdcxx
* Nov 11 2010 - Alex Viskovatoff
- Fork SFEqt47.spec off SFEqt4.spec, disregarding stlport and snv < 147
- To make the build work, disable examples and phonon.  Disable demos
  because that is what kde-solaris does.
* Nov  4 2010 - Alex Viskovatoff
- Spec needs "%include osdistro.inc" (pointed out by Thomas Wagner)
* Nov  3 2010 - Alex Viskovatoff
- Add patch by Milan Jurik to use new libpng names only for osbuild >= 147
- Use cxx_optflags
* Oct 16 2010 - Alex Viskovatoff
- Fix broken use of stlport: if -library=stlport4 is passed to the compiler,
  it must also be passed to the linker
- Update to version 4.5.3, obviating the need for the existing patches
- Add a patch to use changed field names in libpng-1.4
- Use stdcxx instead of stlport, while allowing use of the deprecated
  stlport as an option. (BionicMutton uses stdcxx.)
- Remove dependency on SUNWgccruntime
* Mar 07 2009 - Thomas Wagner
- rework shared patch qt-01-use_bash.diff (to be more independent of qt version SFEqt SFEqt4 in verison 4.x / 4.5)
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
