#
# spec file for package lua scripting language
#
%include Solaris.inc
%define source_name lua

Name:                    SFElua
Summary:                 Lua - fast, simple scripting language
Version:                 5.1.4
Source:                  http://www.lua.org/ftp/%{source_name}-%{version}.tar.gz
URL:                     http://www.lua.org/
Patch1:                  lua-01-fixcc.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{source_name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n %{source_name}-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

make solaris

%install
rm -rf $RPM_BUILD_ROOT
make INSTALL_TOP=$RPM_BUILD_ROOT/usr install
mv ${RPM_BUILD_ROOT}/usr/man ${RPM_BUILD_ROOT}/usr/share/man

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (-, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/lua
%{_datadir}/lua/*

%changelog
* Thu Mar 05 2009 - sobotkap@gmail.com
- Fix patch and bump to version 5.1.4
* Tue Sep 11 2007 - Petr Sobotka sobotkap@centum.cz
- Initial version

