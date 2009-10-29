#
# spec file for package SFEgnomad2
#
# includes module(s): gnomad2
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%use gnomad2 = gnomad2.spec

Name:		SFEgnomad2
Summary:	%{gnomad2.summary}
Version:	%{gnomad2.version}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
Requires: SFEglibmm-gpp
Requires: SFEgtkmm-gpp
Requires: SFElibnjp
Requires: SFElibmtp
BuildRequires: SFEglibmm-gpp-devel
BuildRequires: SFEgtkmm-gpp-devel
BuildRequires: SFElibnjp-devel
BuildRequires: SFElibmtp-devel
Requires: SFEsigcpp-gpp
BuildRequires: SFEsigcpp-gpp-devel
BuildRequires: SUNWsigcpp-devel

%prep
rm -rf %name-%version
mkdir %name-%version

%gnomad2.prep -d %name-%version

%build
%gnomad2.build -d %name-%version/

%install
rm -rf $RPM_BUILD_ROOT
%gnomad2.install -d %name-%version/

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
%if %build_l10n
%attr (0755, root, other) %{_datadir}/locale
%endif
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/application-registry
%{_datadir}/application-registry/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*


%changelog
* Thu Oct 29 2009 - jchoi42@pha.jhu.edu
- Initial spec
