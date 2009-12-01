#
# spec file for package SFEseahorse
#
# includes module(s): seahorse
#
# owner: Jerry Yu
#

%include Solaris.inc
%use seahorse = seahorse.spec

Name:          SFEseahorse
Summary:       %{seahorse.summary}
Version:       %{seahorse.version}
SUNW_BaseDir:  %{_basedir}
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEgnupg
Requires: SFEgpgme
Requires: SUNWdbus

%package devel
Summary: 	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%{name}

%if %build_l10n
%package l10n
Summary:        %{summary} - l10n files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires:       %{name}
%endif

%prep
rm -rf %name-%version
mkdir -p %name-%version
%seahorse.prep -d %name-%version

%build
export CFLAGS="%optflags"
export MSGFMT="/usr/bin/msgfmt"
export LDFLAGS="%_ldflags"
%seahorse.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%seahorse.install -d %{name}-%{version} 
rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -rf $RPM_BUILD_ROOT%{_libdir}/gedit-2/plugins/lib*a
rm -rf $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-1.0/lib*a

%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (0755, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*so*
%{_libdir}/bonobo
%{_libdir}/gedit-2
%{_libdir}/nautilus
%{_libdir}/seahorse
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/applications
%{_datadir}/dbus-1
%{_datadir}/gnome-2.0
%{_datadir}/gnome
%{_datadir}/icons
%{_datadir}/omf
%{_datadir}/pixmaps
%{_datadir}/seahorse
%{_datadir}/mime
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*
%dir %attr (0755, root, bin) /usr/etc
/usr/etc/* 

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%if %build_l10n
%files l10n
%defattr (0755, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (0755, root, other) %{_datadir}/locale
%endif

%changelog
* Tue Dec 18 2007- jijun.yu@sun.com
- initial version created
