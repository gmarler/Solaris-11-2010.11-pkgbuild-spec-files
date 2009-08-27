#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEtevent
Summary:             An event system library.
Version:             0.9.3
Source:              http://us5.samba.org/samba/ftp/samba4/samba-4.0.0alpha7.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWPython26
%prep
rm -rf samba-4.0.0alpha7
%setup -q -n samba-4.0.0alpha7/lib/tevent

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
ln -s -f libtevent.so.%{version} libtevent.so.0
ln -s libtevent.so.%{version} libtevent.so
cd -

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/*.so*
%{_libdir}/python2.6
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Thu Aug 27 2009 - brian.lu@sun.com
- add "-mt" to CFLAGS to set errno correctly in MT environment
* Wed Jun 03 2009 - brian.lu@sun.com
- Add dependency SUNWPythong26
* Wed Feb 18 2009 - jedy.wang@sun.com
- Do not use optimization option for now.
* Tue Feb 17 2009 - jedy.wang@sun.com
- Fixes file attribute problem.
* Tue Feb 11 2009 - jedy.wang@sun.com
- Initial spec
