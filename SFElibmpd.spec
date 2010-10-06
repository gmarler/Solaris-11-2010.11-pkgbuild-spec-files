
#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
# works: snv104 / pkgbuild 1.3.91
# works: snv104 / pkgbuild 1.2.0
# works: snv103 / pkgbuild 1.3.0
# works: snv96  / pkgbuild 1.3.1


# IMPORTANT NOTE: compile with "gcc" - the code uses unnamed unions/structs

%include Solaris.inc

Name:                SFElibmpd
Summary:             libmpd for gmpc
Version:             0.20.0
#needed for download-URL:
%define gmpc_version 0.20.0
Source:              http://download.sarine.nl/Programs/gmpc/%{gmpc_version}/libmpd-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc


%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name


%prep
%setup -q -n libmpd-%version


%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="-O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointers"
export LDFLAGS="%_ldflags -lnsl -lsocket -lresolv"
 
export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++

CC=/usr/sfw/bin/gcc CXX=/usr/sfw/bin/g++ ./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --enable-static=no

            

gmake -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT

gmake install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*


%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*


%changelog
* Sat Oct  2 2010 - Alex Viskovatoff
- bump to 0.20.0; use gmake
* Sat Dec 20 2008 - Thomas Wagner
- adjust download URL
- add LDFLAGS for network libs
* Sun Dec 02 2007 - Thomas Wagner
- bump to 0.15.0
- removed Patch1 (#include <limits.h>)
* Sat May 26 2007  - Thomas Wagner
- bump to 0.14.0 (corresponding to gmpc version 0.15.0)
- added patch1, pls remove this if Version > 0.14.0 has #include <limits.h>
* 20070406 Thomas Wagner
- Initial spec

