#
# spec file for package SFEopenbox
#
# includes module(s): openbox
#
# bugdb: http://bugzilla.icculus.org
#
%include Solaris.inc

Name:                    SFEopenbox
Summary:                 a free window manager for the X Window System
Version:                 3.4.7.2
Source:                  http://icculus.org/openbox/releases/openbox-%{version}.tar.gz
URL:                     http://icculus.org/openbox/index.php/Main_Page

# Refer to Sun Studio compiler bugs 4614572 and 6525110
# owner:alfred date:2009-06-02 type:bug
# reported as bug 3869.
Patch1:                  openbox-01-union.diff
# reported as bug 4253.
Patch2:                  openbox-02-session.diff

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

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n openbox-%version

%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export LDFLAGS="-lsocket"

autoconf
./configure --prefix=%{_prefix} --libdir=%{_libdir} --sysconfdir=%{_sysconfdir}
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT/%{_libdir}/*a

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
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*so*
%dir %attr (0755, root, bin) %{_libdir}/openbox
%{_libdir}/openbox/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/*
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_datadir}/xsessions
%{_datadir}/xsessions/*
%dir %attr (0755, root, bin) %{_datadir}/themes
%{_datadir}/themes/*
%dir %attr (0755, root, bin) %{_datadir}/man
%{_datadir}/man/*

%files root
%defattr (0755, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/xdg/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Tue Aug 04 2009 - brian.cameron@sun.com
- Add patch openbox-02-session.diff so that the script works
  with Nevada bourne-shell.
* Tue Jun 02 2009 - alfred.peng@sun.com
- Add patch union.diff for anonymous union usage.
* Sun Mar 16 2009 - alfred.peng@sun.com
- Initial version
