#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include usr-gnu.inc

Name:                SFElibiconv
Summary:             GNU iconv -- Code set conversion
Version:             1.13
Source:              http://ftp.gnu.org/pub/gnu/libiconv/libiconv-%{version}.tar.gz
Patch1:              libiconv-01-fix-runpath.diff
Patch2:              libiconv-02-646.diff
Patch3:              libiconv-03-intmax.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n libiconv-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"

./configure \
        --prefix=%{_prefix}	\
        --libdir=%{_libdir}	\
        --datadir=%{_datadir}	\
        --mandir=%{_mandir}	\
        --enable-static=no

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm ${RPM_BUILD_ROOT}%{_libdir}/lib*.la
rm $RPM_BUILD_ROOT%{_libdir}/charset.alias

%if %build_l10n
%else
# REMOVE l10n FILES
rm -fr $RPM_BUILD_ROOT%{_datadir}/locale
#rm -r $RPM_BUILD_ROOT%{_datadir}/gnome/help/gnome-commander/[a-z]*
#rm -r $RPM_BUILD_ROOT%{_datadir}/omf/gnome-commander/*-[a-z]*.omf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/iconv
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/iconv.1
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/iconv*.3

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/doc
%{_datadir}/doc/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Fri Oct 09 2009 - Milan Jurik
- update to 1.13
- fix /usr/gnu/share/doc group
* Sun Aug 17 2008 - nonsea@users.sourceforge.net
- Bump to 1.12
- Add patch intmax.diff to fix build issue.
* Sun Jun 29 2008 - river@wikimedia.org
- use rm -fr instead of rm -r, since this directory doesn't seem to exist always
* Sun Nov 18 2007 - daymobrew@users.sourceforge.net
- Add l10n package.
* Sun Apr 21 2007 - Doug Scott
- Added -L/usr/gnu/lib -R/usr/gnu/lib
* Mon Mar 12 2007 - Eric Boutilier
- Initial spec
