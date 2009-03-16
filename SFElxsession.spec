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
Version:                 0.3.2
Source:                  http://downloads.sourceforge.net/lxde/lxsession-%{version}.tar.bz2
URL:                     http://sourceforge.net/projects/lxde/

# owner:alfred date:2009-03-16 type:bug bugid:2688183
Patch1:                  lxsession-01-docbook2man.diff

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEdocbook-utils
BuildRequires: SFEperl-SGMLpm

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

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export LDFLAGS="-lsocket"

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
* Mon Mar 16 2009 - alfred.peng@sun.com
- Initial version
