#
# spec file for package SFElxpanel
#
# includes module(s): lxpanel
#
# https://sourceforge.net/tracker/index.php?func=detail&aid=$bugid&group_id=180858&atid=894869
#
%include Solaris.inc

Name:                    SFElxpanel
Summary:                 LXDE desktop panel
Version:                 0.4.1
Source:                  http://downloads.sourceforge.net/lxde/lxpanel-%{version}.tar.gz
URL:                     http://sourceforge.net/projects/lxde/

# owner:alfred date:2009-03-16 type:bug
Patch1:                  lxpanel-01-solaris.diff

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n lxpanel-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc
export CFLAGS="-DHAVE_SYS_SOCKIO_H"

autoconf
./configure --prefix=%{_prefix} --libdir=%{_libdir}
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}/lxpanel
%{_libdir}/lxpanel/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/lxpanel
%{_datadir}/lxpanel/*
%dir %attr (0755, root, bin) %{_datadir}/man
%{_datadir}/man/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Wed Jun 03 2009 - alfred.peng@sun.com
- Bump to 0.4.1. Remove the upstreamed patch crash.diff.
* Mon Mar 16 2009 - alfred.peng@sun.com
- Initial version with gcc.
