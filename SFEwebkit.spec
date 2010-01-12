# spec file for package SFEwebkit
#
#
# includes module(s): webkit
#
%include Solaris.inc

#we are on OpenSolaris (or on SXCE or Solaris 10)
%define OS2nnn %( egrep "OpenSolaris 20[0-9][0-9]" /etc/release > /dev/null  && echo 1 || echo 0) 

Name:                    SFEwebkit
Summary:                 WetKit, an open source web browser engine that's used by Safari, Dashboard, Mail, and many other OS X applications.
Version:                 1.1.17
Source:                  http://www.webkitgtk.org/webkit-%{version}.tar.gz
URL:                     http://www.webkitgtk.org/

# owner:alfred date:2008-11-26 type:bug
Patch1:                  webkit-01-sun-studio-build-hack.diff
# owner:alfred date:2008-11-26 type:bug
Patch2:                  webkit-02-explicit-const.diff
# owner:jouby date:2009-09-14 type:bug
Patch3:                  webkit-03-1.1.13-failed.diff
Patch4:                  webkit-04-1.1.14-new.diff
Patch5:                  webkit-07-17-new.diff

SUNW_BaseDir:            %{_basedir}
# copyright place holder.
# TODO: add the WebKit copyright
SUNW_Copyright:          SFEwebkit.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibstdcxx4
Requires: SUNWcurl
Requires: SUNWgnome-spell
Requires: SUNWopenssl
Requires: SUNWgnome-spell
Requires: SUNWgnu-idn
Requires: SUNWgnome-base-libs
Requires: SUNWicu
Requires: SUNWlxml

%if %OS2nnn
Requires: SUNWopenssl
%else
BuildRequires: SUNWopenssl-include
Requires: SUNWopenssl-libraries
%endif

#Requires: SUNWpr
Requires: SUNWsqlite3
#Requires: SUNWtls
Requires: SUNWzlib
BuildRequires: SUNWgcc
BuildRequires: SUNWicud

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWlibstdcxx4
Requires: SUNWcurl
Requires: SUNWgnu-idn
Requires: SUNWgnome-base-libs
Requires: SUNWicu
Requires: SUNWlxml
#Requires: SUNWpr
Requires: SUNWsqlite3
#Requires: SUNWtls
Requires: SUNWzlib
BuildRequires: SUNWgcc

%prep
%setup -q -n %name-%version -c -a0
cd webkit-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
export LD=CC
export CPPFLAGS=`pkg-config --cflags-only-I libstdcxx4`
export CXXFLAGS=`pkg-config --cflags-only-other libstdcxx4` 
export LDFLAGS="`pkg-config --libs libstdcxx4` -Wl,-zmuldefs" 
cd webkit-%version

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi 
aclocal -I autotools
automake -a -c -f
autoconf 
./configure --prefix=%{_prefix}			\
	    --libdir=%{_libdir}         \
            --sysconfdir=%{_sysconfdir}         \
	    --mandir=%{_mandir}                 \
	    --datadir=%{_datadir}               \
            --infodir=%{_datadir}/info  

sed '/CCLD =/s/(CC)/(CXX)/g' GNUmakefile > GNUmakefile.tmp 
mv GNUmakefile.tmp GNUmakefile 

make  -j$CPUS
%install
rm -rf $RPM_BUILD_ROOT

cd webkit-%version
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'                                                                                                                                                                             
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%if %build_l10n
%else
#REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libwebkit*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/webkit-1.0/*
#%doc -d webkit-%{Version} ChangeLog README

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_prefix}/include
%{_prefix}/include/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %dir %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif


%changelog
* Tue Jan 12 2009 - yuntong.jin@sun.com
  Remove *.la *.a file which will brings -library=no%Cstd dependency for
applications likedevhelp  
* Tue Jan 12 2009 - yuntong.jin@sun.com
  Bump to 1.1.17
* Mon Dec 28 2009 - yuntong.jin@sun.com
 add copyright file
* Wen Sep 23 2009 - yuntong.jin@sun.com
- Bump to 1.1.14
* Sat Aug 15 2009 - Thomas Wagner
- bump version to 1.1.12
- fix dependencies for SXCE and OS200[89].xx (Build)Requires: SUNWopenssl-include/SUNWopenssl-libraries
* Thu Aug 13 2009 - alfred.peng@sun.com
- trivial fix for source setup (a1 -> a0).
* Fri Jun 19 2009 - alfred.peng@sun.com
- Bump to webkitgtk 1.1.10 release, rework the patches.
* Web Jun 03 2009 - chris.wang@sun.com
- Update to webkitgtk 1.1.7 release, regenerated all patches, 
  change required package to SUNWlibstdcxx4, and reformatted 
  the spec file
* Wed Dec 03 2008 - alfred.peng@sun.com
- Re-arrange the development headers, pc and library.
  Verified to work with the latest 0.22 devhelp release.
* Wed Nov 26 2008 - alfred.peng@sun.com
- Initial version
