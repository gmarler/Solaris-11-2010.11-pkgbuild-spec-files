#
# spec file for package SFElxsession-lite
#
# includes module(s): lxsession-lite
#
%include Solaris.inc

Name:                    SFElxsession-lite
Summary:                 LXDE Lite session manager
Version:                 0.3.6
Source:                  http://downloads.sourceforge.net/lxde/lxsession-lite-%{version}.tar.gz
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
%setup -q -n lxsession-lite-%version

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
