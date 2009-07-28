#
# spec file for package SFEpolicykit
#
# includes module(s): PolicyKit PolicyKit-gnome
#
# Owner: jim
#
%include Solaris.inc
%use policykitgnome = PolicyKit-gnome.spec

Name:                    SFEpolicykit-gnome
Summary:                 GNOME dialogs for PolicyKit
Version:                 0.7
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

BuildRequires: SUNWdbus-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWlibsexy-devel
BuildRequires: SFEpolicykit-devel
Requires: SUNWdbus
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-vfs
Requires: SUNWlibsexy
Requires: SFEpolicykit

%include default-depend.inc

%package devel
Summary:                 %{summary} - development files 
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version
%policykitgnome.prep -d %name-%version

%build
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="-L/usr/lib/polkit -R/usr/lib/polkit"
export PKG_CONFIG_PATH=%{_prefix}/lib/polkit/pkgconfig:%{_prefix}/lib/pkgconfig
%policykitgnome.build -d %name-%version

%install
%policykitgnome.install -d %name-%version

# -f used because charset alias doesn't seem to be created when using
# gnu libiconv/libintl
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -f $RPM_BUILD_ROOT%{_libdir}/PolicyKit/modules/*.{la,ai}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/polkit-gnome-authorization
%{_bindir}/polkit-gnome-example
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libexecdir}/polkit-gnome-manager
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, root) %{_datadir}/PolicyKit
%dir %attr (0755, root, root) %{_datadir}/PolicyKit/policy
%{_datadir}/PolicyKit/policy/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_datadir}/dbus-1

%files devel
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/polkit-gnome.pc
%dir %attr (0755, root, bin) %dir %{_includedir}
%dir %attr (0755, root, bin) %dir %{_includedir}/PolicyKit
%{_includedir}/PolicyKit/*
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, bin) %{_datadir}/gtk-doc

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%endif

%changelog
* Wed Feb 06 2008 - brian.cameron@sun.com
- cleanup
* Thu Jan 31 2008 - Jim.li@sun.com
- initial SFE release.
