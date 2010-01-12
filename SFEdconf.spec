#
# spec file for package SFEdconf
#
# includes module(s): dconf
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use dconf64 = dconf.spec
%endif

%include base.inc
%use dconf = dconf.spec

Name:                    SFEdconf
Summary:                 A low-level configuration system
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
#SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:           SUNWglib2
Requires:                SUNWglib2
Requires:                %{name}-root


%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc


%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%{_arch64}
%dconf64.prep -d %name-%version/%{_arch64}
%endif

mkdir %name-%version/%{base_arch}
%dconf.prep -d %name-%version/%{base_arch}


%build
%ifarch amd64 sparcv9
export PKG_CONFIG_PATH=%{_libdir}/%{_arch64}/pkgconfig
export CFLAGS="%optflags64"
export LDFLAGS="%_ldflags"
%dconf64.build -d %name-%version/%{_arch64}
%endif

export PKG_CONFIG_PATH=%{_libdir}/pkgconfig
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
%dconf.build -d %name-%version/%{base_arch}


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%dconf64.install -d %name-%version/%{_arch64}
%endif

%dconf.install -d %name-%version/%{base_arch}

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/dconf-watch
%{_bindir}/dconf
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/dconf-service
%{_libdir}/dconf-writer
%{_libdir}/gio
%{_libdir}/libdconf.so*
%{_libdir}/pkgconfig/dconf.pc
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/dconf-watch
%{_bindir}/%{_arch64}/dconf
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/dconf-service
%{_libdir}/%{_arch64}/dconf-writer
%{_libdir}/%{_arch64}/gio
%{_libdir}/%{_arch64}/libdconf.so*
%{_libdir}/%{_arch64}/pkgconfig/dconf.pc
%endif
%{_datadir}/dbus-1/services/ca.desrt.dconf.writer.user.service
%{_datadir}/dbus-1/services/ca.desrt.dconf.Service.service
%{_datadir}/dbus-1/system-services/ca.desrt.dconf.writer.system.service
%{_datadir}/dbus-1/system-services/ca.desrt.dconf.writer.default.service
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc/html/dconf/*
%{_includedir}/dconf/*.h


%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/dconf/system.db
%{_sysconfdir}/dconf/default.db
%{_sysconfdir}/dconf/dconf.conf


%changelog
* Tue Jan 12 2010 - jedy.wang@sun.com
- Init spec.

