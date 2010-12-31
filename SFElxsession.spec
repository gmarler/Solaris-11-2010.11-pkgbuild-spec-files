#
# spec file for package SFElxsession
#
# includes module(s): lxsession
#
# https://sourceforge.net/tracker/index.php?func=detail&aid=$bugid&group_id=180858&atid=894869
#
%include Solaris.inc

Name:                    SFElxsession
Summary:                 LXDE session manager
Version:                 0.4.5
Source:                  http://nchc.dl.sourceforge.net/sourceforge/lxde/lxsession-%{version}.tar.gz
Patch1:                  lxsession-01-Werror.diff
Patch2:                  lxsession-02-fixcrash.diff
Patch3:                  lxsession-03-reboot.diff
URL:                     http://sourceforge.net/projects/lxde/

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
%setup -q -n lxsession-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export LDFLAGS="-lsocket"

libtoolize --force
aclocal $ACLOCAL_FLAGS
automake -a -c -f
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
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/lxsession
%{_datadir}/lxsession/*
%dir %attr (0755, root, bin) %{_datadir}/man
%{_datadir}/man/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Thu Dec 30 2010 - brian.cameron@oracle.com
- Bump to 0.4.5.
* Fri Sep 17 2010 - brian.cameron@oracle.com
- Add patch lxsession-03-reboot.diff so that HAL is not checked to see if
  reboot/shutdown is available.
* Tue Apr 27 2010 - brian.cameron@sun.com
- Bump to 0.4.4.
* Mon Feb 15 2010 - brian.cameron@sun.com
- Bump to 0.4.1.
* Wed May 27 2009 - alfred.peng@sun.com
- Bump to 0.3.8.
  Remove upstreamed patch docbook2man.diff for bug 2688183.
* Mon Mar 16 2009 - alfred.peng@sun.com
- Initial version.
