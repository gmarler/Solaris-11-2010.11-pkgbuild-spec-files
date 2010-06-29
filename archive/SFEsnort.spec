#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEsnort
Summary:             Network intrusion prevention and detection system
Version:             2.8.0.1
Source:              http://snort.org/dl/current/snort-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

Requires: SUNWpcre
BuildRequires: SUNWpcre-devel
Requires: SFElibpcap
BuildRequires: SFElibpcap-devel
Requires: SUNWgccruntime
BuildRequires: SUNWpostgr-devel
Requires: SUNWpostgr-server
# The above line also guarantees these: SUNWpostgr, 
# SUNWpostgr-libs, SUNWpostgr-server-data

%prep
%setup -q -n snort-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++
export CFLAGS="-O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointer"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}  \
            --enable-static=no \
            --with-postgresql=yes \
            --with-pgsql-includes=/usr/include/pgsql \
            --mandir=%{_mandir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

mv ${RPM_BUILD_ROOT}%{_prefix}/src ${RPM_BUILD_ROOT}%{_datadir}
rm ${RPM_BUILD_ROOT}%{_libdir}/snort_dynamicengine/*.la
rm ${RPM_BUILD_ROOT}%{_libdir}/snort_dynamicpreprocessor/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}/snort_dynamicengine
%dir %attr (0755, root, bin) %{_libdir}/snort_dynamicpreprocessor
%{_libdir}/snort_dynamic*/libsf*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, sys) %{_datadir}/src
%dir %attr (0755, root, bin) %{_datadir}/src/snort_dynamicsrc
%{_datadir}/src/snort_dynamicsrc/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/snort.8

%changelog
* Tue Feb 12 2008 <pradhap (at) gmail.com>
- Bumped up the version to 2.8.0.1
* Mon Mar 19 2007 - dougs@truemail.co.th
- Fixed -fno-omit-frame-pointer flag
* Sun Mar 04 2007 - Eric Boutilier
- Bump to 2.6.1.3 
- Several misc improvements
* Fri Sep 01 2006 - Eric Boutilier
- Initial spec
