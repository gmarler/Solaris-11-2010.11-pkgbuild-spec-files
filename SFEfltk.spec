#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEfltk
Summary:             A C++ user interface toolkit
Version:             1.1.7
Source:              http://ftp.easysw.com/pub/fltk/%{version}/fltk-%{version}-source.tar.bz2
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%if %(pkginfo -q FSWxwrtl && echo 1 || echo 0)
# using FOX
Requires: FSWxwrtl
%else
Requires: SUNWxwplt
BuildRequires: SUNWxwplt
%endif

%package devel
Summary:		 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:		 %name

%prep
%setup -q -n fltk-%{version}

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=/usr/gcc/4.3/bin/gcc
export CXX=/usr/gcc/4.3/bin/g++
#export CFLAGS="%optflags"
#export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
	    --enable-shared

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm ${RPM_BUILD_ROOT}%{_libdir}/libfltk.a
rm ${RPM_BUILD_ROOT}%{_libdir}/libfltk_forms.a
rm ${RPM_BUILD_ROOT}%{_libdir}/libfltk_images.a

rm -rf ${RPM_BUILD_ROOT}%{_datadir}/man/cat*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/fluid
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/fltk-config
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Sat Oct 13 2007 - laca@sun.com
- add FOX build support
* Wed Oct 11 2006 - laca@sun.com
- create devel subpkg
- fix doc dir attributes
* Wed Sep 27 2006 - Eric Boutilier
- Initial spec
