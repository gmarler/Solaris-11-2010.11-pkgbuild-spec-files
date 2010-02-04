%include Solaris.inc

%include base.inc
%use gitg = gitg.spec

Name:           SFEgitg
Summary:        Image metadata library
Version:        %{default_pkg_version}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%package root
Summary:       %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%{base_arch}
%gitg.prep -d %name-%version/%{base_arch}


%build
export PKG_CONFIG_PATH=%{_libdir}/pkgconfig
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
%gitg.build -d %name-%version/%{base_arch}


%install
rm -rf $RPM_BUILD_ROOT

%gitg.install -d %name-%version/%{base_arch}
%
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
%{_bindir}/gitg
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_datadir}/gitg/
%dir %attr (0755, root, other) %{_datadir}/pixmaps                                                                                                                                                             
%{_datadir}/pixmaps/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/gitg.schemas

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif


%changelog
* Thu Feb 04 2010 - jedy.wang@sun.com
- Initial spec
