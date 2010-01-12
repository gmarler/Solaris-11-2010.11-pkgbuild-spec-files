#
# spec file for package SFEeggdbus
#
# includes module(s): eggdbus
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use eggdbus64 = eggdbus.spec
%endif

%include base.inc
%use eggdbus = eggdbus.spec

Name:                    SFEeggdbus
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
%eggdbus64.prep -d %name-%version/%{_arch64}
%endif

mkdir %name-%version/%{base_arch}
%eggdbus.prep -d %name-%version/%{base_arch}


%build
%ifarch amd64 sparcv9
export PKG_CONFIG_PATH=%{_libdir}/%{_arch64}/pkgconfig
export CFLAGS="%optflags64"
export LDFLAGS="%_ldflags"
%eggdbus64.build -d %name-%version/%{_arch64}
%endif

export PKG_CONFIG_PATH=%{_libdir}/pkgconfig
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
%eggdbus.build -d %name-%version/%{base_arch}


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%eggdbus64.install -d %name-%version/%{_arch64}
%endif

%eggdbus.install -d %name-%version/%{base_arch}

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

rm -rf $RPM_BUILD_ROOT%{_datadir}/gtk-doc/html/tests


%clean
rm -rf $RPM_BUILD_ROOT


%post


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/eggdbus-binding-tool
%{_bindir}/eggdbus-glib-genmarshal
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/libeggdbus-1.so*
%{_libdir}/pkgconfig/eggdbus-1.pc
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/eggdbus-binding-tool
%{_bindir}/%{_arch64}/eggdbus-glib-genmarshal
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/libeggdbus-1.so*
%{_libdir}/%{_arch64}/pkgconfig/eggdbus-1.pc
%endif
%dir %attr(0755, root, bin) %{_mandir}
%{_mandir}/*/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc/html/eggdbus/*
%{_includedir}/eggdbus-1/*


%changelog
* Tue Jan 12 2010 - jedy.wang@sun.com
- Init spec.

