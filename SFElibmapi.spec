#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFElibmapi
Summary:             A client-side implementation of the MAPI protocol that is used by Microsoft Exchange and Outlook. 
Version:             0.8
Source:              http://downloads.sourceforge.net/openchange/libmapi-%{version}-ROMULUS.tar.gz
Patch1:              libmapi-01-solaris.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc


%prep
%setup -q -n libmapi-%{version}-ROMULUS
%patch1 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./autogen.sh
./configure --prefix=%{_prefix}  \
            --with-moduelsdir=%{_libdir}/libmapi

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT/%{_libdir}
ln -s -f libmapi.so.%{version} libmapi.so.0
ln -s libmapiadmin.so.%{version} libmapiadmin.so.0
ln -s libmapiproxy.so.%{version} libmapiproxy.so.0
ln -s libocpf.so.%{version} libocpf.so.0
cd -

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/setup/*
/usr/modules/*

%changelog
* Thu Feb 12 2009 - jedy.wang@sun.com
- Initial spec
