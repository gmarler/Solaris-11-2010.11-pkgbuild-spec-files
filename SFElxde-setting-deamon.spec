#
# spec file for package SFElxde-settings-daemon
#
# includes module(s): lxde-settings-daemon
#
%include Solaris.inc

Name:                    SFElxde-settings-daemon
Summary:                 LXDE settings daemon
Version:                 0.4.1
Source:                  http://nchc.dl.sourceforge.net/sourceforge/lxde/lxde-settings-daemon-%{version}.tar.bz2
URL:                     http://sourceforge.net/projects/lxde/

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n lxde-settings-daemon-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

autoconf
./configure --prefix=%{_prefix} --sysconfdir=%{_sysconfdir} --mandir=%{_mandir}
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/man
%{_datadir}/man/*

%files root
%defattr (0755, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/lxde/*

%changelog
* Wed May 27 2009 - alfred.peng@sun.com
- Initial version
