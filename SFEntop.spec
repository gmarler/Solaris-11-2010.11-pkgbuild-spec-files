#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

# TODO fix sctp support

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%define SFErrdtool	%(/usr/bin/pkginfo -q SFErrdtool && echo 1 || echo 0)

# define for internal lua lib download in ntop configure script
%define lua_version 5.1.4

Name:		SFEntop
Summary:	A network traffic usage monitor
Version:	3.3.10
Source:		%{sf_download}/ntop/ntop-%{version}.tar.gz
Source1:	http://www.lua.org/ftp/lua-%{lua_version}.tar.gz
Source2:	http://www.maxmind.com/download/geoip/api/c/GeoIP.tar.gz
Source3:	http://www.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
Source4:	http://www.maxmind.com/download/geoip/database/asnum/GeoIPASNum.dat.gz
Patch1:		ntop-01-lua-hidden.diff
Patch2:		ntop-02-configure.diff
Patch3:		ntop-03-mimpure.diff
URL:		http://www.ntop.org/
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWlibpcap
BuildRequires: SUNWgnu-dbm
BuildRequires: SUNWgd2
Requires: SUNWlibpcap
Requires: SUNWgnu-dbm
Requires: SUNWgd2
BuildRequires: SFElibevent
Requires: SFElibevent
BuildRequires: SUNWopenssl-include
Requires: SUNWopenssl-libraries
Requires: %name-root
BuildRequires: SUNWgzip
BuildRequires: SUNWgawk
BuildRequires: SUNWgsed
BuildRequires: SUNWscp
BuildRequires: SUNWperl584usr
Requires: SUNWperl584usr

%if %SFErrdtool
BuildRequires: SFErrdtool
Requires: SFErrdtool
%else
BuildRequires: SUNWrrdtool
Requires: SUNWrrdtool
%endif

%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/
%include default-depend.inc

%prep
%setup -q -n ntop-%version
cp %{PATCH1} .
%patch2 -p1
%patch3 -p1
cp %{SOURCE1} .
cp %{SOURCE2} .
cp %{SOURCE3} . && gunzip GeoLiteCity.dat.gz
cp %{SOURCE4} . && gunzip GeoIPASNum.dat.gz

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

# This source is gcc-centric, therefore...
export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
#export CFLAGS="-O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointer"

export LDFLAGS="%{_ldflags} -lsocket -lnsl"

./autogen.sh --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --localstatedir=%{_localstatedir} \
            --sysconfdir=%{_sysconfdir} \
            --disable-static \
            --with-ssl \
            --enable-jumbo-frames

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

cd GeoIP-1.4.6; make install DESTDIR=$RPM_BUILD_ROOT; cd ..
make install DESTDIR=$RPM_BUILD_ROOT

rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*
%dir %attr (0755, root, sys) %{_localstatedir}
%{_localstatedir}/*

%changelog
* Fri May 28 2010 - Milan Jurik
- update to 3.3.10
* Sat Mar 31 2007 - Thomas Wagner
- change Build-Requires to be SFEgd-devel
* Mon Mar 19 2007 - dougs@truemail.co.th
- Fixed -fno-omit-frame-pointer flag
* Sun Nov 05 2006 - Eric Boutilier
- Force gcc; adjust dependencies 
* Fri Sep 29 2006 - Eric Boutilier
- Initial spec
