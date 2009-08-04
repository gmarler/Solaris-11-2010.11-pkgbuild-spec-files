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
Version:                 0.5.1
Source:                  http://downloads.sourceforge.net/pcmanfm/pcmanfm-%{version}.tar.bz2
URL:                     http://sourceforge.net/projects/pcmanfm/

# owner:alfred date:2009-03-16 type:bug bugid:2688199
Patch1:                  pcmanfm-01-mnttab.diff

# owner:alfred date:2009-03-16 type:bug
Patch2:                  pcmanfm-02-Werror.diff

# owner:alfred date:2009-03-16 type:bug
Patch3:                  pcmanfm-03-union-struct-naming.diff

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
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, root) %{_datadir}/mime
%dir %attr (0755, root, root) %{_datadir}/mime/*
%{_datadir}/mime/*/*
%dir %attr (0755, root, other) %{_datadir}/pcmanfm
%{_datadir}/pcmanfm/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Tue Aug 04 2009 - brian.cameron@sun.com
- Bump to 0.5.1
* Mon May 25 2009 - alfred.peng@sun.com
- Update source URL and set correct GMSGFMT.
* Mon Mar 16 2009 - alfred.peng@sun.com
- Initial version
