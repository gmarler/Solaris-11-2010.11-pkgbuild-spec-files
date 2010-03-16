#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEevolution-mapi
Summary:             evolution-mapi provides connectivity to Microsoft Exchange 2007 servers using Openchange's libmapi in Evolution.
Version:             0.28.2
Source:              http://ftp.gnome.org/pub/GNOME/sources/evolution-mapi/0.28/evolution-mapi-%{version}.tar.gz
Patch1:              evolution-mapi-01-solaris.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFElibmapi
Requires: SFElibmapi

BuildRequires: SUNWevolution
Requires: SUNWevolution

%prep
rm -rf %name-%version
%setup -q -c -n %name-%version 
cd evolution-mapi-%{version}
%patch1 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

cd evolution-mapi-%{version}
export CFLAGS="-g -features=extensions"
export LDFLAGS="%_ldflags"

autoheader
automake -a -f -c --gnu
autoconf

./configure --prefix=%{_prefix}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
cd evolution-mapi-%{version}

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
%attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/evolution
%{_libdir}/evolution-data-server-1.2
%{_libdir}/*.so*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/evolution-data-server-2.28
%attr (0755, root, other) %{_datadir}/locale

%changelog
* Tue Mar 16 2010 - brian.lu@sun.com
- Build evolution-mapi under %name-%version directory
  Add dependencies: SFEtdb, SFEtalloc, SFEtevent and SFEsamba4
* Thu Jan 14 2010 - brian.lu@sun.com
- Bump to 0.28.2
* Wed Feb 18 2009 - jedy.wang@sun.com
- Do not use optimization option for now.
* Tue Feb 17 2009 - jedy.wang@sun.com
- Fixes file attribute problem.
* Fri Feb 13 2009 - jedy.wang@sun.com
- Initial spec
