#
# spec file for package SUNWpcmanx
#
# includes module(s): pcmanx-gtk2
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#

%include Solaris.inc

%use pcmanx = pcmanx-gtk2.spec

Name:               SUNWpcmanx
Summary:            pcmanx - A user-friendly telnet client designed for BBS browsing.
Version:            %{pcmanx.version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%if %build_l10n
%package l10n
Summary:            %{summary} - l10n files
SUNW_BaseDir:       %{_basedir}
%include default-depend.inc
Requires:           %{name}
%endif

%prep
rm -rf %name-%version
mkdir -p %name-%version
%pcmanx.prep -d %name-%version


%build
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
%pcmanx.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%pcmanx.install -d %name-%version

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
%{_bindir}/pcmanx
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (-, root, other) %{_datadir}/applications
%{_datadir}/applications/pcmanx.desktop
%dir %attr (-, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%{_datadir}/pcmanx

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Fri Apr 10 2009 - halton.huo@sun.com
- Initial spec
