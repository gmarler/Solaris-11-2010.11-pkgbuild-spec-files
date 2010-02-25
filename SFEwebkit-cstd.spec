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
Version:                 1.1.19
Source:                  http://www.webkitgtk.org/webkit-%{version}.tar.gz
URL:                     http://www.webkitgtk.org/

# owner:jouby date:2010-01-25 type:bug
Patch1:                 webkit-01-configure-and-makefile.diff
Patch2:                 webkit-02-mmap.diff
Patch3:                 webkit-03-return.diff
Patch4:                 webkit-04-make-pair.diff
Patch5:                 webkit-05-ustring.diff
Patch6:                 webkit-06-wtf-compiler-suncc.diff
Patch7:                 webkit-07-wtf-aligned.diff
Patch8:                 webkit-08-svgpodlist.diff
Patch9:                 webkit-09-ternary-operator.diff
Patch10:                 webkit-10-pow.diff
Patch11:                 webkit-11-g-byte-order-marco.diff
Patch12:                 webkit-12-isnan.diff
Patch13:                 webkit-13-webcore-frame.diff
Patch14:                 webkit-14-extern-c.diff
Patch15:                 webkit-15-static.diff
Patch16:                 webkit-16-const-string.diff
Patch17:                 webkit-17-make-pair-range.diff
Patch18:                 webkit-18-locale-h.diff
Patch19:                 webkit-19-ss12-ternary-operator.diff
Patch20:                 webkit-20-visibility.diff
Patch21:                 webkit-21-vector-not-const.diff
Patch22:                 webkit-22-not-reinterpretcast.diff
Patch23:                 webkit-23-a11y-34463.diff
Patch24:                 webkit-24-a11y-35169.diff

SUNW_BaseDir:            %{_basedir}
# copyright place holder.
# TODO: add the WebKit copyright
SUNW_Copyright:          SFEwebkit.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWcurl
Requires: SUNWgnome-spell
Requires: SUNWopenssl
Requires: SUNWgnu-idn
Requires: SUNWgnome-base-libs
Requires: SUNWicu
Requires: SUNWlxml
Requires: SUNWsqlite3
Requires: SUNWzlib
Requires: SUNWlibsoup

BuildRequires: SUNWicud
BuildRequires: SUNWgnu-gettext
BuildRequires: SUNWgnu-gperf

%if %OS2nnn
Requires: SUNWopenssl
%else
BuildRequires: SUNWopenssl-include
Requires: SUNWopenssl-libraries
%endif



%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc


%prep
%setup -q -n %name-%version -c -a0
cd webkit-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
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
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1

%build
#export LD=CC
#export CPPFLAGS=`pkg-config --cflags-only-I libstdcxx4`
#export CXXFLAGS=`pkg-config --cflags-only-other libstdcxx4` 
#export LDFLAGS=`pkg-config --libs libstdcxx4`
#export CPPFLAGS="-D__FUNCTION__=__func__"
#export CXXFLAGS="%cxx_optflags -features=extensions"
#export  LDFLAGS="%_ldflags -Wl,-zmuldefs"
cd webkit-%version

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi 
#aclocal -I autotools
#automake -a -c -f
#autom4te=/usr/bin/autom4te
#automake-1.10
autoconf 
./configure --prefix=%{_prefix}			\
            --disable-jit                       \
	    --libdir=%{_libdir}                 \
            --sysconfdir=%{_sysconfdir}         \
	    --mandir=%{_mandir}                 \
	    --datadir=%{_datadir}               \
            --infodir=%{_datadir}/info  


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
* Tue Feb 25 2010 - yuntong.jin@sun.com
- Add patch for 34463 35169 in webkit community
* Wen Feb 03 2010 - yuntong.jin@sun.com
- Drop off aclocal and automake step case aclocal regenerate GNUmakefile.in and
  automake doesn,t make any different here
* Mon Jan 25 2010 - yuntong.jin@sun.com
- Bump to 1.1.19 and repatch
* Tue Jan 21 2010 - yuntong.jin@sun.com
- Initial version, webkit build with Cstd instead of apache stl stdcxx4
