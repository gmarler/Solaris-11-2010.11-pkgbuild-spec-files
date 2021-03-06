#
# spec file for package SFEpcmanfm
#
# includes module(s): pcmanfm
#
# https://sourceforge.net/tracker/index.php?func=detail&aid=$bugid&group_id=156956&atid=801864
#
%include Solaris.inc

Name:                    SFEpcmanfm
Summary:                 LXDE lightweight file manager
Version:                 0.9.7
Source:                  http://downloads.sourceforge.net/pcmanfm/pcmanfm-%{version}.tar.gz
Patch1:                  pcmanfm-01-Wall.diff
Patch2:                  pcmanfm-02-inline.diff
Patch3:                  pcmanfm-03-state.diff
URL:                     http://sourceforge.net/projects/pcmanfm/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SFElibfm
BuildRequires: SFElibfm-devel

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n pcmanfm-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export LDFLAGS="-lsocket"

export GMSGFMT=/usr/bin/gmsgfmt
libtoolize --force
aclocal $ACLOCAL_FLAGS
autoheader
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
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pcmanfm
%{_datadir}/pcmanfm/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Thu Sep 16 2010 - brian.cameron@oracle.com
- Add patch pcmanfm-03-state.diff so that it builds with older compilers.
* Tue Aug 04 2009 - brian.cameron@sun.com
- Bump to 0.5.1
* Mon May 25 2009 - alfred.peng@sun.com
- Update source URL and set correct GMSGFMT.
* Mon Mar 16 2009 - alfred.peng@sun.com
- Initial version
