#
# spec file for package SFEemerillon
#
# includes module(s): emerillon
#
# bugdb: bugzilla.freedesktop.org
#

%include Solaris.inc
Name:                    SFEemerillon
License:                 GPL v3
Group:                   Libraries/Multimedia
Version:                 0.1.2
Source:                  http://download.gnome.org/sources/emerillon/0.1/emerillon-%{version}.tar.bz2
Patch1:                  emerillon-01-rest.diff
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
Summary:                 Map Viewer
URL:                     http://www.novopia.com/emerillon/
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:            %{_basedir}

%include default-depend.inc
Requires:                SUNWglib2
Requires:                SUNWgtk2
Requires:                SUNWdbus-glib
Requires:                SUNWgnome-config
Requires:                SFElibchamplain
Requires:                SFEgeoclue
Requires:                SFElibrest
Requires:                SFEethos
BuildRequires:           SUNWglib2-devel
BuildRequires:           SUNWgtk2-devel
BuildRequires:           SUNWdbus-glib-devel
BuildRequires:           SUNWgnome-config-devel
BuildRequires:           SFElibchamplain-devel
BuildRequires:           SFEgeoclue-devel
BuildRequires:           SFElibrest-devel
BuildRequires:           SFEethos-devel
BuildRequires:           SUNWgtk-doc

%package root
Summary:		 %{summary} - / filesystem
SUNW_BaseDir:		 /
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif


%prep
%setup -q -n emerillon-%version
%patch1 -p1

%build
./configure \
   --prefix=%{_prefix} \
   --libexecdir=%{_libexecdir} \
   --sysconfdir=%{_sysconfdir}
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'

%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache gconf-cache

%postun
%restart_fmri desktop-mime-cache

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%attr (0755, root, bin)%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/emerillon
%dir %attr (0755, root, bin) %{_libdir}/emerillon/plugins
%dir %attr (0755, root, bin) %{_libdir}/emerillon/plugins/*
%{_libdir}/gir*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_datadir}/emerillon
%{_datadir}/gir*
%{_datadir}/vala
%dir %attr (-, root, other) %{_datadir}/gnome
%{_datadir}/gnome/*
%{_datadir}/gtk-doc

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/emerillon.schemas

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%if %build_l10n
%files l10n
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%{_localedir}
%endif

%changelog
* Sat Jan 15 2011 - Milan Jurik
- with locales build
* Fri Jan 07 2011 - Milan Jurik
- bump to 0.1.2
* Tue Feb 16 2010 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.1.1.  Remove upstream patch emerillon-01-Wl.diff
* Sun Oct 11 2009 - Brian Cameron  <brian.cameron@sun.com>
- Created.
