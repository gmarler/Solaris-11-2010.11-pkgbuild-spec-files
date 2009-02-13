#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEevolution-mapi
Summary:             evolution-mapi provides connectivity to Microsoft Exchange 2007 servers using Openchange's libmapi in Evolution.
Version:             0.25.91
Source:              http://ftp.gnome.org/pub/GNOME/sources/evolution-mapi-%{version}.tar.gz
Patch1:              evolution-mapi-01-solaris.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc


%prep
%setup -q -n evolution-mapi-%{version}
%patch1 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -features=extensions"
export LDFLAGS="%_ldflags"

autoheader
automake -a -f -c --gnu
autoconf

./configure --prefix=%{_prefix}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT/%{_libdir}
#ln -s -f libmapi.so.%{version} libmapi.so.0
#ln -s libmapiadmin.so.%{version} libmapiadmin.so.0
#ln -s libmapiproxy.so.%{version} libmapiproxy.so.0
#ln -s libocpf.so.%{version} libocpf.so.0
cd -

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%changelog
* Fri Feb 13 2009 - jedy.wang@sun.com
- Initial spec
