#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%define	src_ver 2.0.35
%define	src_name gd

# want this? compile with: pkgtool --with-gcc4 build <specfile>
%define use_gcc4 %{?_with_gcc4:1}%{?!_with_gcc4:0}

%include Solaris.inc
%define cc_is_gcc 1
%if %use_gcc4
%define _gpp /usr/gnu/bin/g++
%else
%define _gpp /usr/sfw/bin/g++
%endif


%ifarch amd64 sparcv9
%include arch64.inc
%use gd_64 = gd.spec
%endif

%include base.inc
%use gd = gd.spec

Name:                SFEgd
Summary:             library for the dynamic creation of images by programmers
Version:             %{src_ver}
SUNW_BaseDir:        %{_basedir}

%define src2_name default_fontpath.diff

Source2:             http://src.opensolaris.org/source/raw/sfw/usr/src/lib/gd2/Solaris/%{src2_name}

Requires: SUNWfontconfig
Requires: SUNWpng
Requires: SUNWjpg
%if %(pkginfo -q FSWxorg-clientlibs && echo 1 || echo 0)
#FOX
Requires: FSWxorg-clientlibs
%else
Requires: SUNWxwplt
%endif

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%gd_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%gd.prep -d %name-%version/%{base_arch}


%build
%ifarch amd64 sparcv9
%gd_64.build -d %name-%version/%_arch64
%endif

%gd.build -d %name-%version/%{base_arch}


%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%gd_64.install -d %name-%version/%_arch64
%endif

%gd.install -d %name-%version/%{base_arch}

%clean
%ifarch amd64 sparcv9
%gd_64.clean -d %name-%version/%_arch64
%endif

%gd.clean -d %name-%version/%{base_arch}

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/annotate
%{_bindir}/bdftogd
%{_bindir}/gd2copypal
%{_bindir}/gd2togif
%{_bindir}/gd2topng
%{_bindir}/gdcmpgif
%{_bindir}/gdlib-config
%{_bindir}/gdparttopng
%{_bindir}/gdtopng
%{_bindir}/giftogd2
%{_bindir}/pngtogd
%{_bindir}/pngtogd2
%{_bindir}/webpng
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libgd.so
%{_libdir}/libgd.so.2
%{_libdir}/libgd.so.2.0.0
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/annotate
%{_bindir}/%{_arch64}/bdftogd
%{_bindir}/%{_arch64}/gd2copypal
%{_bindir}/%{_arch64}/gd2togif
%{_bindir}/%{_arch64}/gd2topng
%{_bindir}/%{_arch64}/gdcmpgif
%{_bindir}/%{_arch64}/gdlib-config
%{_bindir}/%{_arch64}/gdparttopng
%{_bindir}/%{_arch64}/gdtopng
%{_bindir}/%{_arch64}/giftogd2
%{_bindir}/%{_arch64}/pngtogd
%{_bindir}/%{_arch64}/pngtogd2
%{_bindir}/%{_arch64}/webpng
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/libgd.so
%{_libdir}/%{_arch64}/libgd.so.2
%{_libdir}/%{_arch64}/libgd.so.2.0.0
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/gd2
%{_includedir}/gd2/*


%changelog
* Sat Jun 5 2010 - markwright@internode.on.net
- build 64 bit, with default fontpath patch, headers in include/gd2
* Wed Oct 17 2007 - laca@sun.com
- add /usr/gnu to CFLAGS/LDFLAGS
* Sat Aug 18 2007 - trisk@acm.jhu.edu
- Bump to 2.0.35
* Tue Mar 22 2007 - Thomas Wagner
- split into SFEgd SFEgd-devel
* Tue Mar 20 2007 - Thomas Wagner
- bump up version to 2.0.34
- new Url / Source
* Fri Sep 29 2006 - Eric Boutilier
- Initial spec
