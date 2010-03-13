#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define source_name samba-4.0.0alpha11

Name:                SFEtdb
Summary:             A trivial database used by samba.
Version:             1.2.0
Source:              http://us5.samba.org/samba/ftp/samba4/%{source_name}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires:SUNWPython26

%prep
rm -rf %name-%version
mkdir %name-%version
%setup -q -c -n %name-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="-g -mt %optflags"
export LDFLAGS="-z ignore %_ldflags"

cd %{source_name}/lib/tdb
./autogen.sh
./configure --prefix=%{_prefix}  \
            --enable-static=no

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
cd %{source_name}/lib/tdb

make install DESTDIR=$RPM_BUILD_ROOT

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
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*

%changelog
* Sat Mar 13 2010 - brian.lu@sunc.om
- Build tdb under SFEtdb-1.2.0 directory
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
