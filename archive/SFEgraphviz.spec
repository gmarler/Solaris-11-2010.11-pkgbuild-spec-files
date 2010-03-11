#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define SFEfreetype %(/usr/bin/pkginfo -q SFEfreetype && echo 1 || echo 0)
%define tcl_8_3 %(pkgchk -l SUNWTcl 2>/dev/null | grep /usr/sfw/bin/tclsh8.3 >/dev/null && echo 1 || echo 0)

Name:                SFEgraphviz
Summary:             Graph drawing tools and libraries
Version:             2.16.1
Source:              http://www.graphviz.org/pub/graphviz/ARCHIVE/graphviz-%{version}.tar.gz
URL:                 http://www.graphviz.org
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWlibtool
Requires: SUNWgd2
Requires: SUNWlexpt
Requires: SUNWfontconfig
Requires: SUNWlexpt
%if %SFEfreetype
Requires: SFEfreetype
%else
Requires: SUNWfreetype2
%endif
Requires: SUNWgnome-base-libs
Requires: SUNWjpg
Requires: SUNWlibC
Requires: SUNWpng
%if %SFEfreetype
BuildRequires: SFEfreetype-devel
%else
BuildRequires: SUNWfreetype2
%endif
BuildRequires: SUNWgnome-base-libs-devel
# obsolete in b133
#BuildRequires: SUNWsfwhea
BuildRequires: SUNWlibtool
BuildRequires: SUNWPython-devel
BuildRequires: SUNWTcl
BuildRequires: SUNWperl584core
BuildRequires: SUNWruby18u
BuildRequires: SUNWswig

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n graphviz-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CPPFLAGS="-I/usr/sfw/include -D_SYS_MODE_H"
export CFLAGS="%optflags -I/usr/X11/include -I/usr/include/gd2"
export LDFLAGS="%_ldflags -L/usr/X11/lib -R/usr/X11/lib -lgd"
%if %tcl_8_3
TCL_OPTS="--with-tclsh=/usr/sfw/bin/tclsh8.3 \
          --with-wish=/usr/sfw/bin/wish8.3"
%else
TCL_OPTS=
%endif

libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf
./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --enable-static=no \
            --enable-ltdl \
            --disable-rpath \
            --disable-sharp \
            --disable-guile \
            --disable-io \
            --disable-java \
            --disable-lua \
            --disable-ocaml \
            --disable-php \
            --disable-swig \
            --disable-r \
            --disable-python23 \
            --disable-python24 \
            --disable-python25 \
            $TCL_OPTS

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

rm -rf ${RPM_BUILD_ROOT}%{_mandir}/mann

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_bindir}/dot -c

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/graphviz
%{_libdir}/graphviz/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*.3
%dir %attr (0755, root, bin) %{_mandir}/man7
%{_mandir}/man7/*.7

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/graphviz
%{_datadir}/graphviz/*

%changelog
* Fri Nov 14 2008 - Gilles Dauphin
- SUNWfsweha is obsolete in b133
* Fri Nov 14 2008 - Gilles Dauphin
- build required  SUNWswig in B101 now
* Thu Jan 24 2008 - nonsea@users.sourceforge.net
- Replace SFEruby to SUNWruby18u
* Wed Jan 17 2008 - moinak.ghosh@sun.com
- Do not disable perl.
- Prevent sys/mode.h from being pulled in via perl.h by defining _SYS_MODE_H. This
- allows the perl plugin to be built.
* Wed Jan 16 2008 - moinak.ghosh@sun.com
- Bump version to 2.16.1
- Remove SUNWfontconfig-devel from BuildRequires. SUNWfontconfig package includes
- devel components.
- Changed SFElibtool dep to SUNWlibtool.
- Remove unneeded patches.
* Thu Oct 25 2007 - nonsea@users.sourceforge.net
- Add configure option --disale-perl 
- Add patch gd-ldflags.diff
- Add /usr/include/gd2 to CFLAGS
* Wed Oct 17 2007 - laca@sun.com
- add /usr/X11 to search paths for FOX
- allow building with either SUNWlexpt or SFEexpat
* Mon Sep 24 2007 - trisk@acm.jhu.edu
- Allow building with Tcl 8.4 (newer SUNWTcl)
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Add patch arith-h to export arith.h to let anjuta build pass.
  This patch is already in cvs head, should be removed in next release.
* Fri Aug 17 2007 - trisk@acm.jhu.edu
- Bump to 2.14
- Update dependencies, disable optional plugins
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Add patch tclsh.diff and ruby-lib.diff to build pass.
- Add Requires/BuildRequries after check-deps.pl run.
* Wed Mar 07 2007 - daymobrew@users.sourceforge.net
- Bump to 2.12. Delete more *.la files in %install. Add URL field.
* Tue Nov 07 2006 - Eric Boutilier
- Initial spec
