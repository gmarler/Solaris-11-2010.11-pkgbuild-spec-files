#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEtdb
Summary:             A trivial database used by samba.
Version:             1.2.0
Source:              http://us5.samba.org/samba/ftp/samba4/samba-4.0.0alpha9.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires:SUNWPython26

%prep
rm -rf samba-4.0.0alpha9
%setup -q -n samba-4.0.0alpha9/lib/tdb

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

#export CFLAGS="%optflags"
export CFLAGS="-g -mt"
export LDFLAGS="%_ldflags"

./autogen.sh
./configure --prefix=%{_prefix}  \
            --enable-static=no

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT/%{_libdir}
ln -s -f libtdb.so.%{version} libtdb.so.1
ln -s libtdb.so.%{version} libtdb.so
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
%{_libdir}/python2.6
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Wed Dec 02 2009 - brian.lu@sun.com
- Bump to Samba4 alpha9
* Wed Jun 03 2009 - brian.lu@sun.com
- Add dependency SUNWPython26
* Wed Feb 18 2009 - jedy.wang@sun.com
- Do not use optimization option for now.
* Tue Feb 17 2009 - jedy.wang@sun.com
- Fixes file attribute problem.
* Tue Feb 10 2009 - jedy.wang@sun.com
- Initial spec
