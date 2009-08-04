#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFElibmapi
Summary:             A client-side implementation of the MAPI protocol that is used by Microsoft Exchange and Outlook. 
Version:             0.8.2
Source:              http://downloads.sourceforge.net/openchange/libmapi-%{version}-ROMULUS.tar.gz
Patch1:              libmapi-03-solaris.diff
Patch2:              libmapi-04-no-return-value.diff
Patch3:              libmapi-01-solaris.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc


%prep
%setup -q -n libmapi-%{version}-ROMULUS
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

#export CFLAGS="%optflags"
export CFLAGS="-g -D__FUNCTION__=__func__"
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
%attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/*.so*
%{_libdir}/mapistore_backends/*
%{_libdir}/python2.4
%{_libdir}/nagios
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/setup/*
/usr/modules/*

%changelog
* Tue Aug 04 2009 - brian.lu@sun.com
- Bump to 0.8.2 
  Update the patch libmapi-01-solaris.diff
* Wed Feb 18 2009 - jedy.wang@sun.com
- Do not use optimization option for now.
* Tue Feb 17 2009 - jedy.wang@sun.com
- Fix file attribute problem.
* Thu Feb 12 2009 - jedy.wang@sun.com
- Initial spec
