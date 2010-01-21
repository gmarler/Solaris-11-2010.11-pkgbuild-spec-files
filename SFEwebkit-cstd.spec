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
Patch1:                  webkit-01-sun-studio-build-hack-noapache.diff
# owner:alfred date:2008-11-26 type:bug
Patch2:                  webkit-02-explicit-const.diff 
# owner:jouby date:2009-09-14 type:bug
Patch3:                  webkit-03-1.1.13-failed.diff
Patch4:                  webkit-04-1.1.14-new.diff
Patch5:                  webkit-06-17-noapache.diff
Patch6:                   webkit-07-17-new.diff
#Patch7:                   webkit-05-17-cstd.diff

SUNW_BaseDir:            %{_basedir}
# copyright place holder.
# TODO: add the WebKit copyright
SUNW_Copyright:          SFEwebkit.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
#Requires: SUNWlibstdcxx4
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
#Requires: SUNWlibstdcxx4
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
%patch6 -p1
#%patch7 -p1

%build
#export LD=CC
#export CPPFLAGS=`pkg-config --cflags-only-I libstdcxx4`
#export CXXFLAGS=`pkg-config --cflags-only-other libstdcxx4` 
#export LDFLAGS=`pkg-config --libs libstdcxx4`
export  LDFLAGS="%_ldflags -Wl,-zmuldefs"
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

make -j$CPUS
%install
rm -rf $RPM_BUILD_ROOT

cd webkit-%version
make install DESTDIR=$RPM_BUILD_ROOT
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
* Tue Jan 21 2010 - yuntong.jin@sun.com
- Initial version, webkit build with Cstd instead of apache stl stdcxx4
