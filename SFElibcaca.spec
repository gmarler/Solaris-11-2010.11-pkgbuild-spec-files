#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFElibcaca
Summary:             A colour ASCII art library.
Version:             0.99
%define tarball_version 0.99.beta11
Source:              http://libcaca.zoy.org/files/libcaca-%{tarball_version}.tar.gz
URL:                 http://libcaca.zoy.org/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWslang
BuildRequires: SFEimlib2
Requires: SUNWslang
Requires: SFEimlib2
Requires: SUNWgccruntime

# Guarantee X/freetype environment, concisely (hopefully)
Requires: SUNWxwplt 
# The above brings in many things, including SUNWxwice and SUNWzlib
Requires: SUNWxwxft 
# The above also pulls in SUNWfreetype2

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n libcaca-%tarball_version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

# Use gcc:
export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++
export CFLAGS="-O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointer"
export LDFLAGS="%_ldflags -lsocket -lnsl"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
	    --disable-ncurses \
            --disable-doc \
            --enable-static=no

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm ${RPM_BUILD_ROOT}%{_libdir}/libcaca.la
rm ${RPM_BUILD_ROOT}%{_libdir}/libcucul.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, other) %{_datadir}/libcaca
%{_datadir}/libcaca/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Fri Jun 20 2008 - river@wikimedia.org
- change SFEslang to SUNWslang
* Thu Mar 22 2007 - daymobrew@users.sourceforge.net
- Update Source location and add URL.
* Mon Mar 19 2007 - dougs@truemail.co.th
- Fixed -fno-omit-frame-pointer flag
* Wed Dec 20 2006 - Eric Boutilier
- Initial spec
